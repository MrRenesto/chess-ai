"""
AI Player - manages the AI opponent.
"""

import threading
from .engine import UCIEngine
from .settings import AISettings


class AIPlayer:
    """Manages the AI chess player."""
    
    def __init__(self, settings=None):
        """
        Initialize AI player.
        
        Args:
            settings: AISettings instance (creates default if None)
        """
        self.settings = settings or AISettings()
        self.engine = None
        self.thinking = False
        self.current_move = None
        self.think_thread = None
    
    def start(self):
        """Start the AI engine."""
        # Validate settings
        valid, error = self.settings.validate()
        if not valid:
            print(f"AI initialization failed: {error}")
            return False
        
        try:
            self.engine = UCIEngine(
                self.settings.engine_path,
                self.settings.weights_path
            )
            self.engine.start()
            print("AI engine initialized successfully")
            return True
        except Exception as e:
            print(f"Failed to start AI engine: {e}")
            return False
    
    def think_async(self, board, callback):
        """
        Start thinking about the best move in a separate thread.
        
        Args:
            board: chess.Board object
            callback: Function to call with the move when ready
        """
        if self.thinking:
            return
        
        self.thinking = True
        self.current_move = None
        
        def think():
            try:
                if self.settings.use_nodes:
                    move = self.engine.get_best_move(
                        board,
                        nodes=self.settings.difficulty
                    )
                else:
                    move = self.engine.get_best_move(
                        board,
                        time_limit=self.settings.time_limit
                    )
                
                self.current_move = move
                self.thinking = False
                
                if callback:
                    callback(move)
            except Exception as e:
                print(f"AI thinking error: {e}")
                self.thinking = False
                if callback:
                    callback(None)
        
        self.think_thread = threading.Thread(target=think, daemon=True)
        self.think_thread.start()
    
    def is_thinking(self):
        """Check if AI is currently thinking."""
        return self.thinking
    
    def stop(self):
        """Stop the AI engine."""
        if self.engine:
            self.engine.stop()
            self.engine = None
    
    def __del__(self):
        """Cleanup when destroyed."""
        self.stop()
