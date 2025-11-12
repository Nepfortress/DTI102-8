#ตัวละคร
import pygame
import math

pygame.init()

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic type")

character = pygame.image.load("boy.png").convert_alpha()
character = pygame.transform.scale(character, (128, 128))
char_rect = character.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
clock = pygame.time.Clock()
time = 0
running = True
white = (255, 255, 255)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(white)
    time += 0.25
    breathe = math.sin(time) * 4
    screen.fill((white))
    screen.blit(character, (char_rect.x, char_rect.y + breathe))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
