"""
Constants and configuration settings for the chess game.
"""

# Window settings
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE  # 100 pixels per square
FPS = 60

# Colors (RGB)
LIGHT_SQUARE = (240, 217, 181)  # Light brown
DARK_SQUARE = (181, 136, 99)    # Dark brown
HIGHLIGHT_COLOR = (186, 202, 68, 128)  # Yellow-green with alpha
CHECK_COLOR = (255, 0, 0, 128)  # Red with alpha
LAST_MOVE_COLOR = (155, 199, 0, 100)  # Light green with alpha
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Board orientation
WHITE_BOTTOM = True  # White pieces at bottom

# File and rank labels
FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']

# Piece symbols
PIECE_SYMBOLS = {
    'P': 'white_pawn', 'N': 'white_knight', 'B': 'white_bishop',
    'R': 'white_rook', 'Q': 'white_queen', 'K': 'white_king',
    'p': 'black_pawn', 'n': 'black_knight', 'b': 'black_bishop',
    'r': 'black_rook', 'q': 'black_queen', 'k': 'black_king',
}

# Asset paths
ASSETS_DIR = "assets"
PIECES_DIR = f"{ASSETS_DIR}/pieces"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
