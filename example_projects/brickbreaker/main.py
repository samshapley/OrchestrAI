import pygame
import os
import sys
from gamewindow import GameWindow
from paddle import Paddle
from ball import Ball
from brick import Brick
from score import Score

def check_game_over(ball, bricks):
    if ball.rect.bottom >= 600:
        return True
    for row in bricks:
        for brick in row:
            if brick is not None:
                return False
    return True

def main_loop():
    pygame.init()
    clock = pygame.time.Clock()
    window = GameWindow(800, 600)
    paddle = Paddle(350, 550, 100, 20)
    ball = Ball(400, 300, 10, 10)
    bricks = [[Brick(100 * i + 50, 50 * j + 50, 80, 30) for i in range(8)] for j in range(4)]
    score = Score(0)

    while not check_game_over(ball, bricks):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        paddle.move()
        ball.move(paddle, bricks)
        score.update(bricks)
        window.draw(paddle, ball, bricks, score)
        pygame.display.update()
        clock.tick(60)
    window.draw_game_over()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                os.execv(sys.executable, ['python'] + sys.argv)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main_loop()
