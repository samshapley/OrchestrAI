from brick import Brick

class BrickLayer:
    def __init__(self):
        self.bricks = [Brick(x, y) for x in range(50, 800, 60) for y in range(50, 250, 30)]
    
    def draw(self, screen):
        for brick in self.bricks:
            brick.draw(screen)
    
    def check_collision(self, ball):
        for brick in self.bricks:
            if brick.rect.colliderect(ball.rect):
                self.bricks.remove(brick)
                ball.bounce()
                break
