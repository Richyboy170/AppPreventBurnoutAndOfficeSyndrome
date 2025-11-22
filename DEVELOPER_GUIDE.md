# 🛠️ Developer Guide

This guide will help you set up, install, and develop the Burnout & Office Syndrome Prevention App.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Development Workflow](#development-workflow)
6. [Project Structure](#project-structure)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)

---

## 🎯 Quick Reference Commands

```bash
# Setup
python -m venv venv
source venv/Scripts/activate
 #or source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# Run
python main.py                    # Default
python main.py --debug           # Debug mode
python main.py --port 8080       # Custom port
python main.py --share           # Public link

# Development
python -m pytest tests/          # Run tests
python -m pytest tests/ -v       # Verbose
python main.py --debug           # Hot reload

# Git workflow
git checkout -b feature/my-feature
git add .
git commit -m "feat: description"
git push origin feature/my-feature
```

---

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required

- **Python 3.11 or higher**
  ```bash
  # Check your Python version
  python --version
  # or
  python3 --version
  ```

- **pip** (Python package manager)
  ```bash
  # Check pip version
  pip --version
  ```

- **Git**
  ```bash
  # Check Git version
  git --version
  ```

- **Anthropic API Key**
  - Sign up at [Anthropic Console](https://console.anthropic.com/)
  - Navigate to API Keys section
  - Generate a new API key
  - Keep it secure - you'll need it during setup

### Optional (for full features)

- **Google Calendar API credentials** (for calendar integration)
- **Virtual environment tool** (recommended: venv, virtualenv, or conda)

---

## 📥 Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Richyboy170/AppPreventBurnoutAndOfficeSyndrome.git

# Navigate to the project directory
cd AppPreventBurnoutAndOfficeSyndrome
```

### Step 2: Create a Virtual Environment (Recommended)

Using a virtual environment helps isolate project dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
source venv/Scripts/activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all required dependencies
pip install -r requirements.txt
```

This will install:
- **anthropic** - Claude AI SDK
- **railtracks** - Agentic framework
- **gradio** - Web UI framework
- **sqlalchemy** - Database ORM
- **apscheduler** - Task scheduling
- **plyer** - Desktop notifications
- And more...

### Step 4: Verify Installation

```bash
# Check if key packages are installed
python -c "import anthropic; print('Anthropic SDK:', anthropic.__version__)"
python -c "import gradio; print('Gradio:', gradio.__version__)"
python -c "import railtracks; print('Railtracks installed')"
```

---

## ⚙️ Configuration

### Step 1: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

### Step 2: Edit .env File

Open `.env` in your favorite text editor and configure:

```env
# Required: Your Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-api-key-here

# Database Configuration (default is fine)
DATABASE_PATH=./data/wellness.db

# Storage Paths (default is fine)
PHOTO_STORAGE_PATH=./data/photos
USER_DATA_PATH=./data/user_data

# Application Settings
DEBUG_MODE=false
LOG_LEVEL=INFO

# Break Reminder Settings (in minutes)
DEFAULT_BREAK_INTERVAL=45
MIN_BREAK_INTERVAL=30
MAX_BREAK_INTERVAL=90

# UI Settings
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
SHARE_GRADIO=false

# Gamification Settings
POINTS_PER_BREAK=10
POINTS_PER_STRETCH=20
POINTS_PER_CHAT=5
```

### Step 3: Create Required Directories

The app will create these automatically, but you can create them manually:

```bash
# Create data directories
mkdir -p data/photos
mkdir -p data/user_data

# Verify directory structure
ls -la data/
```

### Optional: Google Calendar Integration

If you want calendar integration:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Download credentials as `credentials.json`
6. Place in `./data/credentials.json`
7. Update `.env`:
   ```env
   GOOGLE_CALENDAR_CREDENTIALS_PATH=./data/credentials.json
   ```

---

## 🚀 Running the Application

### Basic Usage

```bash
# Run with default settings
python main.py
```

The app will start at `http://localhost:7860`

### Command Line Options

```bash
# Run on a different port
python main.py --port 8080

# Run with debug mode enabled
python main.py --debug

# Create a public share link (via Gradio)
python main.py --share

# Bind to specific host
python main.py --host 127.0.0.1

# Combine multiple options
python main.py --port 8080 --debug --share
```

### Expected Output

When you run the app, you should see:

```
============================================================
🌟 Burnout & Office Syndrome Prevention App
============================================================
Starting server on 0.0.0.0:7860
Database: ./data/wellness.db
Data directory: ./data
============================================================
Ready! Open your browser to start your wellness journey! 🚀
============================================================

Running on local URL:  http://0.0.0.0:7860
```

### Accessing the Application

1. Open your web browser
2. Navigate to `http://localhost:7860`
3. You should see the Gradio UI with multiple tabs

---

## 💻 Development Workflow

### Setting Up Your Development Environment

1. **Install development dependencies** (if you add them later):
   ```bash
   pip install pytest black flake8 mypy
   ```

2. **Configure your IDE/Editor**:
   - **VS Code**: Install Python extension
   - **PyCharm**: Configure Python interpreter to use your venv
   - **Vim/Neovim**: Set up Python LSP

### Code Structure Overview

```
AppPreventBurnoutAndOfficeSyndrome/
├── main.py                           # Entry point
├── railtracks_integration.py         # Railtracks agents & nodes
├── config/
│   ├── __init__.py
│   ├── settings.py                   # App configuration
│   └── prompts.py                    # AI system prompts
├── agents/                           # Agent implementations
│   ├── __init__.py
│   ├── wellness_companion_agent.py
│   ├── stretch_coach_agent.py
│   └── break_scheduler_agent.py
├── models/                           # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── activity.py
│   ├── achievement.py
│   └── pet.py
├── tools/                            # Utility tools
│   ├── __init__.py
│   ├── database_tools.py
│   └── notification_tools.py
├── ui/
│   ├── __init__.py
│   └── app.py                        # Gradio UI
├── data/                             # Static data & database
│   ├── stretches.json
│   ├── achievements.json
│   └── wellness_resources.json
└── tests/                            # Test files
    ├── __init__.py
    └── test_agents.py
```

### Making Changes

#### 1. Modifying Railtracks Agents

Edit `railtracks_integration.py`:

```python
# Example: Adding a new function node
@rt.function_node
def my_custom_function(param: str) -> Dict[str, Any]:
    """
    Your custom function that does something useful.

    Args:
        param: Description of parameter

    Returns:
        Dict with results
    """
    # Your implementation
    return {"result": "success"}
```

#### 2. Adding New Stretches

Edit `data/stretches.json`:

```json
{
  "stretch_id": "my_new_stretch",
  "name": "My New Stretch",
  "category": "neck",
  "difficulty": "beginner",
  "duration": 30,
  "instructions": [
    "Step 1: Do this",
    "Step 2: Do that"
  ],
  "benefits": ["Reduces tension", "Improves mobility"]
}
```

#### 3. Modifying the UI

Edit `ui/app.py` to change the Gradio interface:

```python
# Example: Adding a new tab
with gr.Tab("My New Feature"):
    gr.Markdown("## My New Feature")
    # Add your components
```

#### 4. Updating Database Models

Edit files in `models/` directory:

```python
# Example: Adding a field to User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    # Add your new field
    new_field = Column(String, default="")
```

After modifying models, you may need to recreate the database or write migrations.

### Hot Reload Development

Gradio supports hot reload in debug mode:

```bash
python main.py --debug
```

Changes to UI will auto-reload. For agent changes, you may need to restart.

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_agents.py

# Run with coverage
python -m pytest tests/ --cov=.
```

### Manual Testing Checklist

Test these features manually:

- [ ] **User Setup**
  - [ ] Create new user
  - [ ] Virtual pet hatches

- [ ] **Wellness Companion**
  - [ ] Start new conversation
  - [ ] Send message and receive response
  - [ ] Stress level detection works

- [ ] **Breaks**
  - [ ] Log a break
  - [ ] Points are awarded
  - [ ] Break history updates

- [ ] **Stretches**
  - [ ] View available stretches
  - [ ] Complete a stretch
  - [ ] Points are awarded

- [ ] **Gamification**
  - [ ] Check stats tab
  - [ ] View achievements
  - [ ] Pet health updates

### Testing Railtracks Integration

```python
# In Python REPL or test file
from railtracks_integration import get_railtracks_info

# Verify Railtracks is working
info = get_railtracks_info()
print(info)

# Should show:
# {
#   'available': True,
#   'agent_nodes': [...],
#   'function_nodes': [...],
#   'tool_nodes': [...]
# }
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. API Key Not Set

**Error:**
```
⚠️  Warning: ANTHROPIC_API_KEY not set!
```

**Solution:**
- Check your `.env` file exists
- Verify `ANTHROPIC_API_KEY` is set correctly
- Make sure there are no spaces around the `=` sign
- Restart the application

#### 2. Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
# Ensure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Use a different port
python main.py --port 8080

# Or kill the process using port 7860
# On macOS/Linux:
lsof -ti:7860 | xargs kill -9

# On Windows:
netstat -ano | findstr :7860
taskkill /PID <PID> /F
```

#### 4. Database Errors

**Error:**
```
sqlalchemy.exc.OperationalError: unable to open database file
```

**Solution:**
```bash
# Ensure data directory exists
mkdir -p data

# Check permissions
chmod 755 data

# Delete and recreate database
rm data/wellness.db
python main.py  # Will recreate database
```

#### 5. Railtracks Not Found

**Error:**
```
ModuleNotFoundError: No module named 'railtracks'
```

**Solution:**
```bash
# Install railtracks specifically
pip install railtracks>=0.1.0

# If that fails, check for alternative installation
pip install git+https://github.com/anthropics/railtracks.git
```

### Debug Mode

Run with debug flag for detailed error messages:

```bash
python main.py --debug
```

This will:
- Show detailed stack traces
- Enable Gradio debug mode
- Print more verbose logging

### Checking Logs

Set log level in `.env`:

```env
LOG_LEVEL=DEBUG  # Options: DEBUG, INFO, WARNING, ERROR
```

---

## 🤝 Contributing

### Development Setup for Contributors

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AppPreventBurnoutAndOfficeSyndrome.git
   cd AppPreventBurnoutAndOfficeSyndrome
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Richyboy170/AppPreventBurnoutAndOfficeSyndrome.git
   ```

4. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-awesome-feature
   ```

5. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "Add my awesome feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/my-awesome-feature
   ```

7. **Create a Pull Request** on GitHub

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions focused and small
- Comment complex logic

### Commit Message Format

```
type(scope): brief description

Detailed description if needed

Fixes #issue_number
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(agents): add mood tracking to wellness companion

Implemented mood detection using sentiment analysis
to better track user emotional state over time.

Fixes #42
```

---

## 📚 Additional Resources

### Documentation

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Railtracks Framework](https://github.com/anthropics/railtracks)
- [Gradio Documentation](https://gradio.app/docs/)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org/)

### Project-Specific Docs

- [README.md](README.md) - Overview and features
- [HACKATHON_PLAN.md](HACKATHON_PLAN.md) - Detailed architecture
- `data/stretches.json` - Stretch library
- `data/achievements.json` - Achievement definitions

### Getting Help

- Open an issue on [GitHub Issues](https://github.com/Richyboy170/AppPreventBurnoutAndOfficeSyndrome/issues)
- Check existing issues for solutions
- Join discussions in Pull Requests

---

## 🎯 Quick Reference Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API key

# Run
python main.py                    # Default
python main.py --debug           # Debug mode
python main.py --port 8080       # Custom port
python main.py --share           # Public link

# Development
python -m pytest tests/          # Run tests
python -m pytest tests/ -v       # Verbose
python main.py --debug           # Hot reload

# Git workflow
git checkout -b feature/my-feature
git add .
git commit -m "feat: description"
git push origin feature/my-feature
```

---

## ✅ Installation Checklist

Use this checklist to ensure everything is set up correctly:

- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created and configured
- [ ] Anthropic API key added to `.env`
- [ ] Data directories exist (`data/`)
- [ ] Application runs without errors (`python main.py`)
- [ ] Can access UI at `http://localhost:7860`
- [ ] Can create a user and see virtual pet
- [ ] Wellness companion responds to messages

---

## 💡 Tips for Developers

1. **Use Virtual Environments**: Always work in a virtual environment to avoid dependency conflicts

2. **Check API Usage**: Monitor your Anthropic API usage in the console to avoid unexpected costs

3. **Database Backups**: Backup `data/wellness.db` before making schema changes

4. **Test in Debug Mode**: Use `--debug` flag during development for better error messages

5. **Gradio Interface**: Changes to UI can be tested quickly with hot reload in debug mode

6. **Railtracks Nodes**: Keep agent nodes focused - each should have a single responsibility

7. **Error Handling**: Always add try-catch blocks around AI API calls

8. **Documentation**: Update docstrings when modifying functions

---

**Happy Coding! Build something awesome! 🚀**

---

*Last Updated: 2025-11-22*
