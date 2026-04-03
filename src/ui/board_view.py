"""
Board rendering - draws the chess board.
"""

import pygame
import chess
from utils.constants import (
    WINDOW_SIZE, BOARD_SIZE, SQUARE_SIZE,
    LIGHT_SQUARE, DARK_SQUARE, FILES, RANKS
)


class BoardView:
    """Renders the chess board."""
    
    def __init__(self, screen, size=WINDOW_SIZE):
        """
        Initialize the board view.
        
        Args:
            screen: Pygame screen surface
            size: Size of the board in pixels
        """
        self.screen = screen
        self.size = size
        self.square_size = size // BOARD_SIZE
        self.board_offset_x = 0
        self.board_offset_y = 0
    
    def draw_board(self):
        """Draw the chess board with alternating squares."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Determine square color (alternating pattern)
                is_light = (row + col) % 2 == 0
                color = LIGHT_SQUARE if is_light else DARK_SQUARE
                
                # Calculate square position
                x = col * self.square_size + self.board_offset_x
                y = row * self.square_size + self.board_offset_y
                
                # Draw square
                rect = pygame.Rect(x, y, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_coordinates(self, font_size=16):
        """
        Draw file and rank labels around the board.
        
        Args:
            font_size: Size of the coordinate font
        """
        font = pygame.font.Font(None, font_size)
        
        for i in range(BOARD_SIZE):
            # Draw file labels (a-h) at bottom
            file_label = font.render(FILES[i], True, (0, 0, 0))
            x = i * self.square_size + self.square_size - 12
            y = self.size - 12
            self.screen.blit(file_label, (x, y))
            
            # Draw rank labels (1-8) on left side
            rank_label = font.render(RANKS[7 - i], True, (0, 0, 0))
            x = 2
            y = i * self.square_size + 2
            self.screen.blit(rank_label, (x, y))
    
    def pixel_to_square(self, pixel_x, pixel_y):
        """
        Convert pixel coordinates to chess square.
        
        Args:
            pixel_x: X coordinate in pixels
            pixel_y: Y coordinate in pixels
        
        Returns:
            int or None: Chess square (0-63) or None if outside board
        """
        # Adjust for board offset
        x = pixel_x - self.board_offset_x
        y = pixel_y - self.board_offset_y
        
        # Check if within board bounds
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return None
        
        # Calculate file and rank
        file = x // self.square_size
        rank = 7 - (y // self.square_size)  # Flip rank (bottom = 0, top = 7)
        
        # Convert to chess square (0-63)
        return chess.square(file, rank)
    
    def square_to_pixel(self, square):
        """
        Convert chess square to pixel coordinates (center of square).
        
        Args:
            square: Chess square (0-63)
        
        Returns:
            tuple: (x, y) pixel coordinates of square center
        """
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        # Calculate pixel position (center of square)
        x = file * self.square_size + self.square_size // 2 + self.board_offset_x
        y = (7 - rank) * self.square_size + self.square_size // 2 + self.board_offset_y
        
        return (x, y)
    
    def get_square_rect(self, square):
        """
        Get the pygame Rect for a chess square.
        
        Args:
            square: Chess square (0-63)
        
        Returns:
            pygame.Rect: Rectangle for the square
        """
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        x = file * self.square_size + self.board_offset_x
        y = (7 - rank) * self.square_size + self.board_offset_y
        
        return pygame.Rect(x, y, self.square_size, self.square_size)
    
    def highlight_square(self, square, color):
        """
        Highlight a square with a color overlay.
        
        Args:
            square: Chess square (0-63)
            color: RGB or RGBA tuple
        """
        rect = self.get_square_rect(square)
        
        # Create a surface with alpha for transparency
        if len(color) == 4:
            surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            surface.fill(color)
            self.screen.blit(surface, rect.topleft)
        else:
            pygame.draw.rect(self.screen, color, rect, 3)  # Draw border
    
    def highlight_squares(self, squares, color):
        """
        Highlight multiple squares.
        
        Args:
            squares: List of chess squares (0-63)
            color: RGB or RGBA tuple
        """
        for square in squares:
            self.highlight_square(square, color)
