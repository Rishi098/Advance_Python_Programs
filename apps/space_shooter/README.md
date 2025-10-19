# Astro Space Game

A 2D space shooter game featuring arcade-style gameplay, colorful visuals, thrilling asteroid waves, power-ups, and immersive sound effects.

## Game Flow

### Screens and Transitions

- **Splash Screen**: A short animation of the Astro Space logo with background music.
- **Main Menu**: Start Game, Best Score, Instructions, Settings, Quit.
- **Best Score**: Displays the highest score achieved.
- **Instructions**: Shows controls, game objective, and guide to power-ups.
- **Gameplay Screen**: Main arena where player, asteroids, bullets interact.
- **Pause Menu**: Allows resume, return to main menu, or quit.
- **Game Over Screen**: Displays final score and buttons to Retry or Exit.

## Requirements

- Python 3.6+
- Pygame 2.0+

## Installation

1. Install the required packages:
   ```
   pip install pygame
   ```
2. Run the game:
   ```
   cd AstroSpace
   python main.py
   ```

## Core Gameplay Mechanics

### Controls

- **Arrow keys** or **W/A/S/D**: Move ship.
- **Space**: Fire bullet (hold for continuous fire).
- **P**: Pause game.
- **M**: Mute background music and effects.
- **X**: Energy Blast.
- **F1**: Full Screen.

### Player Mechanics

- Starts with 3 lives.
- Fires bullets at fixed intervals (cooldown).
- Collision with asteroid: lose one life and trigger temporary invincibility.

### Asteroid Mechanics

- Spawn from top of screen at random positions.
- Rotate while falling to simulate tumbling in space.
- Vary in speed and movement patterns.
- Appear with increasing frequency as time progresses.

### Collision Detection

- Bullet hits asteroid: Destroy both, add score, play boom sound.
- Asteroid hits player: Reduce life, trigger invincibility, subtract points.

## Power-Ups

Spawn randomly from destroyed asteroids:

| Name        | Visual Hint   | Effect                           |
| ----------- | ------------- | -------------------------------- |
| Double Shot | Purple square | Fires two bullets simultaneously |
| Shield      | Blue square   | Temporary invincibility          |
| Speed Boost | Yellow square | Increases ship movement speed    |
| Extra Life  | Red square    | Adds one life to player's count  |

## Level Design / Difficulty

Dynamic difficulty system:

- Asteroid speed increases every 15 seconds.
- Enemy frequency increases over time.
- Score increases as you destroy more asteroids.

## Scoring System

| Action                   | Points |
| ------------------------ | ------ |
| Destroy an asteroid      | +10    |
| Survive every 30 seconds | +50    |
| Collect a power-up       | +20    |
| Hit by asteroid          | -50    |

- Score cannot go below zero.
- High score is saved between game sessions.
- Floating score text animations when points are gained or lost.

## UI Elements

### Main Menu

- Buttons for Start Game, Best Score, Instructions, Settings, and Quit.

### Best Score Screen

- Displays the highest score achieved.
- Back button to return to main menu.

### Instructions Page

- Shows controls and game mechanics.
- Explains power-ups and scoring system.

### Pause Menu

- Dark semi-transparent overlay.
- Centered "Paused" text with Resume, Main Menu, Quit buttons.

### Game Over Screen

- Fade to black after player loses all lives.
- Shows "Mission Failed" or "New High Score!" depending on score.
- Displays final score and best score.
- Retry and Main Menu buttons.


## Project Structure

```
AstroSpace/
│
├── assets/               # All images, sounds, and fonts
│   ├── images/           # Spaceships, asteroids, stars, etc.
│   ├── sounds/           # Laser shots, explosion, background music
│   └── fonts/            # Custom game fonts
│
├── main.py               # Main game loop and core logic
├── player.py             # Handles player spaceship movement and actions
├── enemy.py              # Enemy logic and spawn behavior
├── bullet.py             # Bullet and collision handling
├── config.py             # Game settings like screen size, speed, etc.
├── utils.py              # Helper functions (e.g., loading assets)
└── README.md             # Project overview and instructions
```
