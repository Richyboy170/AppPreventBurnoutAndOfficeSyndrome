# 🌟 Burnout & Office Syndrome Prevention App

A comprehensive wellness application powered by **Claude AI** and **Railtracks** to prevent burnout and office syndrome through intelligent break reminders, guided stretching, emotional support, and gamified habit formation.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Railtracks](https://img.shields.io/badge/Framework-Railtracks-purple.svg)
![Claude AI](https://img.shields.io/badge/AI-Claude-orange.svg)

---

## 📖 What Does This App Do?

This application helps office workers and remote professionals maintain their physical and mental health by combining:

- **🤖 AI-Powered Wellness Companion**: Chat with an empathetic AI that provides emotional support and personalized advice
- **⏰ Smart Break Reminders**: Intelligent scheduling based on your work patterns, preventing meeting interruptions
- **🧘 Guided Stretches**: 15+ office-friendly stretches with step-by-step instructions
- **🎥 AI Camera Stretch Guidance**: Real-time pose detection and form feedback using computer vision (MediaPipe)
- **🎮 Gamification**: Points, achievements, streaks, and a virtual pet companion that grows with your wellness journey
- **📊 Progress Tracking**: Monitor your wellness journey with detailed statistics and AI-generated insights

### Why This Matters

- **Burnout costs $190B annually** in healthcare expenses
- **60% of desk workers** suffer from office syndrome (neck pain, back pain, eye strain)
- **Traditional reminders fail** because they're not intelligent or engaging enough

This app solves these problems by making wellness **intelligent**, **personalized**, and **fun**.

---

## 🚀 Railtracks Integration - Agentic AI Framework

This project showcases **Railtracks**, a Python agentic framework that enables building sophisticated AI agents with composable nodes.

### What is Railtracks?

Railtracks provides a declarative way to build AI agents using three types of nodes:

- **🤖 Agent Nodes** (`@rt.agent_node`): Complex multi-step agents that orchestrate workflows
- **⚙️ Function Nodes** (`@rt.function_node`): Individual AI-powered functions with specific purposes
- **🔧 Tool Nodes** (`@rt.tool_node`): External integrations and actions

### Our Railtracks Implementation

We use Railtracks to create three main agents:

#### 1. Wellness Companion Agent (`wellness_companion_agent`)

```python
@rt.agent_node
def wellness_companion_agent(
    user_message: str,
    user_id: int,
    conversation_history: List[Dict],
    user_profile: Dict
) -> Dict[str, Any]:
    """
    Main AI companion agent with empathy and wellness expertise.

    - Provides emotional support
    - Detects stress levels
    - Suggests personalized actions
    - Integrates user wellness data
    """
```

**Key Features:**
- Multi-turn conversations with context awareness
- Integrates with `detect_stress_level` function node
- Analyzes user's wellness history for personalized advice
- Suggests actionable steps based on stress detection

#### 2. Stretch Coaching Agent (`stretch_coaching_agent`)

```python
@rt.agent_node
def stretch_coaching_agent(
    user_id: int,
    current_pain_points: List[str],
    session_goal: str = "general_wellness"
) -> Dict[str, Any]:
    """
    Stretch coaching agent that creates personalized routines.

    - Generates custom stretch sequences
    - Adapts to fitness level
    - Provides real-time form feedback
    - Tracks progress over time
    """
```

**Key Features:**
- Uses `generate_personalized_routine` function node
- Adapts difficulty based on user history
- Provides professional coaching tips
- Estimates session duration

#### 3. Break Scheduler Agent (`break_scheduler_agent`)

```python
@rt.agent_node
def break_scheduler_agent(
    user_id: int,
    calendar_events: List[Dict],
    current_time: datetime
) -> Dict[str, Any]:
    """
    Intelligent break scheduling agent.

    - Analyzes work patterns
    - Respects calendar conflicts
    - Optimizes for ultradian rhythms
    - Provides contextual reasoning
    """
```

**Key Features:**
- Calendar-aware scheduling (no breaks during meetings)
- Uses `analyze_work_pattern` function node
- Learns from user's break history
- Provides reasoning for scheduling decisions

### Railtracks Function Nodes

Our app includes several specialized function nodes:

| Function Node | Purpose |
|--------------|---------|
| `analyze_work_pattern` | AI analyzes calendar and break history for optimal timing |
| `detect_stress_level` | Deep analysis of conversation patterns for stress detection |
| `generate_personalized_routine` | Creates custom stretch sequences based on pain points |
| `verify_stretch_completion` | Vision-based verification of stretch completion (demo) |

### Why Railtracks?

**Traditional Approach:**
```python
# Monolithic function with hard-coded logic
def handle_user_message(message):
    response = call_ai(message)
    send_notification(response)
    return response
```

**Railtracks Approach:**
```python
# Composable, reusable, testable
@rt.agent_node
def wellness_companion_agent(...):
    # Orchestrates multiple function nodes
    stress = detect_stress_level(...)  # Reusable function node
    routine = generate_personalized_routine(...)  # Another reusable node
    return intelligent_response
```

**Benefits:**
- ✅ **Modular**: Each node has a single responsibility
- ✅ **Reusable**: Nodes can be composed in different workflows
- ✅ **Testable**: Test each node independently
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Scalable**: Easy to add new capabilities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Gradio UI Layer                         │
│         (User Interface with Tabs & Components)             │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 Railtracks Agent Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Wellness    │  │   Stretch    │  │    Break     │     │
│  │  Companion   │  │   Coaching   │  │  Scheduler   │     │
│  │    Agent     │  │    Agent     │  │    Agent     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼─────────────┐
│              Railtracks Function Nodes                      │
│  ┌─────────────────┐  ┌──────────────────┐                 │
│  │ detect_stress   │  │ analyze_work     │  ...            │
│  │    _level       │  │    _pattern      │                 │
│  └─────────────────┘  └──────────────────┘                 │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Core Services                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Claude AI  │  │  Database   │  │ Notifications│        │
│  │     API     │  │  (SQLite)   │  │   Manager   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

### Project Structure

```
AppPreventBurnoutAndOfficeSyndrome/
├── README.md                          # This file
├── HACKATHON_PLAN.md                  # Detailed hackathon plan
├── requirements.txt                   # Python dependencies (includes railtracks)
├── main.py                            # Application entry point
├── railtracks_integration.py          # ⭐ Railtracks agent & function nodes
├── config/
│   ├── settings.py                    # App settings
│   └── prompts.py                     # AI system prompts
├── agents/                            # Traditional agent wrappers
│   ├── wellness_companion_agent.py    # Integrates with Railtracks
│   ├── stretch_coach_agent.py         # Integrates with Railtracks
│   └── break_scheduler_agent.py       # Integrates with Railtracks
├── tools/                             # Utility tools
│   ├── database_tools.py              # SQLite operations
│   ├── notification_tools.py          # Desktop notifications
│   └── pose_detection.py              # ⭐ AI pose detection & stretch analysis
├── models/                            # Database models
│   ├── user.py                        # User profile
│   ├── activity.py                    # Activity logs
│   ├── achievement.py                 # Achievements
│   └── pet.py                         # Virtual pet
├── ui/
│   └── app.py                         # Gradio UI (includes AI camera UI)
├── docs/                              # Documentation
│   └── AI_STRETCH_GUIDE.md            # AI stretch guidance user guide
└── data/                              # Static data
    ├── stretches.json                 # Stretch library
    ├── achievements.json              # Achievement definitions
    └── wellness_resources.json        # Help resources
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **pip** (Python package manager)
- **Claude API Key** (from [Anthropic](https://console.anthropic.com/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Richyboy170/AppPreventBurnoutAndOfficeSyndrome.git
cd AppPreventBurnoutAndOfficeSyndrome
```

2. **Install dependencies** (includes Railtracks)
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. **Run the application**
```bash
python main.py
```

The app will start on `http://localhost:7860`

### Command Line Options

```bash
python main.py --port 8080        # Custom port
python main.py --share            # Create public share link
python main.py --debug            # Run in debug mode
```

---

## 💡 Features Walkthrough

### 1. Wellness Companion (AI Chat)

**What it does:**
- Provides empathetic emotional support 24/7
- Detects stress levels from your messages
- Offers personalized wellness advice based on your activity history
- Remembers context across conversations

**Powered by Railtracks:**
- Uses `wellness_companion_agent` agent node
- Integrates `detect_stress_level` function node for deep analysis
- Accesses your complete wellness profile for personalized responses

**Try it:**
1. Go to "Wellness Companion" tab
2. Click "Start New Conversation"
3. Share how you're feeling or ask for advice
4. The AI will provide empathetic support with actionable suggestions

### 2. Smart Break Management

**What it does:**
- Schedules breaks based on ultradian rhythms (90-minute cycles)
- Avoids interrupting meetings (calendar integration coming soon)
- Learns your break preferences over time
- Awards points for consistent break-taking

**Powered by Railtracks:**
- Uses `break_scheduler_agent` agent node
- Calls `analyze_work_pattern` to optimize timing
- Provides reasoning for why now is a good time for a break

**Try it:**
1. Navigate to "Breaks" tab
2. Click "I Took a Break!" when you take a break
3. Earn 10 points and keep your virtual pet healthy
4. View your break history and patterns

### 3. Guided Stretching with AI Camera Guidance

**What it does:**
- 15+ professionally designed stretches
- Categories: Neck, Shoulders, Back, Wrists, Hips, Legs, Eyes
- Step-by-step instructions with timing
- Pre-built routines for different needs
- **NEW**: Real-time pose detection and form feedback using your camera
- **NEW**: Earn bonus points (up to +20) for perfect form
- **NEW**: Visual overlay showing your body position and form score

**Powered by Railtracks & MediaPipe:**
- Uses `stretch_coaching_agent` for personalized routines
- Calls `generate_personalized_routine` based on your pain points
- Adapts difficulty to your fitness level automatically
- MediaPipe Pose for real-time body tracking (33 landmarks)
- AI analysis of joint angles and body positioning

**Try it:**
1. Go to "Stretches" tab
2. Choose "AI Camera Guidance" tab (install MediaPipe first: `pip install mediapipe`)
3. Browse stretches and note a stretch ID (e.g., `neck_side_stretch`)
4. Enter the stretch ID and click "Start AI Session"
5. Position yourself in front of the camera
6. Follow real-time feedback to perfect your form
7. Complete the stretch and earn base points + bonus for good form!

**Manual Entry:**
1. Go to "Stretches" tab → "Manual Entry"
2. Click "Show Available Stretches"
3. Choose a stretch (e.g., `neck_side_stretch`)
4. Complete the stretch and earn 20 points

📖 **For detailed AI stretch guidance instructions, see [docs/AI_STRETCH_GUIDE.md](docs/AI_STRETCH_GUIDE.md)**

### 4. Gamification System

**What it does:**
- **Points**: Earn points for wellness activities
  - Break: 10 points
  - Stretch: 20 points
  - Chat: 5 points
- **Achievements**: 30+ achievements to unlock
- **Streaks**: Build daily wellness habits
- **Virtual Pet**: A companion that grows with your wellness journey

**Try it:**
1. Check "Stats" tab for your dashboard
2. View "Achievements" tab for unlocked achievements
3. Monitor your pet's health and happiness
4. Build your daily streak

---

## 🎮 How to Use

### First Time Setup

1. Open the app in your browser (`http://localhost:7860`)
2. Go to "Setup" tab
3. Enter your username
4. Click "Start My Wellness Journey"
5. Your virtual pet hatches!

### Daily Workflow

```
Morning:
  → Open the app
  → Check in with wellness companion
  → See your pet's greeting

Work Session:
  → Work for ~45-90 minutes
  → Receive break suggestion (powered by Railtracks)
  → Take a break → Log it → Earn points

Break Time:
  → Choose a stretch from AI-generated routine
  → Follow step-by-step instructions
  → Complete stretch → Earn more points

Feeling Stressed:
  → Open wellness companion chat
  → Share what's bothering you
  → Receive AI-powered support and recommendations

End of Day:
  → Review your stats
  → Check achievements
  → See your pet grow happier and healthier
```

---

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Required
ANTHROPIC_API_KEY=your_key_here

# Optional Customization
DEFAULT_BREAK_INTERVAL=45              # Break interval in minutes
GRADIO_SERVER_PORT=7860                # Web interface port
DATABASE_PATH=./data/wellness.db       # SQLite database location
POINTS_PER_BREAK=10                    # Points for each break
POINTS_PER_STRETCH=20                  # Points for each stretch
POINTS_PER_CHAT=5                      # Points for each chat

# AI Settings
CLAUDE_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=2048
TEMPERATURE=0.7
MAX_CONVERSATION_HISTORY=20
```

---

## 🧪 Testing Railtracks Integration

To verify Railtracks is working correctly:

```python
# In Python console
from railtracks_integration import get_railtracks_info

info = get_railtracks_info()
print(info)

# Should output:
# {
#   'available': True,
#   'agent_nodes': ['wellness_companion_agent', ...],
#   'function_nodes': ['analyze_work_pattern', ...],
#   'tool_nodes': ['send_break_notification', ...]
# }
```

---

## 📊 Database Schema

Uses SQLite for data persistence:

- **users**: User profiles and preferences
- **activities**: Activity logs (breaks, stretches, chats)
- **conversations**: Chat history with AI companion
- **achievements**: Achievement definitions and unlocks
- **pets**: Virtual pet state

Database location: `./data/wellness.db`

---

## 🌟 Why This Project Stands Out

### 1. Real-World Problem
Addresses the $190B burnout crisis with a practical, engaging solution

### 2. Sophisticated AI Architecture
Uses Railtracks to build composable, maintainable AI agents instead of monolithic functions

### 3. Multi-Modal Wellness Approach
Combines physical health (stretches), mental health (companion), and habit formation (gamification)

### 4. Science-Based Design
- **Ultradian rhythms**: 90-minute work cycles
- **Habit formation**: 66-day tracking based on research
- **Micro-breaks**: Evidence-based effectiveness

### 5. Privacy-First
- Local SQLite database
- No cloud requirement
- User data stays on their machine

---

## 🛠️ Development

### Running in Debug Mode
```bash
python main.py --debug
```

### Adding New Railtracks Nodes

**Function Node Example:**
```python
@rt.function_node
def my_new_function(param1: str, param2: int) -> Dict:
    """Your function that does one thing well."""
    # Implementation
    return result
```

**Agent Node Example:**
```python
@rt.agent_node
def my_new_agent(user_id: int, context: Dict) -> Dict:
    """Your agent that orchestrates multiple functions."""
    result1 = my_function_node_1(...)
    result2 = my_function_node_2(...)
    return combined_result
```

### Running Tests
```bash
# When tests are implemented
python -m pytest tests/
```

---

## 📚 Resources & References

### Scientific Backing
- **Ultradian rhythms**: Rossi, E. L. (1991). The 20-minute break
- **Habit formation**: Lally et al. (2010). How habits are formed (66 days)
- **Micro-breaks**: Albulescu et al. (2022). Effectiveness of microbreaks

### Stretch Library Sources
- American Physical Therapy Association (APTA) guidelines
- Mayo Clinic desk exercise recommendations
- Office ergonomics best practices

### Technologies
- [Claude AI](https://www.anthropic.com/claude) by Anthropic
- [Railtracks](https://github.com/anthropics/railtracks) - Agentic framework
- [Gradio](https://gradio.app/) - UI framework
- [MediaPipe](https://google.github.io/mediapipe/) - AI pose detection
- [OpenCV](https://opencv.org/) - Computer vision
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM

---

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [Claude AI](https://www.anthropic.com/claude) by Anthropic
- Powered by [Railtracks](https://github.com/anthropics/railtracks) agentic framework
- UI powered by [Gradio](https://gradio.app/)
- Stretch routines based on APTA and Mayo Clinic guidelines
- Habit formation research by Lally et al. (2010)

---

## 💬 Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/Richyboy170/AppPreventBurnoutAndOfficeSyndrome/issues)
- Check the [Hackathon Plan](HACKATHON_PLAN.md) for detailed architecture

---

## ⭐ Key Railtracks Highlights

This project demonstrates:

✅ **3 Agent Nodes** - Complex orchestration agents
✅ **4 Function Nodes** - Specialized AI-powered functions
✅ **2 Tool Nodes** - External integrations
✅ **Composable Architecture** - Nodes work together seamlessly
✅ **Real-World Application** - Solves actual burnout problems
✅ **Privacy-First Design** - Local-first with optional cloud
✅ **Production-Ready Patterns** - Error handling, fallbacks, monitoring

---

**Remember: Your wellbeing matters. Take breaks, stretch often, and be kind to yourself!** 🌟

---

*Built for the Anthropic Hackathon - Showcasing Railtracks Agentic Framework*
