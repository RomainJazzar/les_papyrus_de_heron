# config.py
import pygame
import os

# --- Core Settings ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# --- Asset Paths ---
# Use os.path.join for cross-platform compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Gets the directory where config.py is
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# --- Colors ---
# Basic Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (211, 211, 211)

# Highlight Colors (can be overridden by theme)
DEFAULT_HIGHLIGHT_COLOR = (0, 255, 0, 150) # Green semi-transparent
DEFAULT_SWAP_COLOR = (255, 0, 0, 150)     # Red semi-transparent

# --- Themes ---
# Dictionary to hold theme settings
THEMES = {
    'egyptian': {
        'background': (210, 180, 140), # Tan/Dark Sand
        'bars': (244, 164, 96),        # Sand
        'text': BLACK,
        'highlight': DEFAULT_HIGHLIGHT_COLOR,
        'swap': DEFAULT_SWAP_COLOR,
        'background_image': os.path.join(IMAGES_DIR, 'background_egyptian.png'), # Optional
        'font': os.path.join(FONTS_DIR, 'Papyrus.ttf') # Optional custom font path
    },
    'futuristic': {
        'background': (10, 10, 40),     # Dark Blue
        'bars': (0, 200, 255),         # Cyan
        'text': (200, 200, 255),       # Light Blue/White
        'highlight': (0, 255, 0, 180),  # Brighter Green
        'swap': (255, 0, 255, 180),    # Magenta
        'background_image': os.path.join(IMAGES_DIR, 'background_futuristic.png'), # Optional
        'font': os.path.join(FONTS_DIR, 'Orbitron-Regular.ttf') # Optional custom font path
    },
    'natural': {
        'background': (34, 139, 34),    # Forest Green
        'bars': (160, 82, 45),         # Sienna (Wood)
        'text': WHITE,
        'highlight': (255, 255, 0, 150), # Yellow
        'swap': (255, 69, 0, 150),     # Orange-Red
        'background_image': os.path.join(IMAGES_DIR, 'background_natural.png'), # Optional
        'font': None # Use default font
    }
    # Add more themes here
}

# --- Font Settings ---
# Attempt to load themed font or fallback to default
def get_font_path(theme_name, default_font=None):
    """Gets the font path for the theme, or returns None for default."""
    theme_font = THEMES.get(theme_name, {}).get('font', None)
    if theme_font and os.path.exists(theme_font):
        return theme_font
    # Could add more fallbacks here (e.g., specific default font path)
    return default_font # None tells Pygame to use its default

DEFAULT_TITLE_FONT_SIZE = 74
DEFAULT_UI_FONT_SIZE = 36
DEFAULT_STATS_FONT_SIZE = 28

# --- Sound Settings ---
# Dictionary of sound file paths
SOUNDS = {
    'compare': os.path.join(SOUNDS_DIR, 'compare.wav'),
    'swap': os.path.join(SOUNDS_DIR, 'swap.wav'),
    'done': os.path.join(SOUNDS_DIR, 'done.mp3'),
    'click': os.path.join(SOUNDS_DIR, 'click.wav')
}

# Sound Volume (0.0 to 1.0)
VOLUME_COMPARE = 0.3
VOLUME_SWAP = 0.5
VOLUME_DONE = 0.7
VOLUME_CLICK = 0.6

# --- Visualization Settings ---
# Area dedicated to visualization (adjust as needed)
VISUALIZATION_AREA_Y_START = 60
VISUALIZATION_AREA_HEIGHT_RATIO = 0.7 # 70% of screen height below start Y
STATS_AREA_HEIGHT = 120 # Space at the bottom for stats and controls

# Bar visualization specifics
BAR_WIDTH_RATIO = 0.9 # Use 90% of screen width for bars total
BAR_SPACING = 2 # Pixels between bars

# Circle visualization specifics
CIRCLE_RADIUS_RATIO = 0.35 # Max radius as fraction of min(screen_width, screen_height)
CIRCLE_CENTER_Y_OFFSET = -50 # Move center up a bit from screen center
CIRCLE_POINT_RADIUS = 5
CIRCLE_HIGHLIGHT_RADIUS = 8
CIRCLE_HIGHLIGHT_WIDTH = 2

# --- Sorting Parameters ---
DEFAULT_LIST_SIZE = 50
DEFAULT_MIN_VAL = 0.0
DEFAULT_MAX_VAL = 100.0
DEFAULT_DISORDER_TYPE = 'random'

LIST_SIZE_OPTIONS = {
    "Petite": 20,
    "Moyenne": 50,
    "Grande": 100,
    "Très Grande": 250 # Adjust based on performance
}

DISORDER_OPTIONS = ['random', 'nearly_sorted', 'reversed', 'sorted'] # Added 'sorted'