import sys, pygame, random, math, os
pygame.init()

base_path = os.path.dirname(__file__)
ball_path = os.path.join(base_path, "images/ball.gif")
hoop_path = os.path.join(base_path, "images/hoop.png")
background_path = os.path.join(base_path, "images/background.jpg")

BALL = pygame.image.load(ball_path)
HOOP = pygame.image.load(hoop_path)
BACKGROUND = pygame.image.load(background_path)

BALL = pygame.transform.scale(BALL, (100, 100))
HOOP = pygame.transform.scale(HOOP, (100, 100))
BACKGROUND = pygame.transform.scale(BACKGROUND, (1000, 684))

size = width, height = 1000, 684
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
          

def draw_hoop(screen, position):
    screen.blit(HOOP, (position[0], position[1]))

def draw_screen(screen, balls, rand_y):
    screen.blit(BACKGROUND, (0,0))
    for ball in balls:
        ball.draw(screen)
    draw_hoop(screen, [900, rand_y])
    pygame.display.update()

def check_win(balls, rand_y):
    for ball in balls:
        middle_x = ball.x + 100
        middle_y = ball.y + 100
        if 920 <= middle_x <= 990 and rand_y + 20 <= middle_y <= rand_y + 80:
            return True
    return False

def check_lose(balls):
    for ball in balls:
        if ball.x > 1000 or ball.x < 0 or ball.y > 684 or ball.y < 0:
            return True
    return False

def driver():
    rand_y = random.randint(100, 584)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    press = None
    balls = []

    screen.blit(BACKGROUND, (0,0))
    pygame.display.update()

    run = True;
    while(run):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                press = pygame.mouse.get_pos()

        if press is not None:
            balls.append(Ball(0, 584, math.atan((684 - press[1]) / press[1])))

            press = None
    
        for ball in balls:
            ball.move()

        draw_screen(screen, balls, rand_y)
        
        if check_win(balls, rand_y):
            run = False
        elif check_lose(balls):
            driver()

    pygame.quit()
    quit()

driver()