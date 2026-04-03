"""
UCI Chess Engine Interface - communicates with LC0 via UCI protocol.
"""

import subprocess
import threading
import queue
import time
import chess


class UCIEngine:
    """Interface to communicate with UCI chess engines like LC0."""
    
    def __init__(self, engine_path, weights_path=None):
        """
        Initialize the UCI engine.
        
        Args:
            engine_path: Path to the engine executable
            weights_path: Path to neural network weights (for LC0)
        """
        self.engine_path = engine_path
        self.weights_path = weights_path
        self.process = None
        self.output_queue = queue.Queue()
        self.ready = False
        self.thread = None
        
    def start(self):
        """Start the engine process."""
        cmd = [self.engine_path]
        
        # Add weights parameter for LC0 (use --weights=path format)
        if self.weights_path:
            cmd.append(f'--weights={self.weights_path}')
        
        # Windows-specific: use CREATE_NO_WINDOW flag
        import sys
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,  # Suppress stderr
                text=True,
                bufsize=0,  # Unbuffered
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=0
            )
        
        # Start output reading thread
        self.thread = threading.Thread(target=self._read_output, daemon=True)
        self.thread.start()
        
        # Initialize engine
        self._send_command("uci")
        if not self._wait_for("uciok", timeout=10):
            raise Exception("Engine failed to respond to UCI command")
        
        self._send_command("isready")
        if not self._wait_for("readyok", timeout=10):
            raise Exception("Engine not ready")
        
        self.ready = True
        print("Engine started and ready")
    
    def _send_command(self, command):
        """Send a command to the engine."""
        if self.process and self.process.stdin:
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()
    
    def _read_output(self):
        """Read output from engine in a separate thread."""
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline()
            if line:
                self.output_queue.put(line.strip())
    
    def _wait_for(self, expected_response, timeout=30):
        """Wait for a specific response from the engine."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                line = self.output_queue.get(timeout=0.1)
                if expected_response in line:
                    return True
            except queue.Empty:
                continue
        return False
    
    def get_best_move(self, board, time_limit=1.0, nodes=None):
        """
        Get the best move for the current position.
        
        Args:
            board: chess.Board object
            time_limit: Time limit in seconds
            nodes: Number of nodes to search (alternative to time)
        
        Returns:
            chess.Move or None: Best move found
        """
        if not self.ready:
            return None
        
        # Set up position
        fen = board.fen()
        self._send_command(f"position fen {fen}")
        
        # Start search
        if nodes:
            self._send_command(f"go nodes {nodes}")
        else:
            movetime_ms = int(time_limit * 1000)
            self._send_command(f"go movetime {movetime_ms}")
        
        # Wait for bestmove
        best_move = None
        start_time = time.time()
        max_wait = time_limit + 5  # Give extra time
        
        while time.time() - start_time < max_wait:
            try:
                line = self.output_queue.get(timeout=0.1)
                if line.startswith("bestmove"):
                    parts = line.split()
                    if len(parts) >= 2:
                        move_str = parts[1]
                        try:
                            best_move = chess.Move.from_uci(move_str)
                            break
                        except ValueError:
                            pass
            except queue.Empty:
                continue
        
        return best_move
    
    def set_option(self, name, value):
        """
        Set an engine option.
        
        Args:
            name: Option name
            value: Option value
        """
        self._send_command(f"setoption name {name} value {value}")
    
    def stop(self):
        """Stop the engine."""
        if self.process:
            try:
                self._send_command("quit")
                self.process.wait(timeout=2)
            except:
                self.process.terminate()
                try:
                    self.process.wait(timeout=1)
                except:
                    self.process.kill()
            finally:
                self.process = None
                self.ready = False
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop()
