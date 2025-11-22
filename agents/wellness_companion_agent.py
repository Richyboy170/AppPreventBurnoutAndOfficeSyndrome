"""Wellness companion agent for emotional support and conversation.

This agent integrates with Railtracks for advanced agentic capabilities.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from anthropic import Anthropic

from config import settings, prompts
from tools.database_tools import get_db

# Import Railtracks integration
try:
    from railtracks_integration import (
        wellness_companion_agent,
        detect_stress_level,
        ConversationMessage,
        UserProfile
    )
    RAILTRACKS_ENABLED = True
except ImportError:
    RAILTRACKS_ENABLED = False


class WellnessCompanionAgent:
    """AI companion for emotional support and wellness guidance."""

    def __init__(self, user_id: int):
        """Initialize wellness companion agent."""
        self.user_id = user_id
        self.db = get_db()
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

        # Get user info
        self.user = self.db.get_user(user_id)

        # Current conversation session
        self.session_id = None

    def start_conversation(self) -> str:
        """Start a new conversation session."""
        self.session_id = f"session_{datetime.utcnow().timestamp()}"

        # Get user info for personalization
        user_name = self.user.username if self.user else "there"

        greeting = f"Hi {user_name}! 👋 How are you feeling today?"

        # Save to conversation history
        self.db.save_conversation(
            user_id=self.user_id,
            role='assistant',
            content=greeting,
            session_id=self.session_id
        )

        return greeting

    def chat(self, user_message: str) -> Dict[str, Any]:
        """Process user message and generate response.

        Args:
            user_message: User's message

        Returns:
            Dictionary with response and metadata
        """
        # Save user message
        self.db.save_conversation(
            user_id=self.user_id,
            role='user',
            content=user_message,
            session_id=self.session_id
        )

        # Use Railtracks agent if available, otherwise fallback to direct implementation
        if RAILTRACKS_ENABLED and self.client:
            # Build conversation history as Pydantic models
            conversation_history = self._build_conversation_history_for_railtracks()

            # Build user profile as Pydantic model
            user_profile = UserProfile(
                username=self.user.username if self.user else 'User',
                current_streak=self.user.current_streak if self.user else 0,
                total_points=self.user.total_points if self.user else 0
            )

            # Call Railtracks wellness companion agent
            result = wellness_companion_agent(
                user_message=user_message,
                user_id=self.user_id,
                conversation_history=conversation_history,
                user_profile=user_profile
            )

            # Extract response from Pydantic model
            response_text = result.response
            stress_level = result.stress_level

        # If no API key or Railtracks not available, return simple response
        elif not self.client:
            response_text = self._simple_response(user_message)
            stress_level = None
        else:
            # Get AI response using direct implementation
            response_text, stress_level = self._get_ai_response(user_message)

        # Save assistant response
        self.db.save_conversation(
            user_id=self.user_id,
            role='assistant',
            content=response_text,
            session_id=self.session_id,
            stress_indicators=None
        )

        # Log activity
        self.db.log_activity(
            user_id=self.user_id,
            activity_type='chat',
            points_earned=settings.POINTS_PER_CHAT,
            chat_summary=user_message[:100],
            stress_level=stress_level
        )

        return {
            'response': response_text,
            'stress_level': stress_level,
            'timestamp': datetime.utcnow()
        }

    def _get_ai_response(self, user_message: str) -> tuple[str, Optional[int]]:
        """Get AI-powered response using Claude.

        Returns:
            Tuple of (response_text, stress_level)
        """
        try:
            # Get conversation history for context
            history = self.db.get_conversation_history(
                user_id=self.user_id,
                limit=settings.MAX_CONVERSATION_HISTORY,
                session_id=self.session_id
            )

            # Build conversation context
            messages = []
            for msg in reversed(history):  # Reverse to get chronological order
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Get user stats for context
            stats = self.db.get_user_stats(self.user_id, days=7)
            pet = self.db.get_pet(self.user_id)

            # Build system prompt with context
            system_prompt = f"""{prompts.WELLNESS_COMPANION_PROMPT}

Current user context:
- Total breaks this week: {stats['breaks']}
- Total stretches this week: {stats['stretches']}
- Current streak: {self.user.current_streak if self.user else 0} days
- Pet health: {pet.health if pet else 'N/A'}
- Pet happiness: {pet.happiness if pet else 'N/A'}
"""

            # Call Claude API
            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
                system=system_prompt,
                messages=messages
            )

            response_text = response.content[0].text

            # Simple stress detection (basic version)
            stress_level = self._detect_stress_level(user_message, response_text)

            return response_text, stress_level

        except Exception as e:
            print(f"Error getting AI response: {e}")
            return self._simple_response(user_message), None

    def _simple_response(self, user_message: str) -> str:
        """Simple rule-based response when API is not available."""
        message_lower = user_message.lower()

        # Stress indicators
        if any(word in message_lower for word in ['stressed', 'overwhelmed', 'anxious', 'tired', 'exhausted']):
            return "I hear that you're feeling stressed. Remember, it's okay to take things one step at a time. Have you tried taking a short break or doing a quick stretch? Sometimes even a few minutes can help reset your mood."

        # Positive indicators
        elif any(word in message_lower for word in ['good', 'great', 'happy', 'better']):
            return "That's wonderful to hear! I'm glad you're feeling good. Keep up the great work with your wellness habits!"

        # Questions about breaks/stretches
        elif any(word in message_lower for word in ['break', 'stretch', 'exercise']):
            return "Taking regular breaks and stretching are great for preventing burnout! Would you like me to suggest a stretch or remind you to take breaks?"

        # Default supportive response
        else:
            return "I'm here to support you. Tell me more about what's on your mind, or let me know if you'd like to take a break or do some stretches together."

    def _detect_stress_level(self, user_message: str, ai_response: str) -> Optional[int]:
        """Simple stress level detection.

        Returns:
            Stress level 1-10, or None
        """
        message_lower = user_message.lower()

        # High stress indicators
        high_stress_words = ['overwhelmed', 'can\'t cope', 'breaking down', 'terrible', 'awful']
        if any(word in message_lower for word in high_stress_words):
            return 8

        # Medium stress indicators
        medium_stress_words = ['stressed', 'anxious', 'worried', 'frustrated', 'tired']
        if any(word in message_lower for word in medium_stress_words):
            return 6

        # Low stress indicators
        low_stress_words = ['okay', 'fine', 'managing', 'alright']
        if any(word in message_lower for word in low_stress_words):
            return 4

        # Positive indicators
        positive_words = ['good', 'great', 'happy', 'better', 'excellent']
        if any(word in message_lower for word in positive_words):
            return 2

        return None

    def get_wellness_insight(self, days: int = 7) -> str:
        """Generate wellness insight based on recent activity.

        Args:
            days: Number of days to analyze

        Returns:
            Insight text
        """
        stats = self.db.get_user_stats(self.user_id, days=days)

        if not self.client:
            return self._simple_insight(stats, days)

        try:
            context = f"""User's wellness data for the past {days} days:
- Total activities: {stats['total_activities']}
- Breaks taken: {stats['breaks']}
- Stretches completed: {stats['stretches']}
- Chat sessions: {stats['chats']}
- Average mood: {stats['average_mood'] if stats['average_mood'] else 'Not recorded'}
- Average stress: {stats['average_stress'] if stats['average_stress'] else 'Not recorded'}
- Current streak: {self.user.current_streak if self.user else 0} days

Provide a brief, encouraging insight about their wellness journey and suggest one actionable improvement."""

            response = self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=300,
                temperature=0.7,
                system="You are a supportive wellness coach providing insights.",
                messages=[{"role": "user", "content": context}]
            )

            return response.content[0].text

        except Exception as e:
            print(f"Error generating insight: {e}")
            return self._simple_insight(stats, days)

    def _build_conversation_history(self) -> List[Dict[str, str]]:
        """Build conversation history for Railtracks agent (dict format)."""
        history = self.db.get_conversation_history(
            user_id=self.user_id,
            limit=settings.MAX_CONVERSATION_HISTORY,
            session_id=self.session_id
        )

        messages = []
        for msg in reversed(history):
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        return messages

    def _build_conversation_history_for_railtracks(self):
        """Build conversation history for Railtracks agent (Pydantic models).

        Returns:
            List of ConversationMessage Pydantic models
        """
        if not RAILTRACKS_ENABLED:
            return []

        history = self.db.get_conversation_history(
            user_id=self.user_id,
            limit=settings.MAX_CONVERSATION_HISTORY,
            session_id=self.session_id
        )

        messages = []
        for msg in reversed(history):
            messages.append(ConversationMessage(
                role=msg.role,
                content=msg.content
            ))

        return messages

    def _simple_insight(self, stats: Dict[str, Any], days: int) -> str:
        """Generate simple insight without AI."""
        total = stats['total_activities']

        if total == 0:
            return "You're just getting started on your wellness journey! Try taking your first break or completing a stretch today."

        elif stats['breaks'] < days:
            return f"You've been active with {total} wellness activities! Consider taking more regular breaks throughout your day for optimal wellbeing."

        elif stats['current_streak'] > 0 if self.user else False:
            return f"Great job maintaining your {self.user.current_streak}-day streak! Consistency is key to building lasting wellness habits."

        else:
            return f"You've logged {total} wellness activities this week. Keep up the good work and remember to listen to your body!"


def create_wellness_companion(user_id: int) -> WellnessCompanionAgent:
    """Factory function to create a wellness companion agent."""
    return WellnessCompanionAgent(user_id)
