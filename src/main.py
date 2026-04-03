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
from ui.drag_drop import DragDropHandler
from ui.highlighter import MoveHighlighter
from game.game_manager import GameManager


def main():
    """Main game loop."""
    # Create window and game manager
    window = GameWindow()
    game_manager = GameManager()
    board_view = BoardView(window.get_screen())
    piece_view = PieceView(window.get_screen(), board_view.square_size)
    drag_handler = DragDropHandler(board_view, piece_view)
    highlighter = MoveHighlighter(board_view)
    
    window.start()
    
    print("Chess AI - Starting...")
    print("Window created successfully!")
    print("Drag and drop pieces to move.")
    print("Close the window to exit.")
    
    # Main game loop
    while window.running:
        # Handle events
        events = window.handle_events()
        
        if events['quit']:
            window.stop()
            break
        
        # Handle drag and drop
        if events['mouse_down']:
            if drag_handler.handle_mouse_down(events['mouse_click'], game_manager):
                # Started dragging - highlight legal moves
                highlighter.highlight_legal_moves(
                    drag_handler.get_drag_square(),
                    game_manager
                )
        
        if events['mouse_pos']:
            drag_handler.handle_mouse_motion(events['mouse_pos'])
        
        if events['mouse_up']:
            result = drag_handler.handle_mouse_up(events['mouse_pos'], game_manager)
            if result and result['success']:
                # Move was made - update last move highlight
                highlighter.set_last_move(result['from'], result['to'])
                highlighter.clear_highlights()
                
                # Check game state
                if game_manager.game_state == "checkmate":
                    winner = "Black" if game_manager.get_board().get_turn() else "White"
                    print(f"Checkmate! {winner} wins!")
                elif game_manager.game_state == "stalemate":
                    print("Stalemate! It's a draw.")
                elif game_manager.game_state == "draw":
                    print("Draw!")
            else:
                highlighter.clear_highlights()
        
        # Handle keyboard shortcuts
        if events['key_press']:
            if events['key_press'] == pygame.K_u:  # Undo
                if game_manager.undo_last_move():
                    highlighter.last_move = None
                    print("Move undone")
            elif events['key_press'] == pygame.K_r:  # Reset
                game_manager.reset_game()
                highlighter.last_move = None
                highlighter.clear_highlights()
                print("Game reset")
        
        # Clear screen
        window.clear()
        
        # Render board
        board_view.draw_board()
        
        # Render highlights
        highlighter.render(game_manager)
        
        # Render pieces (skip dragged piece)
        piece_view.draw_all_pieces(
            game_manager.get_board(),
            board_view,
            exclude_square=drag_handler.get_drag_square()
        )
        
        # Render dragged piece on top
        drag_handler.render_dragged_piece()
        
        # Render coordinates last (on top)
        board_view.draw_coordinates()
        
        # Update display
        window.update_display()
    
    # Cleanup
    window.quit()


if __name__ == "__main__":
    main()
