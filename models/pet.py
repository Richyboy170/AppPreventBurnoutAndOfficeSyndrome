"""Virtual pet model for habit formation and gamification."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Pet(Base):
    """Virtual pet companion state."""

    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    name = Column(String(50), default='Buddy')
    personality_type = Column(String(50), default='encouraging_coach')
    # Personality types: 'encouraging_coach', 'gentle_supporter', 'playful_motivator', 'wise_mentor'

    # Pet stats
    health = Column(Float, default=100.0)  # 0-100
    happiness = Column(Float, default=100.0)  # 0-100
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)

    # Evolution stages
    evolution_stage = Column(String(20), default='egg')  # egg, sprout, buddy, guardian
    days_active = Column(Integer, default=0)  # Days since creation

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    last_fed = Column(DateTime, default=datetime.utcnow)  # Last break/stretch
    last_interaction = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Pet(id={self.id}, name='{self.name}', stage='{self.evolution_stage}', health={self.health:.1f})>"

    def to_dict(self):
        """Convert pet to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'personality_type': self.personality_type,
            'health': self.health,
            'happiness': self.happiness,
            'level': self.level,
            'experience': self.experience,
            'evolution_stage': self.evolution_stage,
            'days_active': self.days_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_fed': self.last_fed.isoformat() if self.last_fed else None,
            'last_interaction': self.last_interaction.isoformat() if self.last_interaction else None
        }

    def get_evolution_threshold(self):
        """Get days needed for next evolution."""
        thresholds = {
            'egg': 0,
            'sprout': 7,
            'buddy': 21,
            'guardian': 66
        }
        return thresholds.get(self.evolution_stage, 999)

    def check_evolution(self):
        """Check if pet should evolve."""
        if self.evolution_stage == 'egg' and self.days_active >= 7:
            return 'sprout'
        elif self.evolution_stage == 'sprout' and self.days_active >= 21:
            return 'buddy'
        elif self.evolution_stage == 'buddy' and self.days_active >= 66:
            return 'guardian'
        return None

    def update_stats(self, health_change: float = 0, happiness_change: float = 0, exp_gain: int = 0):
        """Update pet stats with bounds checking."""
        self.health = max(0, min(100, self.health + health_change))
        self.happiness = max(0, min(100, self.happiness + happiness_change))
        self.experience += exp_gain

        # Level up logic (every 100 XP)
        while self.experience >= 100 * self.level:
            self.level += 1

        self.last_interaction = datetime.utcnow()
