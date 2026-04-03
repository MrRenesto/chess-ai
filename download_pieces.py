"""
Download better chess piece images (cburnett style - similar to chess.com).
These are open-source pieces from Lichess.
"""

import urllib.request
import os

# Create pieces directory
os.makedirs("assets/pieces", exist_ok=True)

# Lichess pieces (cburnett style) - these are open source
# Base URL for lichess piece images
base_url = "https://raw.githubusercontent.com/lichess-org/lila/master/public/piece/cburnett/"

pieces = {
    'white_pawn': 'wP.svg',
    'white_knight': 'wN.svg',
    'white_bishop': 'wB.svg',
    'white_rook': 'wR.svg',
    'white_queen': 'wQ.svg',
    'white_king': 'wK.svg',
    'black_pawn': 'bP.svg',
    'black_knight': 'bN.svg',
    'black_bishop': 'bB.svg',
    'black_rook': 'bR.svg',
    'black_queen': 'bQ.svg',
    'black_king': 'bK.svg',
}

print("Downloading chess pieces from Lichess (cburnett style)...")
print("These pieces are open source and similar to chess.com style.\n")

for name, filename in pieces.items():
    url = base_url + filename
    output_path = f"assets/pieces/{name}.svg"
    
    try:
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, output_path)
        print(f"  ✓ Saved to {output_path}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

print("\n✓ Download complete!")
print("\nNote: SVG files downloaded. We'll need to convert them to PNG.")
print("Installing required packages...")

import subprocess
import sys

try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cairosvg", "pillow", "-q"])
    print("✓ Packages installed")
except:
    print("⚠ Failed to install packages. You may need to install cairosvg and pillow manually.")
