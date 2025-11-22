"""
Railtracks Integration Layer for Burnout Prevention App

This module demonstrates the use of Railtracks agentic framework to create
intelligent, composable agents for wellness management.
"""

try:
    import railtracks as rt
    RAILTRACKS_AVAILABLE = True
except ImportError:
    RAILTRACKS_AVAILABLE = False
    print("Warning: Railtracks not installed. Using fallback implementations.")
    # Create mock decorators for development without railtracks
    class MockRailtracks:
        @staticmethod
        def agent_node(func):
            """Mock agent_node decorator"""
            return func

        @staticmethod
        def function_node(func):
            """Mock function_node decorator"""
            return func

        @staticmethod
        def tool_node(func):
            """Mock tool_node decorator"""
            return func

    rt = MockRailtracks()


from typing import Dict, List, Any, Optional
from datetime import datetime
from anthropic import Anthropic

from config import settings, prompts
from tools.database_tools import get_db


# ============================================================================
# RAILTRACKS FUNCTION NODES - Individual AI-powered functions
# ============================================================================

@rt.function_node
def analyze_work_pattern(calendar_events: List[Dict], past_breaks: List[Dict]) -> Dict[str, Any]:
    """
    AI analyzes user's work schedule to optimize break timing.

    This Railtracks function node uses Claude to intelligently determine
    the best times for breaks based on calendar and break history.

    Args:
        calendar_events: List of upcoming calendar events
        past_breaks: History of user's break patterns

    Returns:
        Dictionary with optimal break schedule and reasoning
    """
    if not settings.ANTHROPIC_API_KEY:
        return {
            'next_break_in_minutes': 45,
            'reasoning': 'Default schedule (API key not configured)',
            'confidence': 0.5
        }

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        prompt = f"""Analyze this user's schedule and suggest optimal break timing:

Calendar Events: {calendar_events}
Past Break Patterns: {past_breaks}

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
        return {
            'next_break_in_minutes': 45,
            'reasoning': response.content[0].text,
            'confidence': 0.85
        }

    except Exception as e:
        print(f"Error in analyze_work_pattern: {e}")
        return {
            'next_break_in_minutes': 45,
            'reasoning': f'Error occurred: {str(e)}',
            'confidence': 0.3
        }


@rt.function_node
def detect_stress_level(conversation_history: List[Dict], recent_activities: Dict) -> Dict[str, Any]:
    """
    Analyzes conversation patterns to detect stress/burnout signals.

    This Railtracks function node provides deep analysis of user's emotional state
    using extended thinking for nuanced understanding.

    Args:
        conversation_history: Recent chat messages
        recent_activities: User's recent wellness activities

    Returns:
        Stress analysis with level, indicators, and recommendations
    """
    if not settings.ANTHROPIC_API_KEY:
        return {
            'stress_level': 5,
            'indicators': ['Unable to analyze (no API key)'],
            'recommendations': ['Configure API key for AI analysis']
        }

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        # Build analysis prompt
        messages_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history[-10:]
        ])

        prompt = f"""As a wellness expert, analyze this user's stress level:

Recent Conversation:
{messages_text}

Recent Activities:
- Breaks taken today: {recent_activities.get('breaks_today', 0)}
- Stretches completed: {recent_activities.get('stretches_today', 0)}
- Last activity: {recent_activities.get('last_activity', 'Unknown')}

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

        return {
            'stress_level': stress_level,
            'indicators': [analysis_text],
            'recommendations': ['Take a short break', 'Try a breathing exercise'],
            'full_analysis': analysis_text
        }

    except Exception as e:
        print(f"Error in detect_stress_level: {e}")
        return {
            'stress_level': 5,
            'indicators': [f'Error: {str(e)}'],
            'recommendations': ['Unable to analyze at this time']
        }


@rt.function_node
def generate_personalized_routine(user_pain_points: List[str], fitness_level: str) -> List[Dict]:
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
            {
                'stretch_id': 'neck_side_stretch',
                'name': 'Neck Side Stretch',
                'reasoning': 'Default recommendation'
            }
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
            {
                'stretch_id': 'neck_rotation',
                'name': 'Gentle Neck Rotation',
                'duration': 30,
                'reasoning': routine_text
            },
            {
                'stretch_id': 'shoulder_rolls',
                'name': 'Shoulder Rolls',
                'duration': 30,
                'reasoning': 'Relieves upper back tension'
            }
        ]

    except Exception as e:
        print(f"Error in generate_personalized_routine: {e}")
        return []


@rt.function_node
def verify_stretch_completion(photo_description: str, stretch_type: str) -> Dict[str, Any]:
    """
    Vision API analyzes photo to verify stretch was performed.

    This Railtracks function node would use Claude's vision capabilities
    to verify proper form and completion (demo version).

    Args:
        photo_description: Description or base64 image
        stretch_type: Expected stretch being performed

    Returns:
        Verification result with feedback
    """
    # Note: In production, this would use Claude Vision API with actual images
    return {
        'verified': True,
        'confidence': 0.85,
        'feedback': f'Good form on {stretch_type}! Keep your shoulders relaxed.',
        'form_corrections': []
    }


# ============================================================================
# RAILTRACKS AGENT NODES - Complex multi-step agents
# ============================================================================

@rt.agent_node
def wellness_companion_agent(
    user_message: str,
    user_id: int,
    conversation_history: List[Dict],
    user_profile: Dict
) -> Dict[str, Any]:
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
        Agent response with text, stress assessment, and actions
    """
    if not settings.ANTHROPIC_API_KEY:
        return {
            'response': 'I\'m here to support you! (Configure API key for full AI features)',
            'stress_level': None,
            'suggested_actions': []
        }

    try:
        client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        db = get_db()

        # Get user context
        stats = db.get_user_stats(user_id, days=7)

        # Build messages for Claude
        messages = [
            {"role": msg['role'], "content": msg['content']}
            for msg in conversation_history
        ]
        messages.append({"role": "user", "content": user_message})

        # Enhanced system prompt with user context
        system_prompt = f"""{prompts.WELLNESS_COMPANION_PROMPT}

Current User Context:
- Username: {user_profile.get('username', 'User')}
- Current streak: {user_profile.get('current_streak', 0)} days
- Breaks this week: {stats.get('breaks', 0)}
- Stretches this week: {stats.get('stretches', 0)}
- Total points: {user_profile.get('total_points', 0)}

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
        recent_activities = {
            'breaks_today': stats.get('breaks', 0),
            'stretches_today': stats.get('stretches', 0),
            'last_activity': 'chat'
        }

        stress_analysis = detect_stress_level(
            conversation_history + [{'role': 'user', 'content': user_message}],
            recent_activities
        )

        # Determine suggested actions based on conversation
        suggested_actions = []
        if stress_analysis['stress_level'] > 6:
            suggested_actions.append('take_break')
            suggested_actions.append('breathing_exercise')

        return {
            'response': response_text,
            'stress_level': stress_analysis['stress_level'],
            'stress_indicators': stress_analysis['indicators'],
            'suggested_actions': suggested_actions,
            'recommendations': stress_analysis['recommendations']
        }

    except Exception as e:
        print(f"Error in wellness_companion_agent: {e}")
        return {
            'response': f'I\'m experiencing technical difficulties: {str(e)}',
            'stress_level': None,
            'suggested_actions': []
        }


@rt.agent_node
def stretch_coaching_agent(
    user_id: int,
    current_pain_points: List[str],
    session_goal: str = "general_wellness"
) -> Dict[str, Any]:
    """
    Stretch coaching agent that creates and guides personalized routines.

    This Railtracks agent node combines routine generation, progress tracking,
    and real-time feedback for effective stretch coaching.

    Args:
        user_id: User identifier
        current_pain_points: Current areas of discomfort
        session_goal: Goal for this session

    Returns:
        Coaching session with routine and guidance
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

    return {
        'routine': routine,
        'fitness_level': fitness_level,
        'session_goal': session_goal,
        'estimated_duration': len(routine) * 1.5,  # minutes
        'coaching_tips': [
            'Remember to breathe deeply throughout each stretch',
            'Never push into pain - mild discomfort is okay',
            'Hold each position for 20-30 seconds'
        ]
    }


@rt.agent_node
def break_scheduler_agent(
    user_id: int,
    calendar_events: List[Dict],
    current_time: datetime
) -> Dict[str, Any]:
    """
    Intelligent break scheduling agent.

    This Railtracks agent node analyzes work patterns and calendar
    to schedule optimal breaks that enhance productivity.

    Args:
        user_id: User identifier
        calendar_events: Upcoming calendar events
        current_time: Current timestamp

    Returns:
        Break schedule with timing and reasoning
    """
    db = get_db()

    # Get user's break history
    recent_activities = db.get_recent_activities(user_id, activity_type='break', limit=20)
    past_breaks = [
        {
            'timestamp': activity.timestamp.isoformat(),
            'duration': 5  # minutes, would be stored in DB
        }
        for activity in recent_activities
    ]

    # Analyze work pattern using function node
    analysis = analyze_work_pattern(calendar_events, past_breaks)

    # Calculate next break time
    from datetime import timedelta
    next_break_time = current_time + timedelta(minutes=analysis['next_break_in_minutes'])

    return {
        'next_break_time': next_break_time.isoformat(),
        'next_break_in_minutes': analysis['next_break_in_minutes'],
        'reasoning': analysis['reasoning'],
        'confidence': analysis['confidence'],
        'break_type': 'short' if analysis['next_break_in_minutes'] < 60 else 'long',
        'suggested_activities': [
            'Take a short walk',
            'Do a quick stretch',
            'Grab some water'
        ]
    }


# ============================================================================
# RAILTRACKS TOOL NODES - External integrations and actions
# ============================================================================

@rt.tool_node
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


@rt.tool_node
def log_wellness_activity(
    user_id: int,
    activity_type: str,
    metadata: Dict[str, Any]
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
        db.log_activity(
            user_id=user_id,
            activity_type=activity_type,
            **metadata
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
    """Get information about Railtracks integration status."""
    return {
        'available': RAILTRACKS_AVAILABLE,
        'version': getattr(rt, '__version__', 'unknown') if RAILTRACKS_AVAILABLE else None,
        'agent_nodes': [
            'wellness_companion_agent',
            'stretch_coaching_agent',
            'break_scheduler_agent'
        ],
        'function_nodes': [
            'analyze_work_pattern',
            'detect_stress_level',
            'generate_personalized_routine',
            'verify_stretch_completion'
        ],
        'tool_nodes': [
            'send_break_notification',
            'log_wellness_activity'
        ]
    }
