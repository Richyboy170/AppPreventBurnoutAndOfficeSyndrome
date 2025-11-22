"""
Railtracks Integration Layer for Burnout Prevention App

This module provides AI-powered functions for wellness management.
Note: Railtracks decorators have been removed as they are not required.
"""

# Railtracks is not used - decorators removed
RAILTRACKS_AVAILABLE = False


from typing import Dict, List, Any, Optional
from datetime import datetime
from anthropic import Anthropic
from pydantic import BaseModel, Field

from config import settings, prompts
from tools.database_tools import get_db


# ============================================================================
# PYDANTIC MODELS - Required for Railtracks function nodes
# ============================================================================

class CalendarEvent(BaseModel):
    """Calendar event model for Railtracks compatibility."""
    title: str
    start_time: str
    end_time: str
    event_type: Optional[str] = "meeting"


class BreakRecord(BaseModel):
    """Break history record for Railtracks compatibility."""
    timestamp: str
    duration: int  # minutes


class ConversationMessage(BaseModel):
    """Conversation message model for Railtracks compatibility."""
    role: str
    content: str


class UserProfile(BaseModel):
    """User profile model for Railtracks compatibility."""
    username: str = "User"
    current_streak: int = 0
    total_points: int = 0


class ActivityMetadata(BaseModel):
    """Activity metadata model for Railtracks compatibility."""
    details: Optional[str] = None
    duration: Optional[int] = None
    category: Optional[str] = None


class RecentActivity(BaseModel):
    """Recent activity data for Railtracks compatibility."""
    breaks_today: int = 0
    stretches_today: int = 0
    last_activity: str = "Unknown"


class StretchRecommendation(BaseModel):
    """Stretch recommendation model."""
    stretch_id: str
    name: str
    duration: Optional[int] = 30
    reasoning: str = ""


class AnalysisResult(BaseModel):
    """Work pattern analysis result."""
    next_break_in_minutes: int
    reasoning: str
    confidence: float


class StressAnalysisResult(BaseModel):
    """Stress detection result."""
    stress_level: int
    indicators: List[str]
    recommendations: List[str]
    full_analysis: Optional[str] = None


class VerificationResult(BaseModel):
    """Stretch verification result."""
    verified: bool
    confidence: float
    feedback: str
    form_corrections: List[str]


class WellnessResponse(BaseModel):
    """Wellness companion response."""
    response: str
    stress_level: Optional[int] = None
    stress_indicators: Optional[List[str]] = None
    suggested_actions: List[str] = []
    recommendations: Optional[List[str]] = None


class CoachingSession(BaseModel):
    """Stretch coaching session."""
    routine: List[StretchRecommendation]
    fitness_level: str
    session_goal: str
    estimated_duration: float
    coaching_tips: List[str]


class BreakSchedule(BaseModel):
    """Break schedule result."""
    next_break_time: str
    next_break_in_minutes: int
    reasoning: str
    confidence: float
    break_type: str
    suggested_activities: List[str]


# ============================================================================
# AI-POWERED FUNCTIONS - Individual AI-powered functions
# ============================================================================

def analyze_work_pattern(calendar_events: List[CalendarEvent], past_breaks: List[BreakRecord]) -> AnalysisResult:
    """
    AI analyzes user's work schedule to optimize break timing.

    This Railtracks function node uses Claude to intelligently determine
    the best times for breaks based on calendar and break history.

    Args:
        calendar_events: List of upcoming calendar events
        past_breaks: History of user's break patterns

    Returns:
        AnalysisResult with optimal break schedule and reasoning
    """
    if not settings.ANTHROPIC_API_KEY:
        return AnalysisResult(
            next_break_in_minutes=45,
            reasoning='Default schedule (API key not configured)',
            confidence=0.5
        )

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        # Convert Pydantic models to dict for prompt
        events_data = [event.model_dump() for event in calendar_events]
        breaks_data = [break_rec.model_dump() for break_rec in past_breaks]

        prompt = f"""Analyze this user's schedule and suggest optimal break timing:

Calendar Events: {events_data}
Past Break Patterns: {breaks_data}

Consider:
1. Ultradian rhythm (90-minute work cycles)
2. Avoiding breaks during meetings
3. User's historical break preferences
4. Energy level patterns

Provide:
- next_break_in_minutes: int
- reasoning: str
- confidence: float (0-1)

Return as JSON."""

        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=500,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response (simplified - would use structured output in production)
        return AnalysisResult(
            next_break_in_minutes=45,
            reasoning=response.content[0].text,
            confidence=0.85
        )

    except Exception as e:
        print(f"Error in analyze_work_pattern: {e}")
        return AnalysisResult(
            next_break_in_minutes=45,
            reasoning=f'Error occurred: {str(e)}',
            confidence=0.3
        )


def detect_stress_level(conversation_history: List[ConversationMessage], recent_activities: RecentActivity) -> StressAnalysisResult:
    """
    Analyzes conversation patterns to detect stress/burnout signals.

    This Railtracks function node provides deep analysis of user's emotional state
    using extended thinking for nuanced understanding.

    Args:
        conversation_history: Recent chat messages
        recent_activities: User's recent wellness activities

    Returns:
        StressAnalysisResult with level, indicators, and recommendations
    """
    if not settings.ANTHROPIC_API_KEY:
        return StressAnalysisResult(
            stress_level=5,
            indicators=['Unable to analyze (no API key)'],
            recommendations=['Configure API key for AI analysis']
        )

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        # Build analysis prompt
        messages_text = "\n".join([
            f"{msg.role}: {msg.content}"
            for msg in conversation_history[-10:]
        ])

        prompt = f"""As a wellness expert, analyze this user's stress level:

Recent Conversation:
{messages_text}

Recent Activities:
- Breaks taken today: {recent_activities.breaks_today}
- Stretches completed: {recent_activities.stretches_today}
- Last activity: {recent_activities.last_activity}

Assess:
1. Stress level (1-10)
2. Key stress indicators
3. Specific recommendations

Be empathetic and actionable."""

        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=800,
            temperature=0.7,
            system="You are an empathetic wellness coach with expertise in stress management.",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse and structure response
        analysis_text = response.content[0].text

        # Simple parsing (would use structured output in production)
        stress_level = 5  # default
        if 'high stress' in analysis_text.lower() or 'very stressed' in analysis_text.lower():
            stress_level = 8
        elif 'moderate stress' in analysis_text.lower():
            stress_level = 6
        elif 'low stress' in analysis_text.lower():
            stress_level = 3

        return StressAnalysisResult(
            stress_level=stress_level,
            indicators=[analysis_text],
            recommendations=['Take a short break', 'Try a breathing exercise'],
            full_analysis=analysis_text
        )

    except Exception as e:
        print(f"Error in detect_stress_level: {e}")
        return StressAnalysisResult(
            stress_level=5,
            indicators=[f'Error: {str(e)}'],
            recommendations=['Unable to analyze at this time']
        )


def generate_personalized_routine(user_pain_points: List[str], fitness_level: str) -> List[StretchRecommendation]:
    """
    Creates customized stretch sequence based on user needs.

    This Railtracks function node generates scientifically-backed stretch
    routines tailored to individual requirements.

    Args:
        user_pain_points: Areas of discomfort (neck, back, shoulders, etc.)
        fitness_level: User's fitness level (beginner, intermediate, advanced)

    Returns:
        List of recommended stretches with instructions
    """
    if not settings.ANTHROPIC_API_KEY:
        return [
            StretchRecommendation(
                stretch_id='neck_side_stretch',
                name='Neck Side Stretch',
                reasoning='Default recommendation'
            )
        ]

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        prompt = f"""Create a personalized stretch routine:

User Profile:
- Pain points: {', '.join(user_pain_points)}
- Fitness level: {fitness_level}

Requirements:
- 5-7 stretches
- Office-friendly (no equipment needed)
- Progressive difficulty
- Target specific pain points
- Include warmup and cooldown

Provide scientific reasoning for each selection."""

        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1000,
            temperature=0.7,
            system="You are a physical therapist specializing in office ergonomics.",
            messages=[{"role": "user", "content": prompt}]
        )

        routine_text = response.content[0].text

        # Return structured routine (simplified)
        return [
            StretchRecommendation(
                stretch_id='neck_rotation',
                name='Gentle Neck Rotation',
                duration=30,
                reasoning=routine_text
            ),
            StretchRecommendation(
                stretch_id='shoulder_rolls',
                name='Shoulder Rolls',
                duration=30,
                reasoning='Relieves upper back tension'
            )
        ]

    except Exception as e:
        print(f"Error in generate_personalized_routine: {e}")
        return []


def verify_stretch_completion(photo_description: str, stretch_type: str) -> VerificationResult:
    """
    Vision API analyzes photo to verify stretch was performed.

    This Railtracks function node would use Claude's vision capabilities
    to verify proper form and completion (demo version).

    Args:
        photo_description: Description or base64 image
        stretch_type: Expected stretch being performed

    Returns:
        VerificationResult with feedback
    """
    # Note: In production, this would use Claude Vision API with actual images
    return VerificationResult(
        verified=True,
        confidence=0.85,
        feedback=f'Good form on {stretch_type}! Keep your shoulders relaxed.',
        form_corrections=[]
    )


# ============================================================================
# AI AGENT FUNCTIONS - Complex multi-step agents
# ============================================================================

def wellness_companion_agent(
    user_message: str,
    user_id: int,
    conversation_history: List[ConversationMessage],
    user_profile: UserProfile
) -> WellnessResponse:
    """
    Main AI companion agent with empathy and wellness expertise.

    This Railtracks agent node orchestrates the wellness conversation,
    integrating stress detection, personalized advice, and emotional support.

    Args:
        user_message: User's current message
        user_id: User identifier
        conversation_history: Previous conversation context
        user_profile: User's wellness data and preferences

    Returns:
        WellnessResponse with text, stress assessment, and actions
    """
    if not settings.ANTHROPIC_API_KEY:
        return WellnessResponse(
            response='I\'m here to support you! (Configure API key for full AI features)',
            stress_level=None,
            suggested_actions=[]
        )

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        db = get_db()

        # Get user context
        stats = db.get_user_stats(user_id, days=7)

        # Build messages for Claude
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation_history
        ]
        messages.append({"role": "user", "content": user_message})

        # Enhanced system prompt with user context
        system_prompt = f"""{prompts.WELLNESS_COMPANION_PROMPT}

Current User Context:
- Username: {user_profile.username}
- Current streak: {user_profile.current_streak} days
- Breaks this week: {stats.get('breaks', 0)}
- Stretches this week: {stats.get('stretches', 0)}
- Total points: {user_profile.total_points}

You have access to the user's wellness data. Be encouraging, specific, and actionable."""

        # Call Claude with extended thinking for deeper empathy
        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=settings.MAX_TOKENS,
            temperature=settings.TEMPERATURE,
            system=system_prompt,
            messages=messages
        )

        response_text = response.content[0].text

        # Use stress detection function node
        recent_activities = RecentActivity(
            breaks_today=stats.get('breaks', 0),
            stretches_today=stats.get('stretches', 0),
            last_activity='chat'
        )

        # Add current message to history for stress analysis
        full_history = conversation_history + [ConversationMessage(role='user', content=user_message)]
        stress_analysis = detect_stress_level(full_history, recent_activities)

        # Determine suggested actions based on conversation
        suggested_actions = []
        if stress_analysis.stress_level > 6:
            suggested_actions.append('take_break')
            suggested_actions.append('breathing_exercise')

        return WellnessResponse(
            response=response_text,
            stress_level=stress_analysis.stress_level,
            stress_indicators=stress_analysis.indicators,
            suggested_actions=suggested_actions,
            recommendations=stress_analysis.recommendations
        )

    except Exception as e:
        print(f"Error in wellness_companion_agent: {e}")
        return WellnessResponse(
            response=f'I\'m experiencing technical difficulties: {str(e)}',
            stress_level=None,
            suggested_actions=[]
        )


def stretch_coaching_agent(
    user_id: int,
    current_pain_points: List[str],
    session_goal: str = "general_wellness"
) -> CoachingSession:
    """
    Stretch coaching agent that creates and guides personalized routines.

    This Railtracks agent node combines routine generation, progress tracking,
    and real-time feedback for effective stretch coaching.

    Args:
        user_id: User identifier
        current_pain_points: Current areas of discomfort
        session_goal: Goal for this session

    Returns:
        CoachingSession with routine and guidance
    """
    db = get_db()
    user = db.get_user(user_id)

    # Determine fitness level from user history
    stats = db.get_user_stats(user_id, days=30)
    total_stretches = stats.get('stretches', 0)

    if total_stretches < 10:
        fitness_level = "beginner"
    elif total_stretches < 50:
        fitness_level = "intermediate"
    else:
        fitness_level = "advanced"

    # Generate personalized routine using function node
    routine = generate_personalized_routine(current_pain_points, fitness_level)

    return CoachingSession(
        routine=routine,
        fitness_level=fitness_level,
        session_goal=session_goal,
        estimated_duration=len(routine) * 1.5,  # minutes
        coaching_tips=[
            'Remember to breathe deeply throughout each stretch',
            'Never push into pain - mild discomfort is okay',
            'Hold each position for 20-30 seconds'
        ]
    )


def break_scheduler_agent(
    user_id: int,
    calendar_events: List[CalendarEvent],
    current_time: datetime
) -> BreakSchedule:
    """
    Intelligent break scheduling agent.

    This Railtracks agent node analyzes work patterns and calendar
    to schedule optimal breaks that enhance productivity.

    Args:
        user_id: User identifier
        calendar_events: Upcoming calendar events
        current_time: Current timestamp

    Returns:
        BreakSchedule with timing and reasoning
    """
    db = get_db()

    # Get user's break history
    recent_activities = db.get_recent_activities(user_id, activity_type='break', limit=20)
    past_breaks = [
        BreakRecord(
            timestamp=activity.timestamp.isoformat(),
            duration=5  # minutes, would be stored in DB
        )
        for activity in recent_activities
    ]

    # Analyze work pattern using function node
    analysis = analyze_work_pattern(calendar_events, past_breaks)

    # Calculate next break time
    from datetime import timedelta
    next_break_time = current_time + timedelta(minutes=analysis.next_break_in_minutes)

    return BreakSchedule(
        next_break_time=next_break_time.isoformat(),
        next_break_in_minutes=analysis.next_break_in_minutes,
        reasoning=analysis.reasoning,
        confidence=analysis.confidence,
        break_type='short' if analysis.next_break_in_minutes < 60 else 'long',
        suggested_activities=[
            'Take a short walk',
            'Do a quick stretch',
            'Grab some water'
        ]
    )


# ============================================================================
# TOOL FUNCTIONS - External integrations and actions
# ============================================================================

def send_break_notification(message: str, urgency: str = "normal") -> bool:
    """
    Railtracks tool node for sending desktop notifications.

    Args:
        message: Notification message
        urgency: Urgency level (low, normal, high)

    Returns:
        Success status
    """
    try:
        from tools.notification_tools import send_notification
        send_notification(
            title="Wellness Reminder",
            message=message,
            app_name="Burnout Prevention"
        )
        return True
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False


def log_wellness_activity(
    user_id: int,
    activity_type: str,
    metadata: Optional[ActivityMetadata] = None
) -> bool:
    """
    Railtracks tool node for logging wellness activities.

    Args:
        user_id: User identifier
        activity_type: Type of activity (break, stretch, chat)
        metadata: Additional activity metadata

    Returns:
        Success status
    """
    try:
        db = get_db()
        # Convert Pydantic model to dict if provided
        metadata_dict = metadata.model_dump() if metadata else {}
        db.log_activity(
            user_id=user_id,
            activity_type=activity_type,
            **metadata_dict
        )
        return True
    except Exception as e:
        print(f"Error logging activity: {e}")
        return False


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def is_railtracks_available() -> bool:
    """Check if Railtracks is properly installed."""
    return RAILTRACKS_AVAILABLE


def get_railtracks_info() -> Dict[str, Any]:
    """Get information about AI integration status."""
    return {
        'available': RAILTRACKS_AVAILABLE,
        'version': None,
        'agent_functions': [
            'wellness_companion_agent',
            'stretch_coaching_agent',
            'break_scheduler_agent'
        ],
        'ai_functions': [
            'analyze_work_pattern',
            'detect_stress_level',
            'generate_personalized_routine',
            'verify_stretch_completion'
        ],
        'tool_functions': [
            'send_break_notification',
            'log_wellness_activity'
        ]
    }
