"""
Samsung S25 optimiertes Darkmode-Theme für Kivy-Komponenten.
Fokus auf AMOLED, klare Kontraste, große Buttons und modernes Touchgefühl.
"""
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

# Allgemeine Farben
COLOR_BG = get_color_from_hex("#121212")
COLOR_ACCENT = get_color_from_hex("#2196F3")
COLOR_TEXT = (1, 1, 1, 1)
COLOR_HINT = (.7, .7, .7, 1)
COLOR_BUTTON = get_color_from_hex("#1E88E5")
COLOR_USER = get_color_from_hex("#0D47A1")
COLOR_AI = get_color_from_hex("#2E7D32")

# Allgemeine UI-Anpassung
Window.clearcolor = COLOR_BG
Window.softinput_mode = "below_target"

# Globale Maße
PADDING = dp(12)
BUBBLE_WIDTH = 0.88
FONT_SIZE = "16sp"
CORNER_RADIUS = dp(16)

# Export für andere Komponenten
__all__ = [
    "COLOR_BG", "COLOR_ACCENT", "COLOR_TEXT", "COLOR_HINT",
    "COLOR_BUTTON", "COLOR_USER", "COLOR_AI",
    "PADDING", "BUBBLE_WIDTH", "FONT_SIZE", "CORNER_RADIUS"
]
