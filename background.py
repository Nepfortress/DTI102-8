import pygame

# madebyverycuteperson

softmountain = pygame.image.load("softmountain.png")
def backgroundImg(softmountain):
    softmountain = pygame.transform.scale(softmountain, (1920, 1080))
    pygame.screen.blit(softmountain, (0, 0))
