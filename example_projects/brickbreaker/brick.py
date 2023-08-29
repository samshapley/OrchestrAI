import pygame
from random import randint

class Brick:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
