import pygame

# https://www.peppercarrot.com/0_sources/0ther/wallpapers/hi-res/2017-04-10_Only-Komona_by-David-Revoy.jpg
bg = pygame.image.load("2017-04-10_Only-Komona_by-David-Revoy.jpg")
def backgroundImg(bg):
    size = pygame.transform.scale(bg, (1920, 1080))
    screen.blit(size, (0, 0))

# Merge this later

"""
# madebyverycuteperson
import pygame
pygame.init() 
pygame.display.set_caption("Magic type") 

WHITE =(255,255,255)
RED =(255,0,0)
GREEN =(0,255,0)


screen = pygame.display.set_mode((1920,1080))
# screen.fill(WHITE)

softmoutain=pygame.image.load("magicimg/softmoutain.png")
softmoutain= pygame.transform.scale(softmoutain,(1920,1080))

# pygame.draw.rect(screen,WHITE,(80,100,250,50))


running = True
while running:
    for event in pygame.event.get():
     if event.type == pygame.QUIT:
        running==False
    
    screen.blit(softmoutain,(0,0))
    pygame.display.update()
pygame.quit()
"""
