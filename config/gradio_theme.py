"""
Custom Gradio Theme based on Color Psychology

This module creates a custom Gradio theme that applies our color psychology-based
palette to the user interface.
"""

import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

from .color_theme import ColorPalette


class WellnessTheme(Base):
    """
    Custom Gradio theme for the Wellness Companion app.
    Incorporates color psychology principles for an optimal user experience.
    """

    def __init__(
        self,
        *,
        primary_hue: str = "blue",
        secondary_hue: str = "green",
        neutral_hue: str = "slate",
        spacing_size: str = "md",
        radius_size: str = "md",
        text_size: str = "md",
        font: tuple = (fonts.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"),
        font_mono: tuple = (fonts.GoogleFont("IBM Plex Mono"), "ui-monospace", "Consolas", "monospace"),
    ):
        # Convert our hex colors to Gradio color objects
        super().__init__(
            primary_hue=self._create_color_palette(ColorPalette.CALM_BLUE),
            secondary_hue=self._create_color_palette(ColorPalette.BALANCE_GREEN),
            neutral_hue=colors.slate,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )

        # Customize specific component colors
        self.set(
            # Primary button colors (energy and action)
            button_primary_background_fill=ColorPalette.CALM_BLUE,
            button_primary_background_fill_hover=ColorPalette.DEEP_BLUE,
            button_primary_text_color=ColorPalette.WHITE,
            button_primary_border_color=ColorPalette.CALM_BLUE,

            # Secondary button colors (support actions)
            button_secondary_background_fill=ColorPalette.BALANCE_GREEN,
            button_secondary_background_fill_hover=ColorPalette.FOREST_GREEN,
            button_secondary_text_color=ColorPalette.WHITE,
            button_secondary_border_color=ColorPalette.BALANCE_GREEN,

            # Input fields
            input_background_fill=ColorPalette.WHITE,
            input_border_color=ColorPalette.MEDIUM_GRAY,
            input_shadow_focus=f"0 0 0 2px {ColorPalette.CALM_BLUE}",

            # Panel/container backgrounds
            panel_background_fill=ColorPalette.LIGHT_GRAY,
            panel_border_color=ColorPalette.MEDIUM_GRAY,

            # Body
            body_background_fill=ColorPalette.WHITE,
            body_text_color=ColorPalette.DARK_GRAY,

            # Sliders and progress
            slider_color=ColorPalette.CALM_BLUE,

            # Links
            link_text_color=ColorPalette.CALM_BLUE,
            link_text_color_hover=ColorPalette.DEEP_BLUE,

            # Success/error states
            color_accent_soft=ColorPalette.BALANCE_GREEN,
            stat_background_fill=ColorPalette.LIGHT_GRAY,
        )

    @staticmethod
    def _create_color_palette(base_hex: str):
        """
        Create a Gradio-compatible color palette from a hex color.
        Gradio expects color objects, but we can use hex strings directly in most cases.
        """
        return base_hex

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_wellness_theme() -> gr.Theme:
    """
    Factory function to create the wellness theme.

    Returns:
        gr.Theme: Custom Gradio theme instance
    """
    return WellnessTheme()


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
/* Activity-specific button colors */
.activity-break {
    background-color: """ + ColorPalette.BALANCE_GREEN + """ !important;
    border-color: """ + ColorPalette.BALANCE_GREEN + """ !important;
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
