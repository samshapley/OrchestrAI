import pygame

class Ball:
    def __init__(self, game):
        self.width, self.height = 15, 15
        self.dx, self.dy = 1, -1
        self.speed = 2
        self.game = game
        self.rect = pygame.Rect(game.width // 2, game.height // 2, self.width, self.height)

    def move(self):
        self.rect.move_ip(self.dx * self.speed, self.dy * self.speed)

    def bounce(self, dx, dy):
        self.dx, self.dy = self.dx * dx, self.dy * dy

    def reset(self):
        self.rect = pygame.Rect(self.game.width // 2, self.game.height // 2, self.width, self.height)
        self.dx, self.dy = 1, -1

    def draw(self):
        pygame.draw.ellipse(self.game.screen, (255, 255, 255), self.rect)