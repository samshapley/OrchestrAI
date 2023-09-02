import pygame

class Paddle:
    def __init__(self, game):
        self.width, self.height = 100, 20
        self.speed = 0
        self.game = game
        self.rect = pygame.Rect(game.width // 2 - self.width // 2, game.height - self.height - 30, self.width, self.height)

    def move(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.width:
            self.rect.right = self.game.width

    def draw(self):
        pygame.draw.rect(self.game.screen, (255, 255, 255), self.rect)