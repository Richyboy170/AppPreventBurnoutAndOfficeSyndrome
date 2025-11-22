# AI-Powered Stretch Guidance

## Overview

The Burnout Prevention App now includes AI-powered stretch guidance using computer vision and pose detection. This feature uses your device's camera to provide real-time feedback on your stretching form, helping you perform stretches correctly and safely.

## Features

### Real-Time Pose Detection
- Uses MediaPipe's advanced pose estimation to track your body movements
- Detects 33 key body landmarks for accurate posture analysis
- Works in real-time with your webcam

### Intelligent Form Analysis
- Analyzes joint angles and body positioning
- Provides instant feedback on stretch quality
- Calculates form scores based on proper technique

### Specialized Stretch Analysis
The system provides targeted feedback for different stretch types:

- **Neck Stretches**: Monitors head tilt and alignment
- **Shoulder Stretches**: Tracks shoulder elevation and rotation
- **Back Stretches**: Analyzes hip flexion and spinal positioning
- **General Stretches**: Provides pose detection and holding time feedback

### Gamification & Rewards
- Earn bonus points for good form (up to 20 extra points!)
- Track your form accuracy over time
- View detailed session statistics

## How to Use

### 1. Installation

First, install the required dependencies:

```bash
pip install mediapipe opencv-python numpy
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Starting a Session

1. Log in to the app
2. Navigate to the **Stretches** tab
3. Click on **AI Camera Guidance**
4. Browse available stretches and note the stretch ID
5. Enter the stretch ID and click **Start AI Session**
6. Allow camera access when prompted

### 3. Performing Stretches

1. Position yourself in front of the camera
   - Make sure your full body is visible (or upper body for desk stretches)
   - Ensure good lighting
   - Stand 3-6 feet from the camera

2. Begin your stretch following the instructions

3. Watch the real-time feedback:
   - **Green skeleton overlay**: Your pose is detected
   - **Form Score**: Shows how well you're performing (0-100%)
   - **Real-time Feedback**: Specific guidance for improvement

4. Hold each position as indicated
   - Aim for form scores above 70% for best results
   - The system tracks "good form frames" automatically

### 4. Completing the Session

1. When you've completed the stretch, click **Complete Session**
2. Review your performance metrics:
   - Form Accuracy percentage
   - Total frames analyzed
   - Points earned (base + bonus)

## Form Scoring

Your form is scored based on:

- **100%**: Perfect form - all angles and positions optimal
- **75-99%**: Excellent form - minor improvements possible
- **60-74%**: Good form - some technique refinement needed
- **Below 60%**: Needs improvement - follow feedback closely

## Bonus Points

Earn bonus points based on your form accuracy:
- **90%+ accuracy**: +20 bonus points
- **75-89% accuracy**: +10 bonus points
- **60-74% accuracy**: +5 bonus points

## Tips for Best Results

1. **Camera Setup**
   - Use a stable camera position
   - Ensure good lighting (natural light works best)
   - Remove clutter from the background

2. **Positioning**
   - Face the camera directly for frontal stretches
   - Turn sideways for profile stretches
   - Keep your entire body in frame

3. **Stretching Technique**
   - Start slowly and follow the feedback
   - Don't force positions - comfort is key
   - Hold positions steady for accurate tracking

4. **Environment**
   - Wear fitted clothing for better pose detection
   - Use a clear background
   - Minimize movement in the frame

## Technical Details

### Pose Detection Model
- **Library**: MediaPipe Pose
- **Landmarks**: 33 body keypoints
- **Processing**: Real-time at ~10 FPS
- **Accuracy**: 95%+ in good conditions

### Analyzed Metrics
- Joint angles (elbows, shoulders, hips, knees)
- Body alignment and symmetry
- Position holding stability
- Movement smoothness

### Privacy
- All processing is done locally on your device
- Camera feed is NOT recorded or transmitted
- No images are saved without explicit action

## Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Ensure no other app is using the camera
- Try refreshing the page

### Pose Not Detected
- Move closer or farther from camera
- Improve lighting conditions
- Ensure full body/upper body is visible
- Remove objects blocking your view

### Low Form Scores
- Follow the specific feedback messages
- Start with easier stretches
- Check your positioning against stretch instructions
- Practice slowly and deliberately

### Performance Issues
- Close other browser tabs
- Reduce camera resolution if needed
- Ensure good internet connection (for web version)

## Supported Stretches

All stretches in the library are supported! The AI adapts its analysis based on the stretch category:

- Neck & Head stretches
- Shoulder & Upper back stretches
- Lower back stretches
- Hip & Leg stretches
- Full body stretches

## Future Enhancements

Planned features:
- Video recording of sessions
- Multi-angle pose analysis
- Custom stretch routines with AI guidance
- Progress tracking over time
- Comparative analysis with ideal form

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the tips for best results
3. Ensure all dependencies are installed
4. Report issues on the project GitHub

---

**Enjoy your AI-guided stretching journey! Your body will thank you!** 🌟
