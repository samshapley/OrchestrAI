import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.lives = 3
        self.font = pygame.font.Font(None, 36)

        self.paddle = Paddle(self)
        self.ball = Ball(self)
        self.bricks = [Brick(self, i*60, j*30) for i in range(14) for j in range(10)]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.paddle.speed = -6
                elif event.key == pygame.K_RIGHT:
                    self.paddle.speed = 6
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    self.paddle.speed = 0

    def update(self):
        self.paddle.move()
        self.ball.move()
        self.check_collision()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.paddle.draw()
        self.ball.draw()
        for brick in self.bricks:
            brick.draw()
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        self.screen.blit(score_text, (20, 550))
        self.screen.blit(lives_text, (700, 550))
        pygame.display.flip()

    def check_collision(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.bounce(1, -1)
        for brick in self.bricks:
            if brick.alive and self.ball.rect.colliderect(brick.rect):
                self.ball.bounce(1, -1)
                brick.destroy()
                self.score += 10
        if self.ball.rect.left < 0 or self.ball.rect.right > self.width:
            self.ball.bounce(-1, 1)
        if self.ball.rect.top < 0:
            self.ball.bounce(1, -1)
        if self.ball.rect.bottom > self.height:
            self.lives -= 1
            if self.lives == 0:
                self.running = False
            else:
                self.ball.reset()

    def reset(self):
        self.score = 0
        self.lives = 3
        self.ball.reset()
        for brick in self.bricks:
            brick.reset()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()