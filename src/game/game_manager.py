"""
Game manager - orchestrates game flow and state.
"""

from .board import ChessBoard


class GameManager:
    """Manages the overall game state and flow."""
    
    def __init__(self):
        """Initialize the game manager."""
        self.board = ChessBoard()
        self.game_state = "playing"  # playing, checkmate, stalemate, draw
        self.selected_square = None
        self.player_color = True  # True = white, False = black
        self.ai_enabled = True
    
    def handle_square_click(self, square):
        """
        Handle a click on a square.
        
        Args:
            square: chess.Square (0-63)
        
        Returns:
            tuple: (success: bool, info: dict)
        """
        # If it's AI's turn, don't allow moves
        if self.ai_enabled and self.board.get_turn() != self.player_color:
            return False, {"message": "Wait for AI to move"}
        
        piece = self.board.get_piece_at(square)
        
        # First click - select a piece
        if self.selected_square is None:
            if piece and piece.color == self.board.get_turn():
                self.selected_square = square
                legal_moves = self.board.get_legal_moves(square)
                return True, {
                    "action": "select",
                    "square": square,
                    "legal_moves": legal_moves
                }
            return False, {"message": "No piece or wrong color"}
        
        # Second click - try to move
        else:
            from_square = self.selected_square
            self.selected_square = None
            
            # Try to make the move
            move = f"{chess.square_name(from_square)}{chess.square_name(square)}"
            
            # Check for promotion (simplified - always promote to queen)
            from_piece = self.board.get_piece_at(from_square)
            if from_piece and from_piece.piece_type == chess.PAWN:
                to_rank = chess.square_rank(square)
                if (from_piece.color and to_rank == 7) or (not from_piece.color and to_rank == 0):
                    move += "q"  # Promote to queen
            
            if self.board.make_move(move):
                self._update_game_state()
                return True, {
                    "action": "move",
                    "from": from_square,
                    "to": square,
                    "game_state": self.game_state
                }
            
            return False, {"message": "Illegal move"}
    
    def make_move(self, from_square, to_square, promotion='q'):
        """
        Make a move programmatically (e.g., by AI).
        
        Args:
            from_square: Source square (0-63)
            to_square: Destination square (0-63)
            promotion: Promotion piece ('q', 'r', 'b', 'n')
        
        Returns:
            bool: True if move was successful
        """
        move = f"{chess.square_name(from_square)}{chess.square_name(to_square)}"
        
        # Check if promotion is needed
        piece = self.board.get_piece_at(from_square)
        if piece and piece.piece_type == chess.PAWN:
            to_rank = chess.square_rank(to_square)
            if (piece.color and to_rank == 7) or (not piece.color and to_rank == 0):
                move += promotion
        
        if self.board.make_move(move):
            self._update_game_state()
            return True
        return False
    
    def make_uci_move(self, uci_move):
        """
        Make a move using UCI notation (e.g., 'e2e4').
        
        Args:
            uci_move: Move in UCI format
        
        Returns:
            bool: True if successful
        """
        if self.board.make_move(uci_move):
            self._update_game_state()
            return True
        return False
    
    def _update_game_state(self):
        """Update the game state after a move."""
        if self.board.is_checkmate():
            self.game_state = "checkmate"
        elif self.board.is_stalemate():
            self.game_state = "stalemate"
        elif self.board.is_game_over():
            self.game_state = "draw"
        else:
            self.game_state = "playing"
    
    def undo_last_move(self):
        """Undo the last move."""
        move = self.board.undo_move()
        if move:
            self._update_game_state()
            return True
        return False
    
    def reset_game(self):
        """Reset the game to starting position."""
        self.board.reset()
        self.game_state = "playing"
        self.selected_square = None
    
    def get_board(self):
        """Get the chess board."""
        return self.board
    
    def get_legal_moves_for_square(self, square):
        """Get legal moves from a specific square."""
        return self.board.get_legal_moves(square)
    
    def is_players_turn(self):
        """Check if it's the player's turn."""
        return self.board.get_turn() == self.player_color


import chess
