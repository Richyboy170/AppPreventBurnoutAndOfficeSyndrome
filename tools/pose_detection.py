"""AI-powered pose detection for stretch guidance using MediaPipe."""
import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
import math

from config.color_theme import OpenCVColors

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("Warning: MediaPipe not installed. Pose detection will not work.")


class PoseDetector:
    """Detects human poses using MediaPipe for stretch guidance."""

    def __init__(self):
        """Initialize pose detector."""
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("MediaPipe is required for pose detection")

        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Initialize pose detector
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def calculate_angle(self, point1: Tuple[float, float],
                       point2: Tuple[float, float],
                       point3: Tuple[float, float]) -> float:
        """Calculate angle between three points.

        Args:
            point1: First point (x, y)
            point2: Vertex point (x, y)
            point3: Third point (x, y)

        Returns:
            Angle in degrees
        """
        # Calculate vectors
        vector1 = (point1[0] - point2[0], point1[1] - point2[1])
        vector2 = (point3[0] - point2[0], point3[1] - point2[1])

        # Calculate angle using dot product
        dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        cos_angle = dot_product / (magnitude1 * magnitude2)
        cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]

        angle = math.acos(cos_angle)
        return math.degrees(angle)

    def get_landmark_coordinates(self, landmarks, landmark_id: int,
                                 image_width: int, image_height: int) -> Tuple[float, float]:
        """Get pixel coordinates for a landmark.

        Args:
            landmarks: MediaPipe pose landmarks
            landmark_id: ID of the landmark
            image_width: Width of the image
            image_height: Height of the image

        Returns:
            (x, y) coordinates in pixels
        """
        landmark = landmarks.landmark[landmark_id]
        return (int(landmark.x * image_width), int(landmark.y * image_height))

    def detect_pose(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """Detect pose in an image.

        Args:
            image: Input image (BGR format from OpenCV)

        Returns:
            Dictionary containing pose information or None if no pose detected
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process image
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return None

        # Get image dimensions
        height, width = image.shape[:2]

        # Extract key landmarks
        landmarks = results.pose_landmarks

        # Get coordinates for key points
        left_shoulder = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_SHOULDER, width, height)
        right_shoulder = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_SHOULDER, width, height)
        left_elbow = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_ELBOW, width, height)
        right_elbow = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_ELBOW, width, height)
        left_wrist = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_WRIST, width, height)
        right_wrist = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_WRIST, width, height)
        left_hip = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_HIP, width, height)
        right_hip = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_HIP, width, height)
        left_knee = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_KNEE, width, height)
        right_knee = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_KNEE, width, height)
        left_ankle = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.LEFT_ANKLE, width, height)
        right_ankle = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.RIGHT_ANKLE, width, height)
        nose = self.get_landmark_coordinates(landmarks, self.mp_pose.PoseLandmark.NOSE, width, height)

        # Calculate important angles
        left_elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
        left_shoulder_angle = self.calculate_angle(left_elbow, left_shoulder, left_hip)
        right_shoulder_angle = self.calculate_angle(right_elbow, right_shoulder, right_hip)
        left_hip_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
        right_hip_angle = self.calculate_angle(right_shoulder, right_hip, right_knee)
        left_knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
        right_knee_angle = self.calculate_angle(right_hip, right_knee, right_ankle)

        # Calculate neck tilt (for neck stretches)
        neck_tilt = abs(nose[0] - (left_shoulder[0] + right_shoulder[0]) / 2)

        return {
            'landmarks': landmarks,
            'coordinates': {
                'left_shoulder': left_shoulder,
                'right_shoulder': right_shoulder,
                'left_elbow': left_elbow,
                'right_elbow': right_elbow,
                'left_wrist': left_wrist,
                'right_wrist': right_wrist,
                'left_hip': left_hip,
                'right_hip': right_hip,
                'left_knee': left_knee,
                'right_knee': right_knee,
                'left_ankle': left_ankle,
                'right_ankle': right_ankle,
                'nose': nose,
            },
            'angles': {
                'left_elbow': left_elbow_angle,
                'right_elbow': right_elbow_angle,
                'left_shoulder': left_shoulder_angle,
                'right_shoulder': right_shoulder_angle,
                'left_hip': left_hip_angle,
                'right_hip': right_hip_angle,
                'left_knee': left_knee_angle,
                'right_knee': right_knee_angle,
                'neck_tilt': neck_tilt,
            }
        }

    def draw_pose(self, image: np.ndarray, pose_data: Dict[str, Any]) -> np.ndarray:
        """Draw pose landmarks on image.

        Args:
            image: Input image
            pose_data: Pose data from detect_pose()

        Returns:
            Image with pose drawn
        """
        if pose_data and pose_data.get('landmarks'):
            self.mp_drawing.draw_landmarks(
                image,
                pose_data['landmarks'],
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        return image

    def close(self):
        """Close the pose detector."""
        if self.pose:
            self.pose.close()


class StretchAnalyzer:
    """Analyzes poses to provide stretch guidance."""

    def __init__(self):
        """Initialize stretch analyzer."""
        self.pose_detector = PoseDetector() if MEDIAPIPE_AVAILABLE else None

    def analyze_neck_stretch(self, pose_data: Dict[str, Any], side: str = 'left') -> Dict[str, Any]:
        """Analyze neck side stretch form.

        Args:
            pose_data: Pose data from PoseDetector
            side: 'left' or 'right'

        Returns:
            Analysis results with feedback
        """
        if not pose_data:
            return {'valid': False, 'feedback': 'No pose detected'}

        angles = pose_data['angles']
        neck_tilt = angles['neck_tilt']

        # Check if head is tilted enough (should be at least 20 pixels from center)
        if neck_tilt < 20:
            return {
                'valid': False,
                'feedback': 'Tilt your head more to the side',
                'score': 30
            }

        # Good stretch
        if neck_tilt > 40:
            return {
                'valid': True,
                'feedback': 'Excellent! Hold this position',
                'score': 100
            }

        return {
            'valid': True,
            'feedback': 'Good stretch! Try to tilt a bit more',
            'score': 70
        }

    def analyze_shoulder_stretch(self, pose_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze shoulder stretch form.

        Args:
            pose_data: Pose data from PoseDetector

        Returns:
            Analysis results with feedback
        """
        if not pose_data:
            return {'valid': False, 'feedback': 'No pose detected'}

        angles = pose_data['angles']

        # Check shoulder angles (arms should be raised)
        left_shoulder = angles['left_shoulder']
        right_shoulder = angles['right_shoulder']

        # For shoulder rolls, shoulders should be moving (angles changing)
        # For now, check if arms are in good position
        if left_shoulder > 60 and right_shoulder > 60:
            return {
                'valid': True,
                'feedback': 'Great shoulder position! Keep moving smoothly',
                'score': 90
            }

        return {
            'valid': True,
            'feedback': 'Raise your shoulders and roll them back',
            'score': 50
        }

    def analyze_back_stretch(self, pose_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze back stretch form.

        Args:
            pose_data: Pose data from PoseDetector

        Returns:
            Analysis results with feedback
        """
        if not pose_data:
            return {'valid': False, 'feedback': 'No pose detected'}

        angles = pose_data['angles']

        # Check hip flexion for forward bend
        left_hip = angles['left_hip']
        right_hip = angles['right_hip']

        avg_hip_angle = (left_hip + right_hip) / 2

        if avg_hip_angle < 90:
            return {
                'valid': True,
                'feedback': 'Excellent forward bend! Feel the stretch in your back',
                'score': 100
            }
        elif avg_hip_angle < 120:
            return {
                'valid': True,
                'feedback': 'Good! Bend forward a bit more if comfortable',
                'score': 75
            }

        return {
            'valid': False,
            'feedback': 'Bend forward at the hips to stretch your back',
            'score': 40
        }

    def analyze_generic_stretch(self, pose_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze generic stretch - just check if pose is detected.

        Args:
            pose_data: Pose data from PoseDetector

        Returns:
            Analysis results with feedback
        """
        if not pose_data:
            return {'valid': False, 'feedback': 'No pose detected - make sure you are in frame'}

        return {
            'valid': True,
            'feedback': 'Great! Continue your stretch and hold the position',
            'score': 85
        }

    def analyze_stretch(self, image: np.ndarray, stretch_type: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Analyze a stretch from an image.

        Args:
            image: Input image from camera
            stretch_type: Type of stretch being performed

        Returns:
            Tuple of (annotated image, analysis results)
        """
        if not self.pose_detector:
            return image, {'valid': False, 'feedback': 'MediaPipe not available'}

        # Detect pose
        pose_data = self.pose_detector.detect_pose(image)

        # Annotate image
        annotated_image = image.copy()
        if pose_data:
            annotated_image = self.pose_detector.draw_pose(annotated_image, pose_data)

        # Analyze based on stretch type
        if 'neck' in stretch_type.lower():
            analysis = self.analyze_neck_stretch(pose_data)
        elif 'shoulder' in stretch_type.lower():
            analysis = self.analyze_shoulder_stretch(pose_data)
        elif 'back' in stretch_type.lower():
            analysis = self.analyze_back_stretch(pose_data)
        else:
            analysis = self.analyze_generic_stretch(pose_data)

        # Add text feedback to image
        feedback = analysis.get('feedback', 'Keep stretching!')
        score = analysis.get('score', 0)

        # Determine feedback color based on score (using color psychology)
        if score >= 80:
            score_color = OpenCVColors.GOOD_FORM  # Green for excellent form
        elif score >= 60:
            score_color = OpenCVColors.NEEDS_ADJUSTMENT  # Orange for needs improvement
        else:
            score_color = OpenCVColors.POOR_FORM  # Red for poor form

        # Add semi-transparent overlay for feedback
        overlay = annotated_image.copy()
        cv2.rectangle(overlay, (10, 10), (annotated_image.shape[1] - 10, 100), OpenCVColors.BACKGROUND, -1)
        annotated_image = cv2.addWeighted(annotated_image, 0.7, overlay, 0.3, 0)

        # Add feedback text with psychology-based colors
        cv2.putText(annotated_image, feedback, (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, OpenCVColors.TEXT_PRIMARY, 2)
        cv2.putText(annotated_image, f"Form Score: {score}%", (20, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, score_color, 2)

        return annotated_image, analysis

    def close(self):
        """Close the stretch analyzer."""
        if self.pose_detector:
            self.pose_detector.close()


def create_stretch_analyzer() -> StretchAnalyzer:
    """Factory function to create a stretch analyzer."""
    return StretchAnalyzer()
