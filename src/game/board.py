"""
Chess board wrapper using python-chess library.
Manages the game state, moves, and chess rules.
"""

import chess


class ChessBoard:
    """Wrapper around python-chess Board for game logic."""
    
    def __init__(self, fen=None):
        """
        Initialize the chess board.
        
        Args:
            fen: Optional FEN string to set up a specific position.
                 If None, starts with standard chess starting position.
        """
        if fen:
            self.board = chess.Board(fen)
        else:
            self.board = chess.Board()
    
    def make_move(self, move):
        """
        Make a move on the board.
        
        Args:
            move: Either a chess.Move object or UCI string (e.g., 'e2e4')
        
        Returns:
            bool: True if move was successful, False otherwise
        """
        try:
            if isinstance(move, str):
                move = chess.Move.from_uci(move)
            
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            return False
        except ValueError:
            return False
    
    def get_legal_moves(self, square=None):
        """
        Get all legal moves, optionally filtered by source square.
        
        Args:
            square: Optional chess.Square (0-63) to filter moves from that square
        
        Returns:
            list: List of legal chess.Move objects
        """
        if square is not None:
            return [move for move in self.board.legal_moves 
                   if move.from_square == square]
        return list(self.board.legal_moves)
    
    def get_piece_at(self, square):
        """
        Get the piece at a given square.
        
        Args:
            square: chess.Square (0-63)
        
        Returns:
            chess.Piece or None: The piece at the square, or None if empty
        """
        return self.board.piece_at(square)
    
    def is_game_over(self):
        """Check if the game is over (checkmate, stalemate, etc.)."""
        return self.board.is_game_over()
    
    def is_checkmate(self):
        """Check if current position is checkmate."""
        return self.board.is_checkmate()
    
    def is_stalemate(self):
        """Check if current position is stalemate."""
        return self.board.is_stalemate()
    
    def is_check(self):
        """Check if current player is in check."""
        return self.board.is_check()
    
    def get_result(self):
        """
        Get the game result.
        
        Returns:
            str: '1-0' (white wins), '0-1' (black wins), '1/2-1/2' (draw), or '*' (ongoing)
        """
        return self.board.result()
    
    def get_fen(self):
        """Get the FEN (Forsyth-Edwards Notation) string of current position."""
        return self.board.fen()
    
    def get_turn(self):
        """
        Get whose turn it is.
        
        Returns:
            bool: True if white's turn, False if black's turn
        """
        return self.board.turn
    
    def undo_move(self):
        """
        Undo the last move.
        
        Returns:
            chess.Move or None: The move that was undone, or None if no moves to undo
        """
        try:
            return self.board.pop()
        except IndexError:
            return None
    
    def get_move_history(self):
        """
        Get the move history in UCI notation.
        
        Returns:
            list: List of UCI move strings
        """
        return [move.uci() for move in self.board.move_stack]
    
    def get_san_history(self):
        """
        Get the move history in SAN (Standard Algebraic Notation).
        
        Returns:
            list: List of SAN move strings
        """
        board_copy = chess.Board()
        san_moves = []
        for move in self.board.move_stack:
            san_moves.append(board_copy.san(move))
            board_copy.push(move)
        return san_moves
    
    def reset(self):
        """Reset the board to the starting position."""
        self.board.reset()
    
    def __str__(self):
        """String representation of the board (for debugging)."""
        return str(self.board)
