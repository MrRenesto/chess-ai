"""
Main entry point for the chess game.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

import pygame
from ui.window import GameWindow
from ui.board_view import BoardView
from ui.piece_view import PieceView
from game.game_manager import GameManager


def main():
    """Main game loop."""
    # Create window and game manager
    window = GameWindow()
    game_manager = GameManager()
    board_view = BoardView(window.get_screen())
    piece_view = PieceView(window.get_screen(), board_view.square_size)
    
    window.start()
    
    print("Chess AI - Starting...")
    print("Window created successfully!")
    print("Close the window to exit.")
    
    # Main game loop
    while window.running:
        # Handle events
        events = window.handle_events()
        
        if events['quit']:
            window.stop()
            break
        
        # Clear screen
        window.clear()
        
        # Render board
        board_view.draw_board()
        board_view.draw_coordinates()
        
        # Render pieces
        piece_view.draw_all_pieces(game_manager.get_board(), board_view)
        
        # TODO: Handle input
        # TODO: Update AI
        
        # Update display
        window.update_display()
    
    # Cleanup
    window.quit()


if __name__ == "__main__":
    main()
