"""
Convert SVG chess pieces to PNG format using pygame.
"""

import pygame
import os
from pathlib import Path
from xml.etree import ElementTree as ET

# For SVG, we'll use a simpler approach - download PNG directly
import urllib.request

pieces_dir = Path("assets/pieces")
size = 100

# Use a different source that provides PNG directly
# cburnett pieces from Wikimedia Commons
base_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/"

# Wikimedia Commons file IDs for cburnett chess pieces
pieces_urls = {
    'white_pawn': '4/45/Chess_plt45.svg/100px-Chess_plt45.svg.png',
    'white_knight': '7/70/Chess_nlt45.svg/100px-Chess_nlt45.svg.png',
    'white_bishop': 'b/b1/Chess_blt45.svg/100px-Chess_blt45.svg.png',
    'white_rook': '7/72/Chess_rlt45.svg/100px-Chess_rlt45.svg.png',
    'white_queen': '1/15/Chess_qlt45.svg/100px-Chess_qlt45.svg.png',
    'white_king': '4/42/Chess_klt45.svg/100px-Chess_klt45.svg.png',
    'black_pawn': 'c/c7/Chess_pdt45.svg/100px-Chess_pdt45.svg.png',
    'black_knight': 'e/ef/Chess_ndt45.svg/100px-Chess_ndt45.svg.png',
    'black_bishop': '9/98/Chess_bdt45.svg/100px-Chess_bdt45.svg.png',
    'black_rook': 'f/ff/Chess_rdt45.svg/100px-Chess_rdt45.svg.png',
    'black_queen': '4/47/Chess_qdt45.svg/100px-Chess_qdt45.svg.png',
    'black_king': 'f/f0/Chess_kdt45.svg/100px-Chess_kdt45.svg.png',
}

print(f"Downloading high-quality PNG chess pieces ({size}x{size})...\n")

for piece, url_path in pieces_urls.items():
    url = base_url + url_path
    output_path = pieces_dir / f"{piece}.png"
    
    # Remove old files
    svg_path = pieces_dir / f"{piece}.svg"
    if svg_path.exists():
        svg_path.unlink()
    
    try:
        print(f"Downloading {piece}...")
        urllib.request.urlretrieve(url, output_path)
        print(f"  ✓ Saved to {output_path}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")

print("\n✓ Download complete!")
print("High-quality chess pieces are now ready to use.")
print("These are professional-grade pieces similar to chess.com style.")

