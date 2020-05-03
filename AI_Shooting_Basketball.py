import sys, pygame, random, math, os, neat
from Ball import Ball
pygame.init()

base_path = os.path.dirname(__file__)
hoop_path = os.path.join(base_path, "images/hoop.png")
background_path = os.path.join(base_path, "images/background.jpg")

HOOP = pygame.transform.scale(pygame.image.load(hoop_path), (100, 100))
BACKGROUND = pygame.transform.scale(pygame.image.load(background_path), (1000, 684))

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

def offScreen(ball):
    if ball.x > 1000 or ball.x < 0 or ball.y > 684 or ball.y < 0:
        return True
    return False

def inBucket(ball, rand_y):
    middle_x = ball.x + 100
    middle_y = ball.y + 100
    if 920 <= middle_x <= 990 and rand_y + 20 <= middle_y <= rand_y + 80:
        return True
    return False

def all_stop(balls):
    for ball in balls:
        if ball.x_vel != 0 and ball.y_vel != 0:
            return False

    return True

def single_player():
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

def eval_genome(genomes, config):
    rand_y = random.randint(250, 584)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    ge = []
    balls = []

    # create all balls and neural network assosciated with the ball
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        output = net.activate([rand_y])
        xChange = 684 - output[1]
        yChange = output[0]
        # print(xChange, yChange)
        if yChange == 0:
            angle = math.pi / 4
        else:
            angle = math.atan(yChange / yChange)

        balls.append(Ball(0, 584, angle))
        g.fitness = 0
        ge.append(g)

    run = True;
    while(run):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()

        if len(balls) == 0 or all_stop(balls):
            run = False
            break

        for x, ball in enumerate(balls):
            if offScreen(ball):
                ge[x].fitness -= 2
                balls.pop(x)
                ge.pop(x)
            elif inBucket(ball, rand_y):
                ge[x].fitness += 2
                ball.x_vel = 0
                ball.y_vel = 0
        
        # for x, ball in enumerate(balls):
        #     ge[x].fitness += 0.01

        for ball in balls:
            ball.move()
        
        draw_screen(screen, balls, rand_y)

def initiate_training(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter();
    p.add_reporter(stats)

    winner = p.run(eval_genome, 50)
    
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    config_path = os.path.join(base_path, "config-feedforward.txt")
    initiate_training(config_path)
