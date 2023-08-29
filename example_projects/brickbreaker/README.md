# Pygame Brick Breaker Game Enhanced Version

## Description
This project is an enhanced implementation of the classic Brick Breaker game using the `pygame` library in Python. Players control a paddle to bounce a ball and break bricks. The game ends when all bricks are destroyed or if the ball touches the bottom edge of the screen. This version features a more comprehensive game window, scoring system, and game over detection.

The codebase contains the following files:
- `main.py`: This is the entry point of the application. It initializes game elements, runs the main game loop, and controls the framerate. It also checks for game over conditions and triggers the game over display.
- `game.py`: This file defines the `Game` class which encapsulates the main game logic, including event handling, game state updating, and drawing game elements on the screen.
- `paddle.py`: Defines the `Paddle` class, which includes methods for moving the paddle left and right and checking collision with the ball.
- `ball.py`: Defines the `Ball` class, handling the movement of the ball and bouncing it when it hits a wall, paddle or brick.
- `brick.py`: Defines the `Brick` class, representing a brick that the ball can collide with and destroy. Each brick is randomly colored for visual variety.
- `brick_layer.py`: Defines the `BrickLayer` class, which is a collection of bricks. It checks for collision between the bricks and the ball, and removes any brick that collides with the ball.
- `score.py`: Defines the `Score` class, which tracks and displays the player's score. The score increases every time a brick is destroyed.
- `gamewindow.py`: Defines the `GameWindow` class, which sets up the game window, draws all game elements on the screen, and displays the game over text and button.

## How to Run
Before running the game, make sure the `pygame` library is installed. If not, install it using pip:

```bash
pip install pygame
```

To run the game, navigate to the directory containing these files and execute the `main.py` file with Python:

```bash
python main.py
```

## Controls
- Use the left and right arrow keys to move the paddle.
- The ball moves automatically, bouncing off the paddle and walls.
- The game ends when all bricks are broken or when the ball touches the bottom edge of the screen. A "Game Over" message will be displayed along with a "Play Again" button.

## Game Logic and Structure
The game management is done by the `main_loop` function in `main.py`, which creates instances of `GameWindow`, `Paddle`, `Ball`, `Brick`, and `Score`, and runs the main game loop.

`Paddle`, `Ball`, and `Brick` objects each have a `rect` attribute, provided by the `pygame` library, which represents their position and size. These attributes are used for drawing the objects on the screen, moving them, and checking for collisions.

The `Score` object tracks and displays the player's score, which is increased every time a brick is destroyed.

The `GameWindow` object sets up the game window, draws all game elements on the screen, and displays the game over message and button when the game ends.

## Customization
The sizes, positions, and movement speeds of game elements can be adjusted by changing the corresponding values in the `__init__` methods of their respective classes. The colors of the bricks and ball are randomly generated for each game for a more visually interesting experience.