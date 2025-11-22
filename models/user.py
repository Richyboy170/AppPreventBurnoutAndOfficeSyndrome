"""User model for storing user profiles and preferences."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from datetime import datetime

from models.base import Base


class User(Base):
    """User model with preferences and settings."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    # Preferences
    break_interval = Column(Integer, default=45)  # minutes
    stretch_goal_daily = Column(Integer, default=5)  # number of stretches
    notifications_enabled = Column(Boolean, default=True)
    calendar_integration = Column(Boolean, default=False)

    # Personalization
    fitness_level = Column(String(20), default='beginner')  # beginner, intermediate, advanced
    pain_points = Column(JSON, default=list)  # ['neck', 'back', 'wrists', etc.]
    work_schedule = Column(JSON, default=dict)  # Working hours preferences

    # Stats
    total_breaks_taken = Column(Integer, default=0)
    total_stretches_completed = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)

    # Pet preferences
    pet_name = Column(String(50), default='Buddy')
    pet_type = Column(String(50), default='encouraging_coach')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', streak={self.current_streak})>"

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'break_interval': self.break_interval,
            'stretch_goal_daily': self.stretch_goal_daily,
            'notifications_enabled': self.notifications_enabled,
            'calendar_integration': self.calendar_integration,
            'fitness_level': self.fitness_level,
            'pain_points': self.pain_points,
            'work_schedule': self.work_schedule,
            'total_breaks_taken': self.total_breaks_taken,
            'total_stretches_completed': self.total_stretches_completed,
            'total_points': self.total_points,
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'pet_name': self.pet_name,
            'pet_type': self.pet_type
        }
