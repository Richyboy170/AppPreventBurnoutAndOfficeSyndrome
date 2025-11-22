"""Achievement model for gamification system."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Achievement(Base):
    """Achievement definitions and user unlocks."""

    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    achievement_key = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    icon = Column(String(100), default='🏆')
    points_reward = Column(Integer, default=0)
    requirement_type = Column(String(50), nullable=False)  # 'streak', 'total_count', 'special'
    requirement_value = Column(Integer, nullable=False)
    tier = Column(String(20), default='bronze')  # bronze, silver, gold, platinum

    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}', tier='{self.tier}')>"

    def to_dict(self):
        """Convert achievement to dictionary."""
        return {
            'id': self.id,
            'achievement_key': self.achievement_key,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'points_reward': self.points_reward,
            'requirement_type': self.requirement_type,
            'requirement_value': self.requirement_value,
            'tier': self.tier
        }


class UserAchievement(Base):
    """Track which achievements users have unlocked."""

    __tablename__ = 'user_achievements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    viewed = Column(Boolean, default=False)  # Whether user has seen the unlock notification

    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"

    def to_dict(self):
        """Convert user achievement to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'achievement_id': self.achievement_id,
            'unlocked_at': self.unlocked_at.isoformat() if self.unlocked_at else None,
            'viewed': self.viewed
        }
