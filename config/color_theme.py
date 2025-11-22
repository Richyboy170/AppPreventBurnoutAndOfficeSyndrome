"""
Color Psychology-Based Theme Configuration for Wellness App

This module defines color palettes based on color psychology principles:
- Red: Energy, power, urgency (high-intensity activities)
- Blue: Calm, focus, clarity (meditation, rest activities)
- Green: Balance, relaxation, nature (recovery, wellness)
- Yellow: Happiness, optimism, mental clarity (positive feedback)
- Orange: Passion, energy (motivating activities)
- Black: Strength, discipline, sophistication (tracking, discipline)
"""

from typing import Dict, Tuple


class ColorPalette:
    """Main color palette based on color psychology"""

    # Primary Psychology Colors
    ENERGY_RED = "#E74C3C"          # High-intensity, power, urgency
    CALM_BLUE = "#3498DB"           # Focus, clarity, meditation
    BALANCE_GREEN = "#27AE60"       # Relaxation, wellness, recovery
    OPTIMISM_YELLOW = "#F39C12"     # Happiness, mental clarity
    PASSION_ORANGE = "#E67E22"      # Energy, motivation
    DISCIPLINE_BLACK = "#2C3E50"    # Strength, discipline, focus

    # Secondary/Accent Colors
    DEEP_BLUE = "#2874A6"           # Deep focus, serious calm
    SOFT_BLUE = "#5DADE2"           # Gentle calm, eye rest
    TEAL = "#16A085"                # Balance between calm and energy
    FOREST_GREEN = "#229954"        # Nature, grounding
    LIME_GREEN = "#58D68D"          # Fresh energy, vitality
    CORAL = "#EC7063"               # Gentle energy, warmth
    AMBER = "#F8C471"               # Warm optimism
    LAVENDER = "#B19CD9"            # Gentle relaxation
    PURPLE = "#8E44AD"              # Balance, movement

    # Neutral Colors
    LIGHT_GRAY = "#ECF0F1"          # Backgrounds
    MEDIUM_GRAY = "#95A5A6"         # Secondary text
    DARK_GRAY = "#34495E"           # Primary text
    WHITE = "#FFFFFF"               # Pure backgrounds

    # Achievement Tier Colors
    BRONZE = "#CD7F32"              # Bronze tier
    SILVER = "#C0C0C0"              # Silver tier
    GOLD = "#FFD700"                # Gold tier
    PLATINUM = "#E5E4E2"            # Platinum tier

    # Status Colors
    SUCCESS = "#27AE60"             # Success messages, completed
    WARNING = "#F39C12"             # Warnings, caution
    ERROR = "#E74C3C"               # Errors, urgent attention
    INFO = "#3498DB"                # Information, tips


class StretchCategoryColors:
    """
    Color mapping for stretch categories based on their purpose and benefits.
    Each category is assigned colors that psychologically align with its goals.
    """

    CATEGORIES = {
        # Neck tension relief - Blue for calm and stress reduction
        "Neck & Upper Spine": {
            "primary": ColorPalette.CALM_BLUE,
            "secondary": ColorPalette.SOFT_BLUE,
            "psychology": "Calm and stress reduction for tension relief",
            "emoji": "🦒"
        },

        # Shoulder strength and posture - Orange for energy and motivation
        "Shoulders & Upper Back": {
            "primary": ColorPalette.PASSION_ORANGE,
            "secondary": ColorPalette.CORAL,
            "psychology": "Energy and motivation for posture correction",
            "emoji": "💪"
        },

        # Chest opening and breathing - Green for relaxation and wellness
        "Chest & Front Body": {
            "primary": ColorPalette.BALANCE_GREEN,
            "secondary": ColorPalette.LIME_GREEN,
            "psychology": "Balance and wellness for breathing exercises",
            "emoji": "🫁"
        },

        # Back pain relief - Green for healing and balance
        "Back & Spine": {
            "primary": ColorPalette.FOREST_GREEN,
            "secondary": ColorPalette.BALANCE_GREEN,
            "psychology": "Healing and balance for pain relief",
            "emoji": "🦴"
        },

        # Wrist/forearm focus work - Blue for focus and clarity
        "Wrists & Forearms": {
            "primary": ColorPalette.DEEP_BLUE,
            "secondary": ColorPalette.TEAL,
            "psychology": "Focus and clarity for RSI prevention",
            "emoji": "✋"
        },

        # Hip and leg strength - Red for energy and power
        "Hips & Lower Body": {
            "primary": ColorPalette.ENERGY_RED,
            "secondary": ColorPalette.CORAL,
            "psychology": "Energy and power for lower body strength",
            "emoji": "🦵"
        },

        # Leg circulation and movement - Orange for energy
        "Legs & Circulation": {
            "primary": ColorPalette.PASSION_ORANGE,
            "secondary": ColorPalette.AMBER,
            "psychology": "Energy and motivation for circulation",
            "emoji": "👟"
        },

        # Eye rest and vision - Soft Blue for calm and rest
        "Eyes & Vision": {
            "primary": ColorPalette.SOFT_BLUE,
            "secondary": ColorPalette.CALM_BLUE,
            "psychology": "Calm and restfulness for eye strain relief",
            "emoji": "👁️"
        },

        # Full body high-intensity - Red for energy and urgency
        "Full Body & Energy": {
            "primary": ColorPalette.ENERGY_RED,
            "secondary": ColorPalette.PASSION_ORANGE,
            "psychology": "High energy and power for full body activation",
            "emoji": "⚡"
        }
    }

    @classmethod
    def get_category_color(cls, category_name: str, shade: str = "primary") -> str:
        """
        Get color for a specific stretch category.

        Args:
            category_name: Name of the stretch category
            shade: "primary" or "secondary"

        Returns:
            Hex color code
        """
        category = cls.CATEGORIES.get(category_name, {})
        return category.get(shade, ColorPalette.MEDIUM_GRAY)

    @classmethod
    def get_all_category_names(cls) -> list:
        """Get list of all category names"""
        return list(cls.CATEGORIES.keys())


class ActivityColors:
    """Color mapping for different activity types"""

    ACTIVITIES = {
        # Breaks - Green for relaxation and recovery
        "break": {
            "primary": ColorPalette.BALANCE_GREEN,
            "secondary": ColorPalette.LAVENDER,
            "background": ColorPalette.LIGHT_GRAY,
            "text": ColorPalette.WHITE,
            "psychology": "Relaxation and recovery during rest periods",
            "emoji": "☕"
        },

        # Stretches - Dynamic based on category (see StretchCategoryColors)
        "stretch": {
            "primary": ColorPalette.CALM_BLUE,
            "secondary": ColorPalette.SOFT_BLUE,
            "background": ColorPalette.LIGHT_GRAY,
            "text": ColorPalette.WHITE,
            "psychology": "Focus and body awareness during stretching",
            "emoji": "🤸"
        },

        # Chat/Wellness Companion - Yellow for optimism and mental clarity
        "chat": {
            "primary": ColorPalette.OPTIMISM_YELLOW,
            "secondary": ColorPalette.AMBER,
            "background": ColorPalette.LIGHT_GRAY,
            "text": ColorPalette.DARK_GRAY,
            "psychology": "Positivity and mental clarity for wellness conversations",
            "emoji": "💬"
        },

        # Mood Check - Purple for balance and self-awareness
        "mood_check": {
            "primary": ColorPalette.PURPLE,
            "secondary": ColorPalette.LAVENDER,
            "background": ColorPalette.LIGHT_GRAY,
            "text": ColorPalette.WHITE,
            "psychology": "Balance and introspection for mood tracking",
            "emoji": "😊"
        },

        # Stats/Tracking - Black for discipline and focus
        "stats": {
            "primary": ColorPalette.DISCIPLINE_BLACK,
            "secondary": ColorPalette.DARK_GRAY,
            "background": ColorPalette.LIGHT_GRAY,
            "text": ColorPalette.WHITE,
            "psychology": "Discipline and focus for progress tracking",
            "emoji": "📊"
        },

        # Achievements - Yellow/Gold for happiness and accomplishment
        "achievement": {
            "primary": ColorPalette.GOLD,
            "secondary": ColorPalette.OPTIMISM_YELLOW,
            "background": ColorPalette.LIGHT_GRAY,
            "text": ColorPalette.DARK_GRAY,
            "psychology": "Happiness and celebration of accomplishments",
            "emoji": "🏆"
        }
    }

    @classmethod
    def get_activity_color(cls, activity_type: str, shade: str = "primary") -> str:
        """
        Get color for a specific activity type.

        Args:
            activity_type: Type of activity (break, stretch, chat, etc.)
            shade: "primary", "secondary", "background", or "text"

        Returns:
            Hex color code
        """
        activity = cls.ACTIVITIES.get(activity_type, {})
        return activity.get(shade, ColorPalette.MEDIUM_GRAY)


class PetEvolutionColors:
    """Colors for virtual pet evolution stages"""

    STAGES = {
        "egg": {
            "primary": ColorPalette.SOFT_BLUE,
            "secondary": ColorPalette.LAVENDER,
            "psychology": "Calm and nurturing for new beginnings"
        },
        "sprout": {
            "primary": ColorPalette.LIME_GREEN,
            "secondary": ColorPalette.BALANCE_GREEN,
            "psychology": "Growth and fresh energy"
        },
        "buddy": {
            "primary": ColorPalette.OPTIMISM_YELLOW,
            "secondary": ColorPalette.AMBER,
            "psychology": "Friendship and optimism"
        },
        "guardian": {
            "primary": ColorPalette.PURPLE,
            "secondary": ColorPalette.DISCIPLINE_BLACK,
            "psychology": "Wisdom, strength, and protection"
        }
    }


class MoodColors:
    """Color gradient for mood ratings (1-10)"""

    @staticmethod
    def get_mood_color(mood_rating: int) -> str:
        """
        Get color based on mood rating (1-10 scale).
        Uses a gradient from red (stressed) to green (calm).

        Args:
            mood_rating: Mood rating from 1 (worst) to 10 (best)

        Returns:
            Hex color code
        """
        if mood_rating <= 3:
            return ColorPalette.ERROR  # Red for high stress
        elif mood_rating <= 5:
            return ColorPalette.PASSION_ORANGE  # Orange for moderate stress
        elif mood_rating <= 7:
            return ColorPalette.OPTIMISM_YELLOW  # Yellow for neutral
        elif mood_rating <= 9:
            return ColorPalette.LIME_GREEN  # Light green for good
        else:
            return ColorPalette.BALANCE_GREEN  # Green for excellent


class OpenCVColors:
    """
    OpenCV color codes (BGR format) for pose detection visualization.
    Converted from hex colors to BGR tuples for use with cv2.
    """

    @staticmethod
    def hex_to_bgr(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to BGR tuple for OpenCV"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (rgb[2], rgb[1], rgb[0])  # Convert RGB to BGR

    # Pose detection colors
    GOOD_FORM = hex_to_bgr.__func__(ColorPalette.BALANCE_GREEN)  # Green for good form
    NEEDS_ADJUSTMENT = hex_to_bgr.__func__(ColorPalette.PASSION_ORANGE)  # Orange for adjustments
    POOR_FORM = hex_to_bgr.__func__(ColorPalette.ERROR)  # Red for poor form

    # UI elements
    BACKGROUND = (0, 0, 0)  # Black background
    TEXT_PRIMARY = (255, 255, 255)  # White text
    TEXT_SECONDARY = hex_to_bgr.__func__(ColorPalette.MEDIUM_GRAY)  # Gray text
    SKELETON = hex_to_bgr.__func__(ColorPalette.CALM_BLUE)  # Blue for skeleton lines
    JOINTS = hex_to_bgr.__func__(ColorPalette.OPTIMISM_YELLOW)  # Yellow for joint points


# Export commonly used color groups
__all__ = [
    'ColorPalette',
    'StretchCategoryColors',
    'ActivityColors',
    'PetEvolutionColors',
    'MoodColors',
    'OpenCVColors'
]
