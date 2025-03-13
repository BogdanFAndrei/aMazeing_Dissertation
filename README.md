# aMazeing: Maze Generation and Pathfinding Visualization

## About
This project was created as part of a dissertation at Liverpool John Moores University. It demonstrates and visualizes different pathfinding algorithms (A*, BFS, DFS) working through procedurally generated mazes.

## Features
- Procedural maze generation
- Multiple pathfinding algorithms:
  - A* (A-Star) Algorithm
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
- Real-time visualization of:
  - Maze generation process
  - Path exploration
  - Final solution path
- Interactive GUI with customizable settings:
  - Adjustable maze size
  - Toggle animation on/off
  - Toggle loop creation in maze generation

## Controls
- Space: Start generation/solving
- Enter: Reset
- D: Toggle animation
- L: Toggle loops

## Installation
1. Ensure you have Python 3.x installed
2. Install required dependencies:
```bash
pip install pygame
```

## Usage
1. Run the main menu:
```bash
python Menu.py
```
2. Click to place generation points on the maze
3. Select your preferred pathfinding algorithm:
   - A* for optimal pathfinding
   - BFS for shortest path guarantee
   - DFS for memory-efficient exploration
4. Watch the algorithm explore and solve the maze!

## Technical Details
- Built with Python and Pygame
- Implements three classic pathfinding algorithms
- Features a custom maze generation algorithm
- Includes real-time visualization of algorithm execution
- Provides performance metrics (generation time, solve time, path length)

## Author
Bogdan F Andrei
Liverpool John Moores University
Dissertation Project 2024

## License
MIT License
