# Chess AI - Neural Network Chess Game

An interactive chess game built with Python and Pygame where you can play against a neural network AI powered by Leela Chess Zero. Future versions will include coaching features to help you improve your chess skills.

## Features

### Current
- Play chess against a neural network AI (Leela Chess Zero)
- Drag-and-drop piece movement
- Full chess rules implementation
- Visual move highlighting
- Clean, intuitive GUI

### Planned
- AI coaching mode with move suggestions
- Position analysis and evaluation
- Mistake detection with explanations
- Opening book recommendations
- Progress tracking and statistics

## Technology Stack

- **Language**: Python 3.10+
- **GUI**: Pygame
- **Chess Engine**: python-chess library
- **AI**: Leela Chess Zero (LC0) with pre-trained neural network

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/chess-ai.git
cd chess-ai
```

2. Create and activate virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download Leela Chess Zero:
- Download LC0 binary from https://github.com/LeelaChessZero/lc0/releases
- Download neural network weights from https://lczero.org/play/networks/bestnets/
- Place weights in the `weights/` directory

5. Run the game:
```bash
python src/main.py
```

## Project Structure

```
chess-ai/
├── src/              # Source code
│   ├── game/         # Chess logic
│   ├── ai/           # AI engine interface
│   ├── ui/           # GUI components
│   └── utils/        # Utilities
├── assets/           # Images and sounds
├── weights/          # LC0 neural network weights
└── tests/            # Unit tests
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
This project follows PEP 8 style guidelines.

## Roadmap

- [x] Project setup and architecture
- [ ] Core chess logic implementation
- [ ] Pygame GUI with drag-and-drop
- [ ] AI integration with Leela Chess Zero
- [ ] Game state management
- [ ] Move history and game saving
- [ ] Coaching features (future)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [python-chess](https://python-chess.readthedocs.io/) for chess logic
- [Leela Chess Zero](https://lczero.org/) for the neural network AI
- Chess piece graphics from [chess.com](https://www.chess.com/) or similar open source sets
