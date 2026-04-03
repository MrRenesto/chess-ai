"""
Generate simple chess piece images using Pygame.
"""

import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SIZE = 100
PADDING = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
TRANSPARENT = (0, 0, 0, 0)

def draw_pawn(surface, color):
    """Draw a pawn."""
    center_x = SIZE // 2
    # Body
    pygame.draw.circle(surface, color, (center_x, SIZE - 30), 12)
    pygame.draw.rect(surface, color, (center_x - 8, SIZE - 40, 16, 15))
    # Head
    pygame.draw.circle(surface, color, (center_x, SIZE - 50), 10)

def draw_knight(surface, color):
    """Draw a knight."""
    center_x = SIZE // 2
    points = [
        (center_x - 10, SIZE - 20),
        (center_x - 15, SIZE - 40),
        (center_x - 5, SIZE - 60),
        (center_x + 10, SIZE - 55),
        (center_x + 15, SIZE - 35),
        (center_x + 10, SIZE - 20),
    ]
    pygame.draw.polygon(surface, color, points)
    pygame.draw.circle(surface, color, (center_x + 5, SIZE - 50), 5)

def draw_bishop(surface, color):
    """Draw a bishop."""
    center_x = SIZE // 2
    # Base
    pygame.draw.rect(surface, color, (center_x - 12, SIZE - 25, 24, 10))
    # Body
    points = [
        (center_x - 10, SIZE - 25),
        (center_x - 8, SIZE - 50),
        (center_x + 8, SIZE - 50),
        (center_x + 10, SIZE - 25),
    ]
    pygame.draw.polygon(surface, color, points)
    # Top
    pygame.draw.circle(surface, color, (center_x, SIZE - 55), 8)
    pygame.draw.circle(surface, color, (center_x, SIZE - 65), 4)

def draw_rook(surface, color):
    """Draw a rook."""
    center_x = SIZE // 2
    # Base
    pygame.draw.rect(surface, color, (center_x - 15, SIZE - 25, 30, 10))
    # Body
    pygame.draw.rect(surface, color, (center_x - 12, SIZE - 55, 24, 30))
    # Top battlements
    pygame.draw.rect(surface, color, (center_x - 15, SIZE - 65, 8, 10))
    pygame.draw.rect(surface, color, (center_x - 4, SIZE - 65, 8, 10))
    pygame.draw.rect(surface, color, (center_x + 7, SIZE - 65, 8, 10))

def draw_queen(surface, color):
    """Draw a queen."""
    center_x = SIZE // 2
    # Base
    pygame.draw.rect(surface, color, (center_x - 15, SIZE - 25, 30, 10))
    # Body
    points = [
        (center_x - 12, SIZE - 25),
        (center_x - 10, SIZE - 50),
        (center_x + 10, SIZE - 50),
        (center_x + 12, SIZE - 25),
    ]
    pygame.draw.polygon(surface, color, points)
    # Crown
    pygame.draw.circle(surface, color, (center_x - 8, SIZE - 55), 4)
    pygame.draw.circle(surface, color, (center_x, SIZE - 60), 5)
    pygame.draw.circle(surface, color, (center_x + 8, SIZE - 55), 4)

def draw_king(surface, color):
    """Draw a king."""
    center_x = SIZE // 2
    # Base
    pygame.draw.rect(surface, color, (center_x - 15, SIZE - 25, 30, 10))
    # Body
    points = [
        (center_x - 12, SIZE - 25),
        (center_x - 10, SIZE - 50),
        (center_x + 10, SIZE - 50),
        (center_x + 12, SIZE - 25),
    ]
    pygame.draw.polygon(surface, color, points)
    # Cross
    pygame.draw.rect(surface, color, (center_x - 2, SIZE - 70, 4, 20))
    pygame.draw.rect(surface, color, (center_x - 8, SIZE - 58, 16, 4))

def generate_piece(name, color, draw_func):
    """Generate and save a piece image."""
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    draw_func(surface, color)
    
    # Create directory if it doesn't exist
    os.makedirs("assets/pieces", exist_ok=True)
    
    # Save
    filename = f"assets/pieces/{name}.png"
    pygame.image.save(surface, filename)
    print(f"Generated: {filename}")

def main():
    """Generate all chess pieces."""
    pieces = [
        ("white_pawn", WHITE, draw_pawn),
        ("white_knight", WHITE, draw_knight),
        ("white_bishop", WHITE, draw_bishop),
        ("white_rook", WHITE, draw_rook),
        ("white_queen", WHITE, draw_queen),
        ("white_king", WHITE, draw_king),
        ("black_pawn", BLACK, draw_pawn),
        ("black_knight", BLACK, draw_knight),
        ("black_bishop", BLACK, draw_bishop),
        ("black_rook", BLACK, draw_rook),
        ("black_queen", BLACK, draw_queen),
        ("black_king", BLACK, draw_king),
    ]
    
    for name, color, draw_func in pieces:
        generate_piece(name, color, draw_func)
    
    print("\nAll pieces generated successfully!")
    pygame.quit()

if __name__ == "__main__":
    main()
