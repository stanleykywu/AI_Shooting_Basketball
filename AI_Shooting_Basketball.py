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

def draw_screen(screen, balls, rand_x, rand_y):
    screen.blit(BACKGROUND, (0,0))
    for ball in balls:
        ball.draw(screen)
    draw_hoop(screen, [rand_x, rand_y])
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
    if ball.x > 1000 or ball.x < 0 or ball.y > 684:
        return True
    return False

def inBucket(ball, rand_x, rand_y):
    middle_x = ball.x + 50
    middle_y = ball.y + 50
    if rand_x + 20 <= middle_x <= rand_x + 100 and rand_y + 20 <= middle_y <= rand_y + 100:
        return True
    return False

def nearBucket(ball, rand_x, rand_y):
    middle_x = ball.x + 50
    middle_y = ball.y + 50
    if rand_x - 50 <= middle_x <= rand_x + 150 and rand_y - 50 <= middle_y <= rand_y + 150:
        return True
    return False

def all_stop(balls):
    for ball in balls:
        if ball.x_vel != 0 and ball.y_vel != 0:
            return False

    return True

def single_player(genome, config):
    rand_y = random.randint(250, 584)
    # rand_x = random.randint(500, 900)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    output = net.activate([(rand_y - 250)/ 334])
    angle = output[0] * 2 * math.pi
    vel = output[1] * 50

    # print(angle, vel)

    ball = Ball(0, 584, angle, vel)

    run = True;
    while(run):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()

        if ball.x_vel == 0 and ball.y_vel == 0 or offScreen(ball):
            run = False
            break

        if inBucket(ball, 900, rand_y):
            ball.x_vel = 0
            ball.y_vel = 0
            break

        ball.move()
        
        draw_screen(screen, [ball], 900, rand_y)

def eval_genome(genomes, config):
    rand_y = random.randint(250, 584)
    # rand_x = random.randint(500, 900)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)

    ge = []
    balls = []

    # create all balls and neural network assosciated with the ball
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)

        output = net.activate([(rand_y - 250)/ 334])
        angle = output[0] * 2 * math.pi
        vel = output[1] * 50
        # print(angle, vel)

        balls.append(Ball(0, 584, angle, vel))
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
                ge[x].fitness -= 10
                balls.pop(x)
                ge.pop(x)
        
        for x, ball in enumerate(balls):
            if nearBucket(ball, 900, rand_y):
                ge[x].fitness += 5
            if inBucket(ball, 900, rand_y):
                ge[x].fitness += 10
                ball.x_vel = 0
                ball.y_vel = 0
        
        # for x, ball in enumerate(balls):
        #     ge[x].fitness += ball.x / 10000

        for ball in balls:
            ball.move()
        
        draw_screen(screen, balls, 900, rand_y)

def initiate_training(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter();
    p.add_reporter(stats)

    winner = p.run(eval_genome, 50)
    
    print('\nBest genome:\n{!s}'.format(winner))

    for i in range(10):
        single_player(winner, config)

if __name__ == "__main__":
    config_path = os.path.join(base_path, "config-feedforward.txt")
    initiate_training(config_path)
