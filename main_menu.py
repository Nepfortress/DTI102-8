import pygame
import sys
pygame.init()
pygame.display.set_caption("Magic Type")
screen = pygame.display.set_mode((1920, 1080))
font = pygame.font.SysFont(None, 80)

state = "menu"
buttons = [("Start", 500), ("Setting", 600), ("Quit", 700)]

def draw_menu():    
    screen.fill((0, 70, 50))
    title = font.render("Magic Type", True, (255, 255, 255))
    screen.blit(title, (800, 300))

    mouse = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

    for text, y in buttons:
        rect = pygame.Rect(800, y, 300, 80)
        color = (100, 100, 150) if rect.collidepoint(mouse) else (70, 70, 100)
        pygame.draw.rect(screen, color, rect, border_radius=10)

        txt = font.render(text, True, (255, 255, 255))
        screen.blit(txt, (rect.x + 50, rect.y + 8))

        if rect.collidepoint(mouse) and click:
            if text == "Start":  return "game"
            if text == "Setting": return "setting"
            if text == "Quit": pygame.quit(); sys.exit()
    return "menu"

def draw_black(label):
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()  
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "menu"
    return label.lower()

while True:
    if state == "menu":
        state = draw_menu()
    elif state == "game":
        state = draw_black("GAME")
    elif state == "setting":
        state = draw_black("SETTING")
    pygame.display.update()
