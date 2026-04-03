"""
Test LC0 engine directly.
"""

import subprocess
import sys

engine_path = "bin/lc0.exe"
weights_path = "weights/network.pb.gz"

print("Testing LC0 engine...")
print(f"Engine: {engine_path}")
print(f"Weights: {weights_path}")

# Test with command line args
cmd = [engine_path, "--weights", weights_path]

try:
    print("\nStarting engine...")
    
    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    else:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=0
        )
    
    print("Sending 'uci' command...")
    process.stdin.write("uci\n")
    process.stdin.flush()
    
    print("Reading output...\n")
    import time
    timeout = time.time() + 10
    
    while time.time() < timeout:
        line = process.stdout.readline()
        if line:
            print(f"< {line.strip()}")
            if "uciok" in line:
                print("\n✓ Engine responded successfully!")
                break
        else:
            time.sleep(0.1)
    
    process.stdin.write("quit\n")
    process.stdin.flush()
    process.wait(timeout=2)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
