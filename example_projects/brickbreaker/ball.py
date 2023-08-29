import pygame
from random import randint

class Ball:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.dx = 1 if randint(0, 1) == 0 else -1
        self.dy = -1

    def move(self, paddle, bricks):
        self.rect.move_ip(self.dx * 5, self.dy * 5)
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.colliderect(paddle.rect):
            self.dy *= -1
        for row in bricks:
            for brick in row:
                if brick is not None and self.rect.colliderect(brick.rect):
                    self.dy *= -1
                    row[row.index(brick)] = None
                    break

    def draw(self, surface):
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        pygame.draw.ellipse(surface, self.color, self.rect)
