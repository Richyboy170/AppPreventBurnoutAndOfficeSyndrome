"""Break scheduler agent for managing break reminders.

This agent integrates with Railtracks for intelligent break scheduling.
"""
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from anthropic import Anthropic

from config import settings, prompts
from tools.database_tools import get_db
from tools.notification_tools import get_notification_manager

# Import Railtracks integration
try:
    from railtracks_integration import break_scheduler_agent, analyze_work_pattern
    RAILTRACKS_ENABLED = True
except ImportError:
    RAILTRACKS_ENABLED = False


class BreakSchedulerAgent:
    """Agent for scheduling and managing breaks."""

    def __init__(self, user_id: int):
        """Initialize break scheduler agent."""
        self.user_id = user_id
        self.db = get_db()
        self.notification_manager = get_notification_manager()
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

        # Get user preferences
        self.user = self.db.get_user(user_id)
        self.break_interval = self.user.break_interval if self.user else settings.DEFAULT_BREAK_INTERVAL

        # Track last break time
        self.last_break_time = None
        self._load_last_break()

    def _load_last_break(self):
        """Load the last break time from database."""
        activities = self.db.get_activities(self.user_id, activity_type='break', limit=1)
        if activities:
            self.last_break_time = activities[0].timestamp

    def should_trigger_break(self) -> bool:
        """Check if it's time for a break."""
        if not self.last_break_time:
            # First break of the session
            return False

        time_since_last_break = datetime.utcnow() - self.last_break_time
        minutes_since_break = time_since_last_break.total_seconds() / 60

        return minutes_since_break >= self.break_interval

    def suggest_break(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Suggest a break to the user with reasoning.

        Args:
            context: Optional context about user's current state

        Returns:
            Dictionary with break suggestion details
        """
        # Simple version without Claude AI
        if not self.client:
            return self._simple_break_suggestion()

        # AI-powered suggestion
        try:
            # Calculate time since last break
            time_since_break = None
            if self.last_break_time:
                delta = datetime.utcnow() - self.last_break_time
                time_since_break = int(delta.total_seconds() / 60)

            # Build context message
            context_msg = f"""User has been working for {time_since_break} minutes since last break.
User's preferred break interval: {self.break_interval} minutes.
Current time: {datetime.utcnow().strftime('%H:%M')}
"""
            if context:
                context_msg += f"\nAdditional context: {json.dumps(context)}"

            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=500,
                system=prompts.BREAK_SCHEDULER_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"{context_msg}\n\nSuggest an appropriate break and explain why."
                    }
                ]
            )

            suggestion_text = response.content[0].text

            return {
                'suggested': True,
                'message': suggestion_text,
                'time_since_last_break': time_since_break,
                'break_type': 'regular'
            }

        except Exception as e:
            print(f"Error getting AI break suggestion: {e}")
            return self._simple_break_suggestion()

    def _simple_break_suggestion(self) -> Dict[str, Any]:
        """Simple break suggestion without AI."""
        time_since_break = None
        if self.last_break_time:
            delta = datetime.utcnow() - self.last_break_time
            time_since_break = int(delta.total_seconds() / 60)

        messages = [
            "Time to rest your eyes and stretch!",
            "You've been working hard. Take a moment to recharge.",
            "Step away from your screen and take a breather.",
            "Let's take a quick break to refresh your mind.",
            "Your body and mind need a little break!"
        ]

        import random
        message = random.choice(messages)

        return {
            'suggested': True,
            'message': message,
            'time_since_last_break': time_since_break,
            'break_type': 'regular'
        }

    def notify_break_time(self, custom_message: str = None):
        """Send break notification to user."""
        suggestion = self.suggest_break()
        message = custom_message or suggestion['message']
        self.notification_manager.send_break_reminder(message)

    def record_break(self, duration: int = None) -> Dict[str, Any]:
        """Record that user took a break.

        Args:
            duration: Break duration in seconds

        Returns:
            Dictionary with break details and points earned
        """
        points = settings.POINTS_PER_BREAK

        # Log activity
        activity = self.db.log_activity(
            user_id=self.user_id,
            activity_type='break',
            duration=duration,
            points_earned=points
        )

        # Update last break time
        self.last_break_time = activity.timestamp

        # Update pet stats
        pet = self.db.update_pet_stats(
            user_id=self.user_id,
            health_change=settings.PET_HEALTH_GAIN_PER_BREAK,
            exp_gain=settings.PET_XP_PER_ACTIVITY
        )

        return {
            'success': True,
            'points_earned': points,
            'timestamp': activity.timestamp,
            'pet_health': pet.health if pet else None,
            'pet_happiness': pet.happiness if pet else None
        }

    def get_break_stats(self, days: int = 7) -> Dict[str, Any]:
        """Get break statistics for the user.

        Args:
            days: Number of days to look back

        Returns:
            Dictionary with break statistics
        """
        activities = self.db.get_activities(
            user_id=self.user_id,
            activity_type='break',
            days=days
        )

        total_breaks = len(activities)
        total_duration = sum(a.duration or 0 for a in activities)
        avg_per_day = total_breaks / days if days > 0 else 0

        # Calculate breaks by day of week
        breaks_by_day = {}
        for activity in activities:
            day = activity.timestamp.strftime('%A')
            breaks_by_day[day] = breaks_by_day.get(day, 0) + 1

        return {
            'total_breaks': total_breaks,
            'total_duration_seconds': total_duration,
            'average_per_day': avg_per_day,
            'breaks_by_day': breaks_by_day,
            'days_analyzed': days
        }

    def adjust_interval(self, new_interval: int) -> bool:
        """Adjust the break interval.

        Args:
            new_interval: New interval in minutes

        Returns:
            True if successful
        """
        # Validate interval
        if new_interval < settings.MIN_BREAK_INTERVAL:
            new_interval = settings.MIN_BREAK_INTERVAL
        elif new_interval > settings.MAX_BREAK_INTERVAL:
            new_interval = settings.MAX_BREAK_INTERVAL

        # Update in database
        self.db.update_user(self.user_id, break_interval=new_interval)
        self.break_interval = new_interval

        return True


def create_break_scheduler(user_id: int) -> BreakSchedulerAgent:
    """Factory function to create a break scheduler agent."""
    return BreakSchedulerAgent(user_id)
