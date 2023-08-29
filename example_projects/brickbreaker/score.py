import pygame

class Score:
    def __init__(self, score):
        self.score = score
        self.font = pygame.font.Font(None, 36)

    def update(self, bricks):
        for row in bricks:
            if None in row:
                self.score += 1
                row.remove(None)

    def draw(self, surface):
        text = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
        surface.blit(text, (10, 10))
