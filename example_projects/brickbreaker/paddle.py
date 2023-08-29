import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
