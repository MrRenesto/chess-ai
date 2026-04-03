"""
Main Pygame window and event loop.
"""

import pygame
import sys
from utils.constants import WINDOW_SIZE, FPS, WHITE


class GameWindow:
    """Main game window using Pygame."""
    
    def __init__(self, width=WINDOW_SIZE, height=WINDOW_SIZE, title="Chess AI"):
        """
        Initialize the game window.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
        """
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        self.clock = pygame.time.Clock()
        self.running = False
        self.fps = FPS
    
    def handle_events(self):
        """
        Handle pygame events.
        
        Returns:
            dict: Event information for game logic
        """
        events = {
            'quit': False,
            'mouse_click': None,
            'mouse_pos': None,
            'mouse_down': False,
            'mouse_up': False,
            'key_press': None
        }
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events['quit'] = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    events['mouse_click'] = event.pos
                    events['mouse_down'] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    events['mouse_up'] = True
            
            elif event.type == pygame.KEYDOWN:
                events['key_press'] = event.key
        
        # Always get current mouse position
        events['mouse_pos'] = pygame.mouse.get_pos()
        
        return events
    
    def clear(self, color=WHITE):
        """Clear the screen with a color."""
        self.screen.fill(color)
    
    def update_display(self):
        """Update the display and maintain framerate."""
        pygame.display.flip()
        self.clock.tick(self.fps)
    
    def start(self):
        """Start the game loop."""
        self.running = True
    
    def stop(self):
        """Stop the game loop."""
        self.running = False
    
    def quit(self):
        """Quit pygame and close window."""
        pygame.quit()
        sys.exit()
    
    def get_screen(self):
        """Get the pygame screen surface."""
        return self.screen
