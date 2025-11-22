"""Application configuration and settings."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "ui" / "assets"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
(DATA_DIR / "photos").mkdir(exist_ok=True)
(DATA_DIR / "user_data").mkdir(exist_ok=True)

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
if not ANTHROPIC_API_KEY:
    print("Warning: ANTHROPIC_API_KEY not set. Please set it in .env file.")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "wellness.db"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Storage Configuration
PHOTO_STORAGE_PATH = Path(os.getenv("PHOTO_STORAGE_PATH", str(DATA_DIR / "photos")))
PHOTO_STORAGE_PATH.mkdir(exist_ok=True)

USER_DATA_PATH = Path(os.getenv("USER_DATA_PATH", str(DATA_DIR / "user_data")))
USER_DATA_PATH.mkdir(exist_ok=True)

# Application Settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Break Reminder Settings (in minutes)
DEFAULT_BREAK_INTERVAL = int(os.getenv("DEFAULT_BREAK_INTERVAL", "45"))
MIN_BREAK_INTERVAL = int(os.getenv("MIN_BREAK_INTERVAL", "30"))
MAX_BREAK_INTERVAL = int(os.getenv("MAX_BREAK_INTERVAL", "90"))

# Calendar Integration
GOOGLE_CALENDAR_API_KEY = os.getenv("GOOGLE_CALENDAR_API_KEY", "")
GOOGLE_CALENDAR_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_CALENDAR_CREDENTIALS_PATH",
    str(DATA_DIR / "credentials.json")
)

# UI Settings
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
SHARE_GRADIO = os.getenv("SHARE_GRADIO", "false").lower() == "true"

# Gamification Settings
POINTS_PER_BREAK = int(os.getenv("POINTS_PER_BREAK", "10"))
POINTS_PER_STRETCH = int(os.getenv("POINTS_PER_STRETCH", "20"))
POINTS_PER_CHAT = int(os.getenv("POINTS_PER_CHAT", "5"))

# Claude Model Settings
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# Vision API Settings
VISION_MODEL = "claude-3-5-sonnet-20241022"
VISION_MAX_TOKENS = 1024

# Stretch Verification Settings
MIN_VERIFICATION_CONFIDENCE = 0.6  # Minimum confidence to accept stretch verification

# Pet Settings
PET_HEALTH_DECAY_RATE = 5  # Health points lost per day without activity
PET_HAPPINESS_DECAY_RATE = 3  # Happiness points lost per day without activity
PET_HEALTH_GAIN_PER_BREAK = 10
PET_HAPPINESS_GAIN_PER_STRETCH = 15
PET_XP_PER_ACTIVITY = 20

# Habit Formation Settings
HABIT_FORMATION_DAYS = 66  # Research-based habit formation period
GRACE_PERIOD_HOURS = 24  # Hours allowed before streak is broken

# Wellness Companion Settings
MAX_CONVERSATION_HISTORY = 50  # Number of messages to keep in context
STRESS_LEVEL_THRESHOLD = 7  # Trigger intervention at this stress level (1-10)

# Notification Settings
NOTIFICATION_ENABLED = True
NOTIFICATION_SOUND = True
NOTIFICATION_DURATION = 10  # seconds

# Data Privacy Settings
STORE_PHOTOS = True  # Whether to store stretch verification photos
PHOTO_RETENTION_DAYS = 30  # Days to keep photos before auto-deletion
ALLOW_ANALYTICS = False  # Anonymous usage analytics
