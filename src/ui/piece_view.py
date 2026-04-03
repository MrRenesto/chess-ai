"""
Piece rendering - loads and displays chess pieces.
"""

import pygame
import chess
from pathlib import Path


class PieceView:
    """Renders chess pieces on the board."""
    
    def __init__(self, screen, square_size=100):
        """
        Initialize the piece view.
        
        Args:
            screen: Pygame screen surface
            square_size: Size of each square in pixels
        """
        self.screen = screen
        self.square_size = square_size
        self.piece_images = {}
        self._load_piece_images()
    
    def _load_piece_images(self):
        """Load chess piece images from assets folder."""
        # Piece mapping: chess piece symbol -> filename
        piece_files = {
            'P': 'white_pawn',
            'N': 'white_knight',
            'B': 'white_bishop',
            'R': 'white_rook',
            'Q': 'white_queen',
            'K': 'white_king',
            'p': 'black_pawn',
            'n': 'black_knight',
            'b': 'black_bishop',
            'r': 'black_rook',
            'q': 'black_queen',
            'k': 'black_king',
        }
        
        assets_path = Path("assets/pieces")
        
        for symbol, filename in piece_files.items():
            image_path = assets_path / f"{filename}.png"
            
            if image_path.exists():
                # Load and scale image
                image = pygame.image.load(str(image_path))
                image = pygame.transform.smoothscale(
                    image, 
                    (self.square_size, self.square_size)
                )
                self.piece_images[symbol] = image
            else:
                # Create placeholder if image doesn't exist
                self.piece_images[symbol] = self._create_placeholder(symbol)
    
    def _create_placeholder(self, piece_symbol):
        """
        Create a placeholder image for a piece.
        
        Args:
            piece_symbol: Chess piece symbol (e.g., 'P', 'n')
        
        Returns:
            pygame.Surface: Placeholder image
        """
        surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        
        # Determine color
        is_white = piece_symbol.isupper()
        color = (255, 255, 255) if is_white else (0, 0, 0)
        border_color = (0, 0, 0) if is_white else (255, 255, 255)
        
        # Draw circle as placeholder
        center = self.square_size // 2
        radius = self.square_size // 3
        pygame.draw.circle(surface, color, (center, center), radius)
        pygame.draw.circle(surface, border_color, (center, center), radius, 2)
        
        # Draw piece letter
        font = pygame.font.Font(None, self.square_size // 2)
        text = font.render(piece_symbol.upper(), True, border_color)
        text_rect = text.get_rect(center=(center, center))
        surface.blit(text, text_rect)
        
        return surface
    
    def draw_piece(self, piece, position):
        """
        Draw a piece at a pixel position.
        
        Args:
            piece: chess.Piece object
            position: (x, y) tuple of pixel coordinates (center of piece)
        """
        symbol = piece.symbol()
        if symbol in self.piece_images:
            image = self.piece_images[symbol]
            # Center the image at the position
            rect = image.get_rect(center=position)
            self.screen.blit(image, rect)
    
    def draw_piece_at_square(self, piece, square, board_view):
        """
        Draw a piece at a chess square.
        
        Args:
            piece: chess.Piece object
            square: Chess square (0-63)
            board_view: BoardView instance for coordinate conversion
        """
        position = board_view.square_to_pixel(square)
        self.draw_piece(piece, position)
    
    def draw_all_pieces(self, chess_board, board_view, exclude_square=None):
        """
        Draw all pieces on the board.
        
        Args:
            chess_board: ChessBoard instance
            board_view: BoardView instance
            exclude_square: Optional square to skip (for drag-and-drop)
        """
        for square in chess.SQUARES:
            if square == exclude_square:
                continue
            
            piece = chess_board.get_piece_at(square)
            if piece:
                self.draw_piece_at_square(piece, square, board_view)
    
    def get_piece_image(self, piece):
        """
        Get the image for a piece.
        
        Args:
            piece: chess.Piece object
        
        Returns:
            pygame.Surface: The piece image
        """
        symbol = piece.symbol()
        return self.piece_images.get(symbol)
