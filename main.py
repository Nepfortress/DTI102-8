# Magic Type

import pygame
from display import *
from background import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_length, screen_width))
clock = pygame.time.Clock()
title = pygame.display.set_caption("Debian")
running = True
dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with Monument Valley
    screen.fill((0, 0, 0))
    screen.blit(valley, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
