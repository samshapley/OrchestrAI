import pygame
from paddle import Paddle
from ball import Ball
from brick_layer import BrickLayer

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.paddle = Paddle()
        self.ball = Ball()
        self.brick_layer = BrickLayer()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        elif keys[pygame.K_RIGHT]:
            self.paddle.move_right()
        self.ball.move()
        if self.paddle.check_collision(self.ball):
            self.ball.bounce()
        self.brick_layer.check_collision(self.ball)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.brick_layer.draw(self.screen)
        pygame.display.flip()

    def is_running(self):
        return self.running
