"""Database tools for data persistence and retrieval."""
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, func, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from pathlib import Path

from config import settings
from models.base import Base
from models.user import User
from models.activity import Activity, ConversationHistory
from models.achievement import Achievement, UserAchievement
from models.pet import Pet


class Database:
    """Main database interface."""

    def __init__(self, database_url: str = None):
        """Initialize database connection."""
        self.database_url = database_url or settings.DATABASE_URL
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Create all tables
        self._create_tables()

        # Initialize achievements from JSON
        self._initialize_achievements()

    def _create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()

    def _initialize_achievements(self):
        """Load achievements from JSON file into database."""
        session = self.get_session()
        try:
            # Check if achievements already exist
            if session.query(Achievement).count() > 0:
                return

            # Load achievements from JSON
            achievements_file = settings.DATA_DIR / "achievements.json"
            if not achievements_file.exists():
                print(f"Warning: {achievements_file} not found")
                return

            with open(achievements_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Insert achievements
            for ach_data in data.get('achievements', []):
                achievement = Achievement(
                    achievement_key=ach_data['achievement_key'],
                    name=ach_data['name'],
                    description=ach_data['description'],
                    icon=ach_data['icon'],
                    points_reward=ach_data['points_reward'],
                    requirement_type=ach_data['requirement_type'],
                    requirement_value=ach_data['requirement_value'],
                    tier=ach_data['tier']
                )
                session.add(achievement)

            session.commit()
            print(f"Initialized {len(data.get('achievements', []))} achievements")

        except Exception as e:
            print(f"Error initializing achievements: {e}")
            session.rollback()
        finally:
            session.close()

    # User operations
    def create_user(self, username: str, email: str = None, **kwargs) -> User:
        """Create a new user."""
        session = self.get_session()
        try:
            user = User(username=username, email=email, **kwargs)
            session.add(user)
            session.commit()
            session.refresh(user)

            # Create pet for user
            self.create_pet(user.id, name=kwargs.get('pet_name', 'Buddy'))

            return user
        finally:
            session.close()

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        session = self.get_session()
        try:
            return session.query(User).filter(User.username == username).first()
        finally:
            session.close()

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user attributes."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                for key, value in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                user.last_active = datetime.utcnow()
                session.commit()
                session.refresh(user)
            return user
        finally:
            session.close()

    # Activity operations
    def log_activity(self, user_id: int, activity_type: str, **kwargs) -> Activity:
        """Log a user activity."""
        session = self.get_session()
        try:
            activity = Activity(
                user_id=user_id,
                activity_type=activity_type,
                **kwargs
            )
            session.add(activity)
            session.commit()
            session.refresh(activity)

            # Update user stats
            self._update_user_stats(session, user_id, activity_type, kwargs.get('points_earned', 0))

            # Check for achievements
            self._check_achievements(session, user_id)

            return activity
        finally:
            session.close()

    def _update_user_stats(self, session: Session, user_id: int, activity_type: str, points: int):
        """Update user statistics based on activity."""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return

        if activity_type == 'break':
            user.total_breaks_taken += 1
        elif activity_type == 'stretch':
            user.total_stretches_completed += 1

        user.total_points += points
        user.last_active = datetime.utcnow()

        # Update streak
        self._update_streak(session, user)

        session.commit()

    def _update_streak(self, session: Session, user: User):
        """Update user's activity streak."""
        today = datetime.utcnow().date()

        # Get last activity date (excluding today)
        last_activity = session.query(Activity)\
            .filter(Activity.user_id == user.id)\
            .filter(func.date(Activity.timestamp) < today)\
            .order_by(Activity.timestamp.desc())\
            .first()

        if not last_activity:
            # First activity ever
            user.current_streak = 1
        else:
            last_date = last_activity.timestamp.date()
            days_diff = (today - last_date).days

            if days_diff == 1:
                # Continue streak
                user.current_streak += 1
            elif days_diff == 0:
                # Activity already logged today
                pass
            else:
                # Streak broken
                user.current_streak = 1

        # Update longest streak
        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak

    def get_activities(self, user_id: int, activity_type: str = None,
                      limit: int = 50, days: int = None) -> List[Activity]:
        """Get user activities with optional filters."""
        session = self.get_session()
        try:
            query = session.query(Activity).filter(Activity.user_id == user_id)

            if activity_type:
                query = query.filter(Activity.activity_type == activity_type)

            if days:
                since_date = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Activity.timestamp >= since_date)

            return query.order_by(Activity.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    # Pet operations
    def create_pet(self, user_id: int, name: str = 'Buddy',
                   personality_type: str = 'encouraging_coach') -> Pet:
        """Create a pet for a user."""
        session = self.get_session()
        try:
            pet = Pet(
                user_id=user_id,
                name=name,
                personality_type=personality_type
            )
            session.add(pet)
            session.commit()
            session.refresh(pet)
            return pet
        finally:
            session.close()

    def get_pet(self, user_id: int) -> Optional[Pet]:
        """Get user's pet."""
        session = self.get_session()
        try:
            return session.query(Pet).filter(Pet.user_id == user_id).first()
        finally:
            session.close()

    def update_pet(self, user_id: int, **kwargs) -> Optional[Pet]:
        """Update pet attributes."""
        session = self.get_session()
        try:
            pet = session.query(Pet).filter(Pet.user_id == user_id).first()
            if pet:
                for key, value in kwargs.items():
                    if hasattr(pet, key):
                        setattr(pet, key, value)
                session.commit()
                session.refresh(pet)
            return pet
        finally:
            session.close()

    def update_pet_stats(self, user_id: int, health_change: float = 0,
                        happiness_change: float = 0, exp_gain: int = 0) -> Optional[Pet]:
        """Update pet stats with activity."""
        session = self.get_session()
        try:
            pet = session.query(Pet).filter(Pet.user_id == user_id).first()
            if pet:
                pet.update_stats(health_change, happiness_change, exp_gain)

                # Check for evolution
                new_stage = pet.check_evolution()
                if new_stage:
                    pet.evolution_stage = new_stage
                    # TODO: Trigger evolution celebration

                session.commit()
                session.refresh(pet)
            return pet
        finally:
            session.close()

    # Conversation history
    def save_conversation(self, user_id: int, role: str, content: str,
                         session_id: str = None, stress_indicators: List = None) -> ConversationHistory:
        """Save conversation message."""
        session = self.get_session()
        try:
            conv = ConversationHistory(
                user_id=user_id,
                role=role,
                content=content,
                session_id=session_id,
                stress_indicators=stress_indicators
            )
            session.add(conv)
            session.commit()
            session.refresh(conv)
            return conv
        finally:
            session.close()

    def get_conversation_history(self, user_id: int, limit: int = 50,
                                session_id: str = None) -> List[ConversationHistory]:
        """Get conversation history."""
        session = self.get_session()
        try:
            query = session.query(ConversationHistory).filter(ConversationHistory.user_id == user_id)

            if session_id:
                query = query.filter(ConversationHistory.session_id == session_id)

            return query.order_by(ConversationHistory.timestamp.desc()).limit(limit).all()
        finally:
            session.close()

    # Achievement operations
    def _check_achievements(self, session: Session, user_id: int):
        """Check if user has unlocked any new achievements."""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return

        # Get all achievements
        achievements = session.query(Achievement).all()

        # Get already unlocked achievements
        unlocked = session.query(UserAchievement.achievement_id)\
            .filter(UserAchievement.user_id == user_id)\
            .all()
        unlocked_ids = {a[0] for a in unlocked}

        # Check each achievement
        for achievement in achievements:
            if achievement.id in unlocked_ids:
                continue

            if self._check_achievement_requirement(session, user, achievement):
                # Unlock achievement
                user_ach = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                session.add(user_ach)

                # Award points
                user.total_points += achievement.points_reward

                print(f"🏆 Achievement unlocked: {achievement.name}")

        session.commit()

    def _check_achievement_requirement(self, session: Session, user: User,
                                      achievement: Achievement) -> bool:
        """Check if user meets achievement requirement."""
        req_type = achievement.requirement_type
        req_value = achievement.requirement_value

        if req_type == 'total_count':
            category = achievement.requirement_category if hasattr(achievement, 'requirement_category') else None

            if category == 'stretches':
                return user.total_stretches_completed >= req_value
            elif category == 'breaks':
                return user.total_breaks_taken >= req_value
            elif category == 'points':
                return user.total_points >= req_value

        elif req_type == 'streak':
            return user.current_streak >= req_value

        return False

    def get_user_achievements(self, user_id: int) -> List[Dict]:
        """Get all achievements for a user with unlock status."""
        session = self.get_session()
        try:
            achievements = session.query(Achievement).all()
            unlocked = session.query(UserAchievement)\
                .filter(UserAchievement.user_id == user_id)\
                .all()

            unlocked_dict = {ua.achievement_id: ua for ua in unlocked}

            result = []
            for ach in achievements:
                ach_dict = ach.to_dict()
                if ach.id in unlocked_dict:
                    ach_dict['unlocked'] = True
                    ach_dict['unlocked_at'] = unlocked_dict[ach.id].unlocked_at
                else:
                    ach_dict['unlocked'] = False
                result.append(ach_dict)

            return result
        finally:
            session.close()

    # Statistics and analytics
    def get_user_stats(self, user_id: int, days: int = 7) -> Dict[str, Any]:
        """Get user statistics for a period."""
        session = self.get_session()
        try:
            since_date = datetime.utcnow() - timedelta(days=days)

            activities = session.query(Activity)\
                .filter(Activity.user_id == user_id)\
                .filter(Activity.timestamp >= since_date)\
                .all()

            breaks = sum(1 for a in activities if a.activity_type == 'break')
            stretches = sum(1 for a in activities if a.activity_type == 'stretch')
            chats = sum(1 for a in activities if a.activity_type == 'chat')

            points = sum(a.points_earned for a in activities if a.points_earned)

            # Average mood and stress
            mood_activities = [a for a in activities if a.mood_rating]
            stress_activities = [a for a in activities if a.stress_level]

            avg_mood = sum(a.mood_rating for a in mood_activities) / len(mood_activities) if mood_activities else None
            avg_stress = sum(a.stress_level for a in stress_activities) / len(stress_activities) if stress_activities else None

            return {
                'days': days,
                'total_activities': len(activities),
                'breaks': breaks,
                'stretches': stretches,
                'chats': chats,
                'points_earned': points,
                'average_mood': avg_mood,
                'average_stress': avg_stress,
                'daily_average': len(activities) / days if days > 0 else 0
            }
        finally:
            session.close()


# Global database instance
_db_instance = None

def get_db() -> Database:
    """Get or create global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance
