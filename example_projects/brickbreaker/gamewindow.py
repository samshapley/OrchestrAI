import pygame

class GameWindow:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height))
        self.font = pygame.font.Font(None, 36)

    def draw(self, paddle, ball, bricks, score):
        self.surface.fill((0, 0, 0))
        paddle.draw(self.surface)
        ball.draw(self.surface)
        for row in bricks:
            for brick in row:
                if brick is not None:
                    brick.draw(self.surface)
        score.draw(self.surface)

    def draw_game_over(self):
        self.surface.fill((0, 0, 0))
        text = self.font.render("Game Over", 1, (255, 255, 255))
        button = pygame.draw.rect(self.surface, (0, 255, 0), (350, 300, 100, 50))
        button_text = self.font.render("Play Again", 1, (0, 0, 0))
        self.surface.blit(text, (350, 250))
        self.surface.blit(button_text, (355, 310))
