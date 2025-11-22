"""Stretch coach agent for guiding stretches and verifying completion."""
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime

from config import settings
from tools.database_tools import get_db
from tools.notification_tools import get_notification_manager


class StretchCoachAgent:
    """Agent for stretch guidance and tracking."""

    def __init__(self, user_id: int):
        """Initialize stretch coach agent."""
        self.user_id = user_id
        self.db = get_db()
        self.notification_manager = get_notification_manager()

        # Load stretch library
        self.stretches = self._load_stretches()

    def _load_stretches(self) -> Dict[str, Any]:
        """Load stretch library from JSON."""
        stretches_file = settings.DATA_DIR / "stretches.json"
        if not stretches_file.exists():
            print(f"Warning: {stretches_file} not found")
            return {"stretches": [], "categories": {}, "routines": {}}

        with open(stretches_file, 'r') as f:
            return json.load(f)

    def get_all_stretches(self) -> List[Dict[str, Any]]:
        """Get all available stretches."""
        return self.stretches.get('stretches', [])

    def get_stretch_by_id(self, stretch_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific stretch by ID."""
        for stretch in self.stretches.get('stretches', []):
            if stretch['id'] == stretch_id:
                return stretch
        return None

    def get_stretches_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get stretches in a specific category."""
        return [s for s in self.stretches.get('stretches', [])
                if s.get('category') == category]

    def get_random_stretch(self, difficulty: str = None) -> Optional[Dict[str, Any]]:
        """Get a random stretch, optionally filtered by difficulty."""
        import random

        stretches = self.get_all_stretches()

        if difficulty:
            stretches = [s for s in stretches if s.get('difficulty') == difficulty]

        return random.choice(stretches) if stretches else None

    def suggest_stretch(self, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Suggest an appropriate stretch based on user context.

        Args:
            user_context: Optional context (pain_points, recent_stretches, etc.)

        Returns:
            Dictionary with stretch suggestion
        """
        # Get user info
        user = self.db.get_user(self.user_id)

        # Simple suggestion logic
        if user and user.pain_points:
            # Suggest based on pain points
            for pain_point in user.pain_points:
                stretches = self.get_stretches_by_category(pain_point)
                if stretches:
                    import random
                    return {
                        'stretch': random.choice(stretches),
                        'reason': f'Targeting your {pain_point} area'
                    }

        # Default: random beginner stretch
        stretch = self.get_random_stretch(difficulty='beginner')
        return {
            'stretch': stretch,
            'reason': 'A good general stretch to get started'
        }

    def start_stretch(self, stretch_id: str) -> Dict[str, Any]:
        """Start a stretch session.

        Args:
            stretch_id: ID of the stretch to start

        Returns:
            Dictionary with stretch details and instructions
        """
        stretch = self.get_stretch_by_id(stretch_id)

        if not stretch:
            return {'error': 'Stretch not found'}

        # Send notification
        self.notification_manager.send_stretch_suggestion(stretch['name'])

        return {
            'stretch': stretch,
            'started_at': datetime.utcnow(),
            'message': f"Great choice! Let's do the {stretch['name']}."
        }

    def complete_stretch(self, stretch_id: str, photo_path: str = None,
                        duration: int = None) -> Dict[str, Any]:
        """Record stretch completion.

        Args:
            stretch_id: ID of completed stretch
            photo_path: Optional path to verification photo
            duration: Optional actual duration in seconds

        Returns:
            Dictionary with completion details and points earned
        """
        stretch = self.get_stretch_by_id(stretch_id)

        if not stretch:
            return {'error': 'Stretch not found'}

        # Default duration from stretch definition
        if not duration:
            duration = stretch.get('duration_seconds', 30)

        # Points from stretch definition
        points = stretch.get('points', settings.POINTS_PER_STRETCH)

        # Log activity
        activity = self.db.log_activity(
            user_id=self.user_id,
            activity_type='stretch',
            duration=duration,
            points_earned=points,
            stretch_name=stretch['name'],
            photo_verified=photo_path is not None,
            photo_path=photo_path
        )

        # Update pet stats (stretches make pet happy!)
        pet = self.db.update_pet_stats(
            user_id=self.user_id,
            health_change=settings.PET_HEALTH_GAIN_PER_BREAK / 2,  # Half of break health
            happiness_change=settings.PET_HAPPINESS_GAIN_PER_STRETCH,
            exp_gain=settings.PET_XP_PER_ACTIVITY
        )

        return {
            'success': True,
            'stretch_name': stretch['name'],
            'points_earned': points,
            'timestamp': activity.timestamp,
            'pet_health': pet.health if pet else None,
            'pet_happiness': pet.happiness if pet else None,
            'message': f"Excellent work! You earned {points} points!"
        }

    def get_routine(self, routine_name: str) -> Optional[Dict[str, Any]]:
        """Get a stretch routine by name."""
        routines = self.stretches.get('routines', {})
        return routines.get(routine_name)

    def get_all_routines(self) -> Dict[str, Any]:
        """Get all available routines."""
        return self.stretches.get('routines', {})

    def get_stretch_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get stretch statistics for the user.

        Args:
            days: Number of days to look back

        Returns:
            Dictionary with stretch statistics
        """
        activities = self.db.get_activities(
            user_id=self.user_id,
            activity_type='stretch',
            days=days
        )

        total_stretches = len(activities)
        total_duration = sum(a.duration or 0 for a in activities)
        verified_stretches = sum(1 for a in activities if a.photo_verified)

        # Count by stretch name
        stretch_counts = {}
        for activity in activities:
            name = activity.stretch_name or 'Unknown'
            stretch_counts[name] = stretch_counts.get(name, 0) + 1

        # Most common stretch
        most_common = max(stretch_counts.items(), key=lambda x: x[1])[0] if stretch_counts else None

        # Categories covered
        categories_used = set()
        for activity in activities:
            if activity.stretch_name:
                stretch = self.get_stretch_by_name(activity.stretch_name)
                if stretch:
                    categories_used.add(stretch.get('category', 'unknown'))

        return {
            'total_stretches': total_stretches,
            'total_duration_seconds': total_duration,
            'verified_count': verified_stretches,
            'most_common_stretch': most_common,
            'stretch_counts': stretch_counts,
            'categories_covered': len(categories_used),
            'days_analyzed': days
        }

    def get_stretch_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a stretch by its name."""
        for stretch in self.get_all_stretches():
            if stretch.get('name') == name:
                return stretch
        return None

    def get_categories(self) -> Dict[str, Any]:
        """Get all stretch categories with metadata."""
        return self.stretches.get('categories', {})


def create_stretch_coach(user_id: int) -> StretchCoachAgent:
    """Factory function to create a stretch coach agent."""
    return StretchCoachAgent(user_id)
