# Conway's Game of Life

An interactive visualizer for Conway's Game of Life using Pygame.

## Requirements

- Python 3.6+
- Pygame (`pip install pygame`)

## How to Run

```
python life.py
```

With custom settings:

```
python life.py --width 80 --height 40 --fps 15
```

## Controls

- Space: Play/Pause
- N: Single step
- C: Clear board
- R: Random fill
- S: Save pattern
- L: Load pattern
- Left Click: Add cell
- Right Click: Remove cell
- Escape: Quit

## Game Rules

1. Any live cell with <2 live neighbors dies
2. Any live cell with 2-3 live neighbors lives
3. Any live cell with >3 live neighbors dies
4. Any dead cell with exactly 3 live neighbors becomes alive

## Patterns

The `patterns.txt` file contains several common patterns:
- Glider (moves diagonally)
- Blinker (oscillates)
- Block (still life)
- Toad (oscillator)
- Beacon (oscillator)
- Pulsar (oscillator)

To use these patterns, uncomment the relevant section in patterns.txt, then press 'L' in the game.

