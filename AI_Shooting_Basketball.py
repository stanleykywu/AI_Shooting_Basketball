import sys, pygame, random, math, os
from Ball import Ball
pygame.init()

base_path = os.path.dirname(__file__)
hoop_path = os.path.join(base_path, "images/hoop.png")
background_path = os.path.join(base_path, "images/background.jpg")

HOOP = pygame.image.load(hoop_path)
BACKGROUND = pygame.image.load(background_path)

HOOP = pygame.transform.scale(HOOP, (100, 100))
BACKGROUND = pygame.transform.scale(BACKGROUND, (1000, 684))

size = width, height = 1000, 684

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
    rand_y = random.randint(250, 584)
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