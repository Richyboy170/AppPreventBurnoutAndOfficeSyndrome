"""Notification tools for desktop notifications."""
import platform
from typing import Optional

try:
    from plyer import notification as plyer_notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    print("Warning: plyer not available. Notifications will be simulated.")

from config import settings


class NotificationManager:
    """Manager for desktop notifications."""

    def __init__(self):
        """Initialize notification manager."""
        self.enabled = settings.NOTIFICATION_ENABLED
        self.platform = platform.system()

    def send_notification(self, title: str, message: str,
                         duration: int = None, app_icon: str = None) -> bool:
        """Send a desktop notification.

        Args:
            title: Notification title
            message: Notification message
            duration: Duration in seconds (default from settings)
            app_icon: Path to app icon

        Returns:
            True if notification was sent successfully
        """
        if not self.enabled:
            print(f"[Notification disabled] {title}: {message}")
            return False

        duration = duration or settings.NOTIFICATION_DURATION

        try:
            if PLYER_AVAILABLE:
                plyer_notification.notify(
                    title=title,
                    message=message,
                    app_name="Wellness App",
                    timeout=duration,
                    app_icon=app_icon
                )
                return True
            else:
                # Fallback: just print
                print(f"[Notification] {title}: {message}")
                return True

        except Exception as e:
            print(f"Error sending notification: {e}")
            return False

    def send_break_reminder(self, message: str = None) -> bool:
        """Send a break reminder notification."""
        title = "⏰ Time for a Break!"
        message = message or "You've been working hard. Take a moment to rest and recharge."
        return self.send_notification(title, message)

    def send_stretch_suggestion(self, stretch_name: str = None) -> bool:
        """Send a stretch suggestion notification."""
        title = "🤸 Stretch Time!"
        if stretch_name:
            message = f"Try the {stretch_name} stretch to relieve tension."
        else:
            message = "Time to move your body! Choose a stretch to complete."
        return self.send_notification(title, message)

    def send_achievement_unlock(self, achievement_name: str, icon: str = "🏆") -> bool:
        """Send achievement unlock notification."""
        title = f"{icon} Achievement Unlocked!"
        message = f"You earned: {achievement_name}"
        return self.send_notification(title, message, duration=8)

    def send_pet_message(self, pet_name: str, message: str) -> bool:
        """Send a message from the virtual pet."""
        title = f"🐾 {pet_name} says:"
        return self.send_notification(title, message, duration=6)

    def send_streak_milestone(self, days: int) -> bool:
        """Send streak milestone notification."""
        title = "🔥 Streak Milestone!"
        message = f"Amazing! You've maintained your wellness streak for {days} days!"
        return self.send_notification(title, message, duration=8)

    def send_wellness_tip(self, tip: str) -> bool:
        """Send a wellness tip notification."""
        title = "💡 Wellness Tip"
        return self.send_notification(title, tip, duration=10)

    def send_stress_alert(self, message: str = None) -> bool:
        """Send a stress level alert."""
        title = "🧘 Wellness Check"
        message = message or "I've noticed you might be stressed. Want to talk about it?"
        return self.send_notification(title, message, duration=12)


# Global notification manager instance
_notification_manager = None

def get_notification_manager() -> NotificationManager:
    """Get or create global notification manager instance."""
    global _notification_manager
    if _notification_manager is None:
        _notification_manager = NotificationManager()
    return _notification_manager


def send_notification(title: str, message: str, **kwargs) -> bool:
    """Quick function to send a notification."""
    manager = get_notification_manager()
    return manager.send_notification(title, message, **kwargs)
