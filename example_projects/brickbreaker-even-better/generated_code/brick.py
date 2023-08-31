import pygame

class Brick:
    def __init__(self, game, x, y):
        self.width, self.height = 50, 20
        self.game = game
        self.alive = True
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def destroy(self):
        self.alive = False

    def reset(self):
        self.alive = True

    def draw(self):
        if self.alive:
            pygame.draw.rect(self.game.screen, (255, 255, 255), self.rect)
