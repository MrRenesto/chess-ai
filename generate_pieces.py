"""
Generate professional-looking chess piece images using Pygame.
Styled similar to chess.com pieces.
"""

import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SIZE = 120  # Larger size for better quality
PADDING = 10

# Colors - more realistic
WHITE = (255, 255, 255)
WHITE_SHADOW = (220, 220, 220)
BLACK = (40, 40, 40)
BLACK_HIGHLIGHT = (60, 60, 60)
TRANSPARENT = (0, 0, 0, 0)

def add_shadow(surface, color_dark):
    """Add a subtle shadow effect."""
    shadow = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    # Draw shadow slightly offset
    return surface

def draw_pawn(surface, color, is_white):
    """Draw a professional pawn."""
    center_x = SIZE // 2
    base_y = SIZE - 15
    
    # Base
    pygame.draw.circle(surface, color, (center_x, base_y), 20, 0)
    pygame.draw.rect(surface, color, (center_x - 18, base_y - 5, 36, 8))
    
    # Stem
    points = [
        (center_x - 12, base_y - 5),
        (center_x - 10, base_y - 40),
        (center_x + 10, base_y - 40),
        (center_x + 12, base_y - 5),
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Head
    pygame.draw.circle(surface, color, (center_x, base_y - 50), 14)
    
    # Highlight
    if is_white:
        pygame.draw.circle(surface, WHITE_SHADOW, (center_x - 4, base_y - 54), 5)

def draw_knight(surface, color, is_white):
    """Draw a professional knight."""
    center_x = SIZE // 2
    base_y = SIZE - 15
    
    # Base
    pygame.draw.ellipse(surface, color, (center_x - 22, base_y - 8, 44, 16))
    
    # Horse head outline
    points = [
        (center_x - 15, base_y - 8),
        (center_x - 18, base_y - 25),
        (center_x - 14, base_y - 45),
        (center_x - 5, base_y - 60),
        (center_x + 8, base_y - 58),
        (center_x + 15, base_y - 48),
        (center_x + 18, base_y - 30),
        (center_x + 12, base_y - 8),
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Eye
    eye_color = BLACK if is_white else WHITE_SHADOW
    pygame.draw.circle(surface, eye_color, (center_x + 2, base_y - 50), 3)
    
    # Ear
    pygame.draw.circle(surface, color, (center_x - 2, base_y - 62), 6)

def draw_bishop(surface, color, is_white):
    """Draw a professional bishop."""
    center_x = SIZE // 2
    base_y = SIZE - 15
    
    # Base
    pygame.draw.ellipse(surface, color, (center_x - 22, base_y - 8, 44, 16))
    
    # Body - tapered
    points = [
        (center_x - 18, base_y - 8),
        (center_x - 14, base_y - 35),
        (center_x - 12, base_y - 55),
        (center_x + 12, base_y - 55),
        (center_x + 14, base_y - 35),
        (center_x + 18, base_y - 8),
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Hat
    pygame.draw.circle(surface, color, (center_x, base_y - 60), 12)
    
    # Top sphere
    pygame.draw.circle(surface, color, (center_x, base_y - 72), 6)
    
    # Slit in hat
    pygame.draw.line(surface, BLACK if is_white else WHITE_SHADOW, 
                     (center_x - 8, base_y - 65), (center_x + 8, base_y - 65), 2)

def draw_rook(surface, color, is_white):
    """Draw a professional rook."""
    center_x = SIZE // 2
    base_y = SIZE - 15
    
    # Base
    pygame.draw.ellipse(surface, color, (center_x - 24, base_y - 8, 48, 16))
    
    # Tower body
    pygame.draw.rect(surface, color, (center_x - 20, base_y - 60, 40, 52))
    
    # Battlements
    pygame.draw.rect(surface, color, (center_x - 24, base_y - 72, 10, 12))
    pygame.draw.rect(surface, color, (center_x - 8, base_y - 72, 10, 12))
    pygame.draw.rect(surface, color, (center_x + 8, base_y - 72, 10, 12))
    pygame.draw.rect(surface, color, (center_x + 14, base_y - 72, 10, 12))
    
    # Add depth to tower
    if is_white:
        pygame.draw.rect(surface, WHITE_SHADOW, (center_x - 18, base_y - 58, 4, 48))

def draw_queen(surface, color, is_white):
    """Draw a professional queen."""
    center_x = SIZE // 2
    base_y = SIZE - 15
    
    # Base
    pygame.draw.ellipse(surface, color, (center_x - 24, base_y - 8, 48, 16))
    
    # Body
    points = [
        (center_x - 20, base_y - 8),
        (center_x - 16, base_y - 40),
        (center_x + 16, base_y - 40),
        (center_x + 20, base_y - 8),
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Crown with 5 points
    crown_base = base_y - 45
    crown_points = [
        (center_x - 18, crown_base),
        (center_x - 14, crown_base - 12),
        (center_x - 9, crown_base - 5),
        (center_x - 4, crown_base - 15),
        (center_x, crown_base - 8),
        (center_x + 4, crown_base - 15),
        (center_x + 9, crown_base - 5),
        (center_x + 14, crown_base - 12),
        (center_x + 18, crown_base),
    ]
    pygame.draw.polygon(surface, color, crown_points)
    
    # Crown balls
    for i, x_offset in enumerate([-14, -4, 4, 14]):
        y_offset = -15 if i in [1, 2] else -12
        pygame.draw.circle(surface, color, (center_x + x_offset, crown_base + y_offset), 4)

def draw_king(surface, color, is_white):
    """Draw a professional king."""
    center_x = SIZE // 2
    base_y = SIZE - 15
    
    # Base
    pygame.draw.ellipse(surface, color, (center_x - 24, base_y - 8, 48, 16))
    
    # Body
    points = [
        (center_x - 20, base_y - 8),
        (center_x - 16, base_y - 45),
        (center_x + 16, base_y - 45),
        (center_x + 20, base_y - 8),
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Crown
    crown_base = base_y - 50
    points = [
        (center_x - 18, crown_base),
        (center_x - 16, crown_base - 8),
        (center_x - 10, crown_base - 4),
        (center_x - 8, crown_base - 10),
        (center_x, crown_base - 6),
        (center_x + 8, crown_base - 10),
        (center_x + 10, crown_base - 4),
        (center_x + 16, crown_base - 8),
        (center_x + 18, crown_base),
    ]
    pygame.draw.polygon(surface, color, points)
    
    # Cross on top
    pygame.draw.rect(surface, color, (center_x - 3, base_y - 78, 6, 20))
    pygame.draw.rect(surface, color, (center_x - 10, base_y - 68, 20, 6))

def generate_piece(name, color, is_white, draw_func):
    """Generate and save a piece image."""
    surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    surface.fill(TRANSPARENT)
    
    # Draw the piece
    draw_func(surface, color, is_white)
    
    # Add border to make pieces stand out
    border_color = BLACK if is_white else WHITE
    border_width = 2
    
    # Create a slightly larger version for the border
    border_surface = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    draw_func(border_surface, border_color, is_white)
    
    # Create final surface with border effect
    final = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    final.fill(TRANSPARENT)
    
    # Draw border by offsetting in 8 directions
    offsets = [(-border_width, -border_width), (0, -border_width), (border_width, -border_width),
               (-border_width, 0), (border_width, 0),
               (-border_width, border_width), (0, border_width), (border_width, border_width)]
    
    for offset_x, offset_y in offsets:
        final.blit(border_surface, (offset_x, offset_y))
    
    # Draw the main piece on top
    final.blit(surface, (0, 0))
    
    # Scale down to final size (100x100) for anti-aliasing effect
    final_surface = pygame.transform.smoothscale(final, (100, 100))
    
    # Create directory if it doesn't exist
    os.makedirs("assets/pieces", exist_ok=True)
    
    # Save
    filename = f"assets/pieces/{name}.png"
    pygame.image.save(final_surface, filename)
    print(f"Generated: {filename}")

def main():
    """Generate all chess pieces."""
    pieces = [
        ("white_pawn", WHITE, True, draw_pawn),
        ("white_knight", WHITE, True, draw_knight),
        ("white_bishop", WHITE, True, draw_bishop),
        ("white_rook", WHITE, True, draw_rook),
        ("white_queen", WHITE, True, draw_queen),
        ("white_king", WHITE, True, draw_king),
        ("black_pawn", BLACK, False, draw_pawn),
        ("black_knight", BLACK, False, draw_knight),
        ("black_bishop", BLACK, False, draw_bishop),
        ("black_rook", BLACK, False, draw_rook),
        ("black_queen", BLACK, False, draw_queen),
        ("black_king", BLACK, False, draw_king),
    ]
    
    print("Generating professional chess pieces...")
    print("Style: Similar to chess.com\n")
    
    for name, color, is_white, draw_func in pieces:
        generate_piece(name, color, is_white, draw_func)
    
    print("\n✓ All pieces generated successfully!")
    print("Pieces are saved in assets/pieces/")
    pygame.quit()

if __name__ == "__main__":
    main()
