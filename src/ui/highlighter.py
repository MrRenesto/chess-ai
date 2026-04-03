"""
Move highlighter - shows legal moves and indicators.
"""

import pygame
import chess
from utils.constants import HIGHLIGHT_COLOR, CHECK_COLOR, LAST_MOVE_COLOR


class MoveHighlighter:
    """Highlights legal moves and game states."""
    
    def __init__(self, board_view):
        """
        Initialize move highlighter.
        
        Args:
            board_view: BoardView instance
        """
        self.board_view = board_view
        self.highlighted_squares = []
        self.last_move = None
    
    def highlight_legal_moves(self, square, game_manager):
        """
        Highlight legal moves from a square.
        
        Args:
            square: Chess square (0-63)
            game_manager: GameManager instance
        """
        self.highlighted_squares = []
        
        if square is None:
            return
        
        # Get legal moves from this square
        legal_moves = game_manager.get_legal_moves_for_square(square)
        
        # Extract destination squares
        for move in legal_moves:
            self.highlighted_squares.append(move.to_square)
    
    def set_last_move(self, from_square, to_square):
        """
        Set the last move for highlighting.
        
        Args:
            from_square: Source square (0-63)
            to_square: Destination square (0-63)
        """
        self.last_move = (from_square, to_square)
    
    def clear_highlights(self):
        """Clear all highlights."""
        self.highlighted_squares = []
    
    def render(self, game_manager):
        """
        Render all highlights.
        
        Args:
            game_manager: GameManager instance
        """
        # Highlight last move
        if self.last_move:
            from_sq, to_sq = self.last_move
            self.board_view.highlight_square(from_sq, LAST_MOVE_COLOR)
            self.board_view.highlight_square(to_sq, LAST_MOVE_COLOR)
        
        # Highlight legal move destinations
        for square in self.highlighted_squares:
            self._draw_move_indicator(square)
        
        # Highlight check
        if game_manager.get_board().is_check():
            king_square = self._find_king_square(
                game_manager.get_board(),
                game_manager.get_board().get_turn()
            )
            if king_square is not None:
                self.board_view.highlight_square(king_square, CHECK_COLOR)
    
    def _draw_move_indicator(self, square):
        """
        Draw a move indicator on a square.
        
        Args:
            square: Chess square (0-63)
        """
        # Get square center
        center = self.board_view.square_to_pixel(square)
        
        # Draw a circle indicator
        radius = self.board_view.square_size // 6
        
        # Create transparent surface
        surface = pygame.Surface(
            (self.board_view.square_size, self.board_view.square_size),
            pygame.SRCALPHA
        )
        
        # Draw circle in center
        center_offset = self.board_view.square_size // 2
        pygame.draw.circle(
            surface,
            HIGHLIGHT_COLOR,
            (center_offset, center_offset),
            radius
        )
        
        # Get square rect
        rect = self.board_view.get_square_rect(square)
        self.board_view.screen.blit(surface, rect.topleft)
    
    def _find_king_square(self, chess_board, color):
        """
        Find the king's square for a given color.
        
        Args:
            chess_board: ChessBoard instance
            color: True for white, False for black
        
        Returns:
            int or None: Square where king is located
        """
        for square in chess.SQUARES:
            piece = chess_board.get_piece_at(square)
            if piece and piece.piece_type == chess.KING and piece.color == color:
                return square
        return None
