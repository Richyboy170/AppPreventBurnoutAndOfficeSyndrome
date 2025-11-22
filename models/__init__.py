"""Database models for the Burnout Prevention App."""
from models.user import User, Base as UserBase
from models.activity import Activity, ConversationHistory, Base as ActivityBase
from models.achievement import Achievement, UserAchievement, Base as AchievementBase
from models.pet import Pet, Base as PetBase

# Combine all bases for database initialization
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

__all__ = [
    'User',
    'Activity',
    'ConversationHistory',
    'Achievement',
    'UserAchievement',
    'Pet',
    'Base'
]
