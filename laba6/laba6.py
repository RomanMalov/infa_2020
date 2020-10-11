import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
h = screen.get_height()
w = screen.get_width()
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
balls = []
time = 0
super_exist = False

def new_ball():
    global balls
    '''рисует новый шарик '''
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(30, 100)
    vx = randint(-10, 10)
    vy = randint(-10, 10)

    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    balls.append([x, y, r, vx, vy, color])
def super_ball():
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(30, 100)
    vx = randint(-10, 10)
    vy = randint(-10, 10)

    color = COLORS[randint(0, 5)]

pygame.display.update()
clock = pygame.time.Clock()
finished = False
lose = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            finished = True
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            if not lose:
                mouse_x, mouse_y = event.pos
                new_balls = []
                for ball in balls:
                    if not (ball[0]-mouse_x)**2+(ball[1]-mouse_y)**2<=(ball[2]**2):
                        new_balls.append(ball)
                balls = new_balls
    if not lose:
        for ball in balls:
            ball[0] += ball[3]
            ball[1] += ball[4]

            circle(screen, ball[5], (ball[0], ball[1]), ball[2])
            if ball[0] >= w or ball[0] <= 0:
                ball[3] *= -1
            if ball[1] >= h or ball[1] <= 0:
                ball[4] *= -1

    if time % 50 == 0 and not lose:
        new_ball()

    pygame.display.update()
    screen.fill(BLACK)
    time += 1
    f1 = pygame.font.Font(None, 36)
    f2 = pygame.font.Font(None, 360)

    text1 = f1.render('Time: ' + str(int(time/6)/10), 1, (180, 180, 180))
    if len(balls)>=10:
        lose = True
        screen.fill(BLACK)
        text3 = f2.render('WASTED', 1, (255, 30, 40))
        screen.blit(text3, (w/2, h/2))

    if len(balls)>0:
        text2 = f1.render('Number of balls: ' + str(len(balls)), 1, ((255*len(balls)/10) % 255, (255*(10-len(balls))/10) % 255, 0))
    else:
        text2 = f1.render('Number of balls: ' + str(len(balls)), 1, (0, 0, 255))
    if not lose:
        screen.blit(text1, (10, 50))
        screen.blit(text2, (w-300, 50))

pygame.quit()
