import pygame
import main_menu
import background

pygame.init()
screen = pygame.display.set_mode((1280, 720)) # ความละเอียดของเกม 1280x720
clock = pygame.time.Clock()
title = pygame.display.set_caption('Magic Type') # 
running = True
dt = 0

while running:
    # pygame.QUIT event means the user clicked X to close your window
    # ปิดหน้าตัวเกม
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # flip() the display to put your work on screen
    pygame.display.flip()
    pygame.display.update()
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
