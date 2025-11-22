"""Activity model for logging user activities (breaks, stretches, chats)."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Activity(Base):
    """Activity log for tracking all user actions."""

    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    activity_type = Column(String(50), nullable=False)  # 'break', 'stretch', 'chat', 'mood_check'
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Activity details
    duration = Column(Integer, nullable=True)  # seconds
    points_earned = Column(Integer, default=0)

    # Stretch-specific fields
    stretch_name = Column(String(100), nullable=True)
    photo_verified = Column(Boolean, default=False)
    verification_confidence = Column(Float, nullable=True)  # 0.0 to 1.0
    photo_path = Column(String(500), nullable=True)

    # Chat/mood-specific fields
    mood_rating = Column(Integer, nullable=True)  # 1-10
    stress_level = Column(Integer, nullable=True)  # 1-10
    chat_summary = Column(String(500), nullable=True)

    # Additional data
    extra_data = Column(JSON, default=dict)  # Additional flexible data

    def __repr__(self):
        return f"<Activity(id={self.id}, type='{self.activity_type}', user_id={self.user_id})>"

    def to_dict(self):
        """Convert activity to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'duration': self.duration,
            'points_earned': self.points_earned,
            'stretch_name': self.stretch_name,
            'photo_verified': self.photo_verified,
            'verification_confidence': self.verification_confidence,
            'photo_path': self.photo_path,
            'mood_rating': self.mood_rating,
            'stress_level': self.stress_level,
            'chat_summary': self.chat_summary,
            'extra_data': self.extra_data
        }


class ConversationHistory(Base):
    """Store conversation history with AI companion."""

    __tablename__ = 'conversation_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(String(5000), nullable=False)

    # Metadata
    stress_indicators = Column(JSON, nullable=True)  # Detected stress signals
    session_id = Column(String(100), nullable=True)  # Group related conversations

    def __repr__(self):
        return f"<ConversationHistory(id={self.id}, user_id={self.user_id}, role='{self.role}')>"

    def to_dict(self):
        """Convert conversation to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'role': self.role,
            'content': self.content,
            'stress_indicators': self.stress_indicators,
            'session_id': self.session_id
        }
