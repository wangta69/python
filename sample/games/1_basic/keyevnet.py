import sys
import pygame
from pygame.locals import *
# https://wikidocs.net/64781
pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
FPSCLOCK = pygame.time.Clock()

pos_x = 200
pos_y = 150
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                pos_x -= 5
            elif event.key == K_RIGHT:
                pos_x += 5
            elif event.key == K_UP:
                pos_y -= 5
            elif event.key == K_DOWN:
                pos_y += 5

    SURFACE.fill((0, 0, 0))

    pygame.draw.rect(SURFACE, (0, 0, 255), Rect(pos_x, pos_y, 100, 50))

    pygame.display.update()
    FPSCLOCK.tick(30)