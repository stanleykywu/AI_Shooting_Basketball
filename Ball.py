import pygame, math, os

base_path = os.path.dirname(__file__)
ball_path = os.path.join(base_path, "images/ball.gif")

BALL = pygame.image.load(ball_path)
BALL = pygame.transform.scale(BALL, (100, 100))

vel = 50

class Ball:

    def __init__(self, x, y, theta):
        self.x = x
        self.y = y
        self.vel = vel
        self.x_vel = self.vel * math.cos(theta)
        self.y_vel = -1 * self.vel * math.sin(theta)
        self.img_count = 0
        self.img = BALL
        self.gravity = 2

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.y_vel += self.gravity

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))