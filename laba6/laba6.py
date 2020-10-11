import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
h = screen.get_height()
w = screen.get_width()
WHITE = (255, 255, 255)
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
super_vx = 0
super_vy = 0
super_x = 0
super_y = 0


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


pygame.display.update()
clock = pygame.time.Clock()
finished = False
lose = False
while not finished:
    clock.tick(FPS)
    count = len(balls) + super_exist
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
                    if not (ball[0] - mouse_x) ** 2 + (ball[1] - mouse_y) ** 2 <= (ball[2] ** 2):
                        new_balls.append(ball)
                balls = new_balls
            if super_exist:
                if (time // 10) % 2 == 0:
                    if 0<(-super_x+mouse_x)<200 and 0<(-super_y+mouse_y)<(time % 10 * 20 + 20):
                        super_exist = False

    if not lose:
        for ball in balls:
            ball[0] += ball[3]
            ball[1] += ball[4]

            circle(screen, ball[5], (ball[0], ball[1]), ball[2])
            if ball[0] >= w or ball[0] <= 0:
                ball[3] *= -1
            if ball[1] >= h or ball[1] <= 0:
                ball[4] *= -1
        if super_exist:
            if (time // 10) % 2 == 0:
                super_surface1 = pygame.transform.scale(super_surface, (200, time % 10 * 20 + 20))
            else:
                super_surface1 = pygame.transform.scale(super_surface, (time % 10 * 20 + 20, 200))
            super_x += super_vx
            super_y += super_vy
            if super_x >= w or super_x <= 0:
                super_vx *= -1
            if super_y >= h or super_y <= 0:
                super_vy *= -1
            screen.blit(super_surface1, (super_x, super_y))

    if time % 50 == 0 and not lose:
        if count == 4 and not super_exist:
            super_exist = True
            super_x = randint(100, 1100)
            super_y = randint(200, 600)
            super_vx = randint(-10, 10)
            super_vy = randint(-10, 10)
            super_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
            super_surface.fill((255, 255, 255, 0))
            polygon(super_surface, WHITE, [[0, 100], [100, 200], [200, 100], [100, 0]])


        else:
            new_ball()

    pygame.display.update()
    screen.fill(BLACK)
    time += 1
    f1 = pygame.font.Font(None, 36)
    f2 = pygame.font.Font(None, 360)

    text1 = f1.render('Time: ' + str(int(time / 6) / 10), 1, (180, 180, 180))
    if count >= 10:
        lose = True
        screen.fill(BLACK)
        text3 = f2.render('WASTED', 1, (255, 30, 40))
        screen.blit(text3, (w / 2-500, h / 2-300))

    if count > 0:
        text2 = f1.render('Number of balls: ' + str(count), 1,
                          ((255 * count / 10) % 255, (255 * (10 - count) / 10) % 255, 0))
    else:
        text2 = f1.render('Number of balls: ' + str(count), 1, (0, 0, 255))
    if not lose:
        screen.blit(text1, (10, 50))
        screen.blit(text2, (w - 300, 50))

pygame.quit()
