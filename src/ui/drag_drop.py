"""
Drag and drop handler for chess pieces.
"""

import pygame
import chess


class DragDropHandler:
    """Manages drag-and-drop interaction for chess pieces."""
    
    def __init__(self, board_view, piece_view):
        """
        Initialize drag-and-drop handler.
        
        Args:
            board_view: BoardView instance
            piece_view: PieceView instance
        """
        self.board_view = board_view
        self.piece_view = piece_view
        
        # Drag state
        self.dragging = False
        self.drag_piece = None
        self.drag_start_square = None
        self.drag_pos = None
    
    def handle_mouse_down(self, mouse_pos, game_manager):
        """
        Handle mouse button down event.
        
        Args:
            mouse_pos: (x, y) tuple of mouse position
            game_manager: GameManager instance
        
        Returns:
            bool: True if drag started
        """
        # Convert pixel to square
        square = self.board_view.pixel_to_square(*mouse_pos)
        
        if square is None:
            return False
        
        # Check if there's a piece at this square
        piece = game_manager.get_board().get_piece_at(square)
        
        if piece is None:
            return False
        
        # Check if it's the correct player's turn
        if piece.color != game_manager.get_board().get_turn():
            return False
        
        # Check if it's the player's turn (not AI)
        if not game_manager.is_players_turn():
            return False
        
        # Start dragging
        self.dragging = True
        self.drag_piece = piece
        self.drag_start_square = square
        self.drag_pos = mouse_pos
        
        return True
    
    def handle_mouse_motion(self, mouse_pos):
        """
        Handle mouse motion event.
        
        Args:
            mouse_pos: (x, y) tuple of mouse position
        """
        if self.dragging:
            self.drag_pos = mouse_pos
    
    def handle_mouse_up(self, mouse_pos, game_manager):
        """
        Handle mouse button up event.
        
        Args:
            mouse_pos: (x, y) tuple of mouse position
            game_manager: GameManager instance
        
        Returns:
            dict: Move information or None if no valid move
        """
        if not self.dragging:
            return None
        
        # Get destination square
        dest_square = self.board_view.pixel_to_square(*mouse_pos)
        
        # Reset drag state
        self.dragging = False
        drag_start = self.drag_start_square
        self.drag_piece = None
        self.drag_start_square = None
        self.drag_pos = None
        
        if dest_square is None:
            return None
        
        # Attempt to make the move
        from_sq = chess.square_name(drag_start)
        to_sq = chess.square_name(dest_square)
        move_uci = f"{from_sq}{to_sq}"
        
        # Check for pawn promotion
        piece = game_manager.get_board().get_piece_at(drag_start)
        if piece and piece.piece_type == chess.PAWN:
            to_rank = chess.square_rank(dest_square)
            if (piece.color and to_rank == 7) or (not piece.color and to_rank == 0):
                move_uci += "q"  # Auto-promote to queen for now
        
        # Try to make the move
        if game_manager.make_uci_move(move_uci):
            return {
                'success': True,
                'from': drag_start,
                'to': dest_square,
                'game_state': game_manager.game_state
            }
        
        return {'success': False}
    
    def is_dragging(self):
        """Check if currently dragging."""
        return self.dragging
    
    def get_drag_square(self):
        """Get the square being dragged from."""
        return self.drag_start_square
    
    def render_dragged_piece(self):
        """Render the piece being dragged at mouse position."""
        if self.dragging and self.drag_piece and self.drag_pos:
            self.piece_view.draw_piece(self.drag_piece, self.drag_pos)
