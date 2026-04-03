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
from ai.ai_player import AIPlayer
from ai.settings import AISettings


def main():
    """Main game loop."""
    # Create window and game manager
    window = GameWindow()
    game_manager = GameManager()
    board_view = BoardView(window.get_screen())
    piece_view = PieceView(window.get_screen(), board_view.square_size)
    drag_handler = DragDropHandler(board_view, piece_view)
    highlighter = MoveHighlighter(board_view)
    
    # Initialize AI
    ai_settings = AISettings()
    ai_settings.set_difficulty('medium')  # Start with medium difficulty
    ai_player = AIPlayer(ai_settings)
    
    print("Chess AI - Starting...")
    print("Initializing AI engine...")
    
    if not ai_player.start():
        print("WARNING: AI engine failed to start. You can still play 2-player mode.")
        ai_player = None
    
    window.start()
    
    print("Window created successfully!")
    print("Drag and drop pieces to move.")
    print("You are White, AI is Black.")
    print("Controls: U=Undo, R=Reset, ESC=Quit")
    print("Close the window to exit.")
    
    ai_move_pending = False
    
    def on_ai_move(move):
        """Callback when AI finishes thinking."""
        nonlocal ai_move_pending
        if move and game_manager.board.make_move(move):
            highlighter.set_last_move(move.from_square, move.to_square)
            print(f"AI plays: {move.uci()}")
            
            # Check game state
            game_manager._update_game_state()
            if game_manager.game_state == "checkmate":
                print("Checkmate! AI wins!")
            elif game_manager.game_state == "stalemate":
                print("Stalemate! It's a draw.")
        ai_move_pending = False
    
    # Main game loop
    while window.running:
        # Handle events
        events = window.handle_events()
        
        if events['quit']:
            window.stop()
            break
        
        # Check if it's AI's turn and AI is not thinking
        if (ai_player and 
            not ai_move_pending and 
            not ai_player.is_thinking() and
            game_manager.game_state == "playing" and
            game_manager.board.get_turn() == ai_settings.color):
            
            ai_move_pending = True
            print("AI is thinking...")
            ai_player.think_async(game_manager.board.board, on_ai_move)
        
        # Handle drag and drop (only when it's player's turn)
        if events['mouse_down'] and not ai_move_pending:
            if drag_handler.handle_mouse_down(events['mouse_click'], game_manager):
                # Started dragging - highlight legal moves
                highlighter.highlight_legal_moves(
                    drag_handler.get_drag_square(),
                    game_manager
                )
        
        if events['mouse_pos']:
            drag_handler.handle_mouse_motion(events['mouse_pos'])
        
        if events['mouse_up'] and not ai_move_pending:
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
                    # Undo AI move too if present
                    if ai_player and game_manager.board.get_turn() != ai_settings.color:
                        game_manager.undo_last_move()
                    highlighter.last_move = None
                    ai_move_pending = False
                    print("Move undone")
            elif events['key_press'] == pygame.K_r:  # Reset
                game_manager.reset_game()
                highlighter.last_move = None
                highlighter.clear_highlights()
                ai_move_pending = False
                print("Game reset")
            elif events['key_press'] == pygame.K_ESCAPE:  # Quit
                window.stop()
        
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
    if ai_player:
        print("Shutting down AI...")
        ai_player.stop()
    
    window.quit()


if __name__ == "__main__":
    main()
