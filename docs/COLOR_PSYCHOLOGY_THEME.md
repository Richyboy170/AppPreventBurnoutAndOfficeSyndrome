# Color Psychology Theme Documentation

## Overview

The Wellness Companion app uses a carefully designed color theme based on **color psychology principles** to enhance user experience and support the app's wellness goals.

## Color Psychology Principles

Our color choices are based on research in color psychology:

| Color | Psychological Effect | Application in App |
|-------|---------------------|-------------------|
| **Red** | Energy, power, urgency | High-intensity stretches (Full Body, Hips/Legs) |
| **Blue** | Calm, focus, clarity | Meditation-like activities (Neck, Eyes, general stretches) |
| **Green** | Balance, relaxation, nature | Recovery activities (Breaks, Back/Spine stretches) |
| **Yellow** | Happiness, optimism, mental clarity | Positive feedback (Chat, Achievements) |
| **Orange** | Passion, energy, motivation | Energizing activities (Shoulders, Wrists, Circulation) |
| **Black** | Strength, discipline, sophistication | Tracking and discipline (Stats) |

## Color Palette

### Primary Psychology Colors

- **Energy Red**: `#E74C3C` - High-intensity, power, urgency
- **Calm Blue**: `#3498DB` - Focus, clarity, meditation
- **Balance Green**: `#27AE60` - Relaxation, wellness, recovery
- **Optimism Yellow**: `#F39C12` - Happiness, mental clarity
- **Passion Orange**: `#E67E22` - Energy, motivation
- **Discipline Black**: `#2C3E50` - Strength, discipline, focus

### Secondary/Accent Colors

- **Deep Blue**: `#2874A6` - Deep focus, serious calm
- **Soft Blue**: `#5DADE2` - Gentle calm, eye rest
- **Teal**: `#16A085` - Balance between calm and energy
- **Forest Green**: `#229954` - Nature, grounding
- **Lime Green**: `#58D68D` - Fresh energy, vitality
- **Coral**: `#EC7063` - Gentle energy, warmth

## Stretch Category Color Mapping

Each stretch category is assigned colors based on its therapeutic purpose:

### 🦒 Neck & Upper Spine
- **Primary**: Calm Blue (`#3498DB`)
- **Psychology**: Calm and stress reduction for tension relief
- **Purpose**: Helps users relax while addressing neck tension

### 💪 Shoulders & Upper Back
- **Primary**: Passion Orange (`#E67E22`)
- **Psychology**: Energy and motivation for posture correction
- **Purpose**: Energizes users to maintain good posture

### 🫁 Chest & Front Body
- **Primary**: Balance Green (`#27AE60`)
- **Psychology**: Balance and wellness for breathing exercises
- **Purpose**: Promotes relaxation during breathing stretches

### 🦴 Back & Spine
- **Primary**: Forest Green (`#229954`)
- **Psychology**: Healing and balance for pain relief
- **Purpose**: Conveys natural healing and recovery

### ✋ Wrists & Forearms
- **Primary**: Deep Blue (`#2874A6`)
- **Psychology**: Focus and clarity for RSI prevention
- **Purpose**: Emphasizes importance of focused, precise movements

### 🦵 Hips & Lower Body
- **Primary**: Energy Red (`#E74C3C`)
- **Psychology**: Energy and power for lower body strength
- **Purpose**: Motivates dynamic movement

### 👟 Legs & Circulation
- **Primary**: Passion Orange (`#E67E22`)
- **Psychology**: Energy and motivation for circulation
- **Purpose**: Encourages active circulation-boosting movements

### 👁️ Eyes & Vision
- **Primary**: Soft Blue (`#5DADE2`)
- **Psychology**: Calm and restfulness for eye strain relief
- **Purpose**: Promotes eye rest and relaxation

### ⚡ Full Body & Energy
- **Primary**: Energy Red (`#E74C3C`)
- **Psychology**: High energy and power for full body activation
- **Purpose**: Maximizes motivation for energetic movements

## Activity Color Mapping

### ☕ Breaks
- **Primary**: Balance Green
- **Psychology**: Relaxation and recovery during rest periods
- **Visual Effect**: Green button encourages taking restorative breaks

### 🤸 Stretches
- **Primary**: Calm Blue
- **Psychology**: Focus and body awareness during stretching
- **Visual Effect**: Blue promotes mindful, focused stretching

### 💬 Wellness Chat
- **Primary**: Optimism Yellow
- **Psychology**: Positivity and mental clarity for wellness conversations
- **Visual Effect**: Yellow creates welcoming, optimistic interaction

### 📊 Stats & Tracking
- **Primary**: Discipline Black
- **Psychology**: Discipline and focus for progress tracking
- **Visual Effect**: Black conveys serious commitment to wellness goals

### 🏆 Achievements
- **Primary**: Gold (`#FFD700`)
- **Psychology**: Happiness and celebration of accomplishments
- **Visual Effect**: Gold creates sense of achievement and reward

## Achievement Tier Colors

Achievements use metallic colors to represent progression:

- **Bronze**: `#CD7F32` - Entry-level achievements
- **Silver**: `#C0C0C0` - Intermediate achievements
- **Gold**: `#FFD700` - Advanced achievements
- **Platinum**: `#E5E4E2` - Elite achievements (with glow effect)

## Pet Evolution Stage Colors

Pet stages use color gradients to show growth:

### 🥚 Egg Stage
- **Colors**: Soft Blue → Lavender
- **Psychology**: Calm and nurturing for new beginnings
- **Visual**: Gentle gradient suggesting potential

### 🌱 Sprout Stage
- **Colors**: Lime Green → Balance Green
- **Psychology**: Growth and fresh energy
- **Visual**: Vibrant greens showing life and development

### 🐾 Buddy Stage
- **Colors**: Optimism Yellow → Amber
- **Psychology**: Friendship and optimism
- **Visual**: Warm yellows representing companionship

### 🛡️ Guardian Stage
- **Colors**: Purple → Discipline Black
- **Psychology**: Wisdom, strength, and protection
- **Visual**: Deep gradient showing maturity and power

## Pose Detection Feedback Colors

Real-time camera feedback uses colors to guide form:

- **Good Form** (80%+): Green - Positive reinforcement
- **Needs Adjustment** (60-79%): Orange - Gentle correction
- **Poor Form** (<60%): Red - Urgent attention needed

## Mood Rating Colors

Mood check uses a gradient from stressed to calm:

| Rating | Color | Emotion |
|--------|-------|---------|
| 1-3 | Red | High stress |
| 4-5 | Orange | Moderate stress |
| 6-7 | Yellow | Neutral |
| 8-9 | Light Green | Good |
| 10 | Green | Excellent |

## Status Message Colors

- **Success** (Green): Positive actions completed
- **Info** (Blue): Helpful information and tips
- **Warning** (Yellow): Gentle reminders or cautions
- **Error** (Red): Issues requiring attention

## Implementation Files

### Configuration Files
- `config/color_theme.py` - Color palette definitions and mappings
- `config/gradio_theme.py` - Gradio theme configuration and custom CSS

### UI Files
- `ui/app.py` - Main UI with themed components

### Tool Files
- `tools/pose_detection.py` - Camera feedback with color psychology

## Design Principles

1. **Consistency**: Colors have consistent meaning throughout the app
2. **Accessibility**: Sufficient contrast for readability
3. **Purposeful**: Each color choice supports a psychological goal
4. **Responsive**: Colors adapt to user's activity context
5. **Intuitive**: Color meanings align with common cultural associations

## User Experience Benefits

1. **Visual Guidance**: Colors guide users to appropriate activities
2. **Emotional Support**: Colors reinforce desired emotional states
3. **Motivation**: Energizing colors for active tasks, calming for rest
4. **Feedback**: Immediate visual feedback on performance
5. **Engagement**: Colorful, visually appealing interface increases usage

## Future Enhancements

Potential areas for color psychology expansion:

- [ ] Dark mode with adjusted color psychology
- [ ] Personalized color preferences based on user feedback
- [ ] Seasonal color themes aligned with wellness goals
- [ ] Accessibility mode with high-contrast alternatives
- [ ] Color-based wellness mood tracking visualizations

## References

The color psychology principles used in this app are based on research in:
- Environmental psychology
- Color therapy
- User experience design
- Sports and fitness motivation
- Stress reduction techniques

## Testing the Theme

To see the color theme in action:

1. Launch the app: `python main.py`
2. Create a user account
3. Navigate through different tabs to see category-specific colors
4. Complete activities to see success/feedback colors
5. Check achievements to see tier colors
6. View stats to see pet evolution colors

## Customization

To customize colors:

1. Edit `config/color_theme.py` to change color values
2. Update mappings in `StretchCategoryColors` or `ActivityColors`
3. Modify `config/gradio_theme.py` for UI theme adjustments
4. Add custom CSS in `CUSTOM_CSS` for additional styling

---

**Remember**: Colors are powerful tools for wellness. Use them mindfully to support your users' journey to better health!
