"""
AI settings and configuration.
"""

import os
from pathlib import Path


class AISettings:
    """Configuration for the AI opponent."""
    
    # Difficulty presets (nodes to search)
    DIFFICULTY_EASY = 100
    DIFFICULTY_MEDIUM = 1000
    DIFFICULTY_HARD = 5000
    DIFFICULTY_EXPERT = 20000
    
    def __init__(self):
        """Initialize AI settings with defaults."""
        # Engine paths
        project_root = Path(__file__).parent.parent.parent
        self.engine_path = str(project_root / "bin" / "lc0.exe")
        self.weights_path = str(project_root / "weights" / "network.pb.gz")
        
        # Search settings
        self.difficulty = self.DIFFICULTY_MEDIUM
        self.time_limit = 2.0  # seconds
        self.use_nodes = True  # Use nodes instead of time
        
        # Play settings
        self.enabled = True
        self.color = False  # False = black (AI plays black)
    
    def set_difficulty(self, level):
        """
        Set difficulty level.
        
        Args:
            level: 'easy', 'medium', 'hard', or 'expert'
        """
        difficulty_map = {
            'easy': self.DIFFICULTY_EASY,
            'medium': self.DIFFICULTY_MEDIUM,
            'hard': self.DIFFICULTY_HARD,
            'expert': self.DIFFICULTY_EXPERT
        }
        
        if level.lower() in difficulty_map:
            self.difficulty = difficulty_map[level.lower()]
            print(f"AI difficulty set to: {level} ({self.difficulty} nodes)")
        else:
            print(f"Unknown difficulty: {level}")
    
    def validate(self):
        """
        Validate that required files exist.
        
        Returns:
            tuple: (bool: valid, str: error message)
        """
        if not os.path.exists(self.engine_path):
            return False, f"Engine not found: {self.engine_path}"
        
        if not os.path.exists(self.weights_path):
            return False, f"Weights not found: {self.weights_path}"
        
        return True, "OK"
