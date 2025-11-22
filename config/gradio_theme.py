"""
Custom Gradio Theme based on Color Psychology

This module creates a custom Gradio theme that applies our color psychology-based
palette to the user interface.
"""

import gradio as gr
try:
    from gradio.themes.utils import colors, fonts, sizes
except ImportError:
    # Fallback for older Gradio versions
    colors = None
    fonts = None
    sizes = None

from .color_theme import ColorPalette


def create_wellness_theme():
    """
    Factory function to create the wellness theme.

    NOTE: This function now returns None and relies on CSS for styling.
    This approach is more compatible across different Gradio versions.

    Returns:
        None: No theme object is created, styling is done via CSS
    """
    # We no longer create a theme object to avoid version compatibility issues
    # All styling is now done through CUSTOM_CSS
    return None


def create_activity_button_style(activity_type: str) -> dict:
    """
    Create button styling for specific activity types.

    Args:
        activity_type: Type of activity (break, stretch, chat, etc.)

    Returns:
        dict: Style configuration for Gradio button
    """
    from .color_theme import ActivityColors

    activity_config = ActivityColors.ACTIVITIES.get(activity_type, {})

    return {
        "variant": "primary",
        "size": "lg",
        # Note: Gradio buttons don't accept direct color props,
        # but we can use elem_classes for CSS customization
        "elem_classes": [f"activity-{activity_type}"]
    }


def create_stretch_category_style(category_name: str) -> dict:
    """
    Create styling for stretch category cards/buttons.

    Args:
        category_name: Name of the stretch category

    Returns:
        dict: Style configuration
    """
    from .color_theme import StretchCategoryColors

    category_config = StretchCategoryColors.CATEGORIES.get(category_name, {})

    return {
        "elem_classes": [f"category-{category_name.lower().replace(' & ', '-').replace(' ', '-')}"]
    }


# Custom CSS to apply activity and category colors
CUSTOM_CSS = """
/* Base styling for wellness app */
:root {
    --primary-color: """ + ColorPalette.CALM_BLUE + """;
    --secondary-color: """ + ColorPalette.BALANCE_GREEN + """;
    --background-color: """ + ColorPalette.WHITE + """;
    --text-color: """ + ColorPalette.DARK_GRAY + """;
    --border-radius: 8px;
}

/* Primary buttons */
.primary {
    background: """ + ColorPalette.CALM_BLUE + """ !important;
    border-color: """ + ColorPalette.CALM_BLUE + """ !important;
    color: white !important;
}

.primary:hover {
    background: """ + ColorPalette.DEEP_BLUE + """ !important;
    border-color: """ + ColorPalette.DEEP_BLUE + """ !important;
}

/* Secondary buttons */
.secondary {
    background: """ + ColorPalette.BALANCE_GREEN + """ !important;
    border-color: """ + ColorPalette.BALANCE_GREEN + """ !important;
    color: white !important;
}

.secondary:hover {
    background: """ + ColorPalette.FOREST_GREEN + """ !important;
    border-color: """ + ColorPalette.FOREST_GREEN + """ !important;
}

/* Activity-specific button colors */
.activity-break {
    background-color: """ + ColorPalette.BALANCE_GREEN + """ !important;
    border-color: """ + ColorPalette.BALANCE_GREEN + """ !important;
    color: white !important;
}

.activity-break:hover {
    background-color: """ + ColorPalette.FOREST_GREEN + """ !important;
    border-color: """ + ColorPalette.FOREST_GREEN + """ !important;
}

.activity-stretch {
    background-color: """ + ColorPalette.CALM_BLUE + """ !important;
    border-color: """ + ColorPalette.CALM_BLUE + """ !important;
}

.activity-stretch:hover {
    background-color: """ + ColorPalette.DEEP_BLUE + """ !important;
    border-color: """ + ColorPalette.DEEP_BLUE + """ !important;
}

.activity-chat {
    background-color: """ + ColorPalette.OPTIMISM_YELLOW + """ !important;
    border-color: """ + ColorPalette.OPTIMISM_YELLOW + """ !important;
    color: """ + ColorPalette.DARK_GRAY + """ !important;
}

.activity-chat:hover {
    background-color: """ + ColorPalette.AMBER + """ !important;
    border-color: """ + ColorPalette.AMBER + """ !important;
}

.activity-achievement {
    background-color: """ + ColorPalette.GOLD + """ !important;
    border-color: """ + ColorPalette.GOLD + """ !important;
    color: """ + ColorPalette.DARK_GRAY + """ !important;
}

.activity-achievement:hover {
    background-color: """ + ColorPalette.OPTIMISM_YELLOW + """ !important;
}

.activity-stats {
    background-color: """ + ColorPalette.DISCIPLINE_BLACK + """ !important;
    border-color: """ + ColorPalette.DISCIPLINE_BLACK + """ !important;
}

.activity-stats:hover {
    background-color: """ + ColorPalette.DARK_GRAY + """ !important;
}

/* Stretch category colors */
.category-neck-upper-spine {
    border-left: 4px solid """ + ColorPalette.CALM_BLUE + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.CALM_BLUE + """15, transparent);
}

.category-shoulders-upper-back {
    border-left: 4px solid """ + ColorPalette.PASSION_ORANGE + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.PASSION_ORANGE + """15, transparent);
}

.category-chest-front-body {
    border-left: 4px solid """ + ColorPalette.BALANCE_GREEN + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.BALANCE_GREEN + """15, transparent);
}

.category-back-spine {
    border-left: 4px solid """ + ColorPalette.FOREST_GREEN + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.FOREST_GREEN + """15, transparent);
}

.category-wrists-forearms {
    border-left: 4px solid """ + ColorPalette.DEEP_BLUE + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.DEEP_BLUE + """15, transparent);
}

.category-hips-lower-body {
    border-left: 4px solid """ + ColorPalette.ENERGY_RED + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.ENERGY_RED + """15, transparent);
}

.category-legs-circulation {
    border-left: 4px solid """ + ColorPalette.PASSION_ORANGE + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.PASSION_ORANGE + """15, transparent);
}

.category-eyes-vision {
    border-left: 4px solid """ + ColorPalette.SOFT_BLUE + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.SOFT_BLUE + """15, transparent);
}

.category-full-body-energy {
    border-left: 4px solid """ + ColorPalette.ENERGY_RED + """ !important;
    background: linear-gradient(to right, """ + ColorPalette.ENERGY_RED + """15, transparent);
}

/* Tab styling */
.tab-nav button[aria-selected="true"] {
    border-bottom: 3px solid """ + ColorPalette.CALM_BLUE + """ !important;
}

/* Achievement tier badges */
.tier-bronze {
    color: """ + ColorPalette.BRONZE + """ !important;
    font-weight: bold;
}

.tier-silver {
    color: """ + ColorPalette.SILVER + """ !important;
    font-weight: bold;
}

.tier-gold {
    color: """ + ColorPalette.GOLD + """ !important;
    font-weight: bold;
}

.tier-platinum {
    color: """ + ColorPalette.PLATINUM + """ !important;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(229, 228, 226, 0.5);
}

/* Status messages */
.success-message {
    color: """ + ColorPalette.SUCCESS + """ !important;
    font-weight: 600;
}

.warning-message {
    color: """ + ColorPalette.WARNING + """ !important;
    font-weight: 600;
}

.error-message {
    color: """ + ColorPalette.ERROR + """ !important;
    font-weight: 600;
}

.info-message {
    color: """ + ColorPalette.INFO + """ !important;
    font-weight: 600;
}

/* Pet evolution stage indicators */
.pet-egg {
    background: linear-gradient(135deg, """ + ColorPalette.SOFT_BLUE + """, """ + ColorPalette.LAVENDER + """);
    padding: 10px;
    border-radius: 10px;
}

.pet-sprout {
    background: linear-gradient(135deg, """ + ColorPalette.LIME_GREEN + """, """ + ColorPalette.BALANCE_GREEN + """);
    padding: 10px;
    border-radius: 10px;
}

.pet-buddy {
    background: linear-gradient(135deg, """ + ColorPalette.OPTIMISM_YELLOW + """, """ + ColorPalette.AMBER + """);
    padding: 10px;
    border-radius: 10px;
}

.pet-guardian {
    background: linear-gradient(135deg, """ + ColorPalette.PURPLE + """, """ + ColorPalette.DISCIPLINE_BLACK + """);
    padding: 10px;
    border-radius: 10px;
    color: white;
}

/* Mood indicator colors */
.mood-excellent {
    color: """ + ColorPalette.BALANCE_GREEN + """ !important;
    font-weight: bold;
}

.mood-good {
    color: """ + ColorPalette.LIME_GREEN + """ !important;
    font-weight: bold;
}

.mood-neutral {
    color: """ + ColorPalette.OPTIMISM_YELLOW + """ !important;
    font-weight: bold;
}

.mood-stressed {
    color: """ + ColorPalette.PASSION_ORANGE + """ !important;
    font-weight: bold;
}

.mood-high-stress {
    color: """ + ColorPalette.ERROR + """ !important;
    font-weight: bold;
}

/* Smooth transitions */
button, .tab-nav button {
    transition: all 0.3s ease !important;
}

/* Accessibility - ensure sufficient contrast */
@media (prefers-contrast: high) {
    .activity-chat, .activity-achievement {
        color: """ + ColorPalette.DISCIPLINE_BLACK + """ !important;
    }
}
"""


__all__ = [
    'WellnessTheme',
    'create_wellness_theme',
    'create_activity_button_style',
    'create_stretch_category_style',
    'CUSTOM_CSS'
]
