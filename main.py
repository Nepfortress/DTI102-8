import pygame
import sys
import random
import time
import math

pygame.init()
pygame.mixer.init() # เริ่มต้นใช้ mixer

# ตัวแปร Global
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magic Type')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 120)
small_font = pygame.font.SysFont(None, 65) # ปรับขนาดของฟอนต์ให้ชัดเจนมากขึ้น
tiny_font = pygame.font.SysFont(None, 35)

# สถานะของเกม
STATE = "menu" # ตัวแปร STATE คือ หน้า menu ของเกม

# สี
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
RED = (200, 60, 60)
LIGHT_RED = (150, 40, 40)
BUTTON_DEFAULT = (220, 120, 60)
BUTTON_HOVER = (140, 180, 230)
BG_COLOR = (30, 30, 60)
SLIDER_BAR_COLOR = (180, 180, 200)

# เพลง
pygame.mixer.music.load("kfcnmagicsound.mp3")
pygame.mixer.music.play(-1) # ลูปไม่จำกัดเพื่อเล่นเพลง

# ตัวแปรส่วนกลางสำหรับการตั้งค่าและเกม
VOLUME = 0.5 # สำหรับการเริ่มต้นใช้เสียง
pygame.mixer.music.set_volume(VOLUME) 
DRAGGING = False # สถานะสำหรับการควบคุมเสียงโดยการสไลด์ตัวปุ่มปรับระดับเสียง

# โหลดตัว Assets ของเกมม
bg_image = pygame.image.load("mainpic.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
background_game = pygame.image.load("softmountain.png").convert()
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))
character_img = pygame.image.load("boy.png").convert_alpha()
character_img = pygame.transform.scale(character_img, (150, 150))
background_setting = pygame.image.load("river1.jpg").convert()
background_setting = pygame.transform.scale(background_setting, (WIDTH, HEIGHT))

char_rect = character_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 40))

# ตัวแปรของเกม
game_circles = []
normal_speed = 2
fall_speed = normal_speed
slow_mode = False
slow_start_time = 0
slow_duration = 10  
last_green_time = 0
last_blue_time = 0
time_counter = 0
SCORE = 0 # ติดตามคะแนนของผู้เล่น

# ฟังก์ชันรีเซต
def reset_game_state():
    """Resets all variables specific to the 'game' state for a fresh start."""
    global game_circles, fall_speed, slow_mode, slow_start_time, last_green_time, last_blue_time, time_counter, SCORE
    game_circles = []
    fall_speed = normal_speed
    slow_mode = False
    slow_start_time = 0
    last_green_time = 0
    last_blue_time = 0
    time_counter = 0
    SCORE = 0 # Reset score
    print("Game state has been reset.")


# วาดตัววงกลม
def create_circle(x, y, color, letter, radius=30):
    return {"x": x, "y": y, "color": color, "letter": letter, "radius": radius}

def draw_circle(circle):
    pygame.draw.circle(screen, circle["color"], (circle["x"], int(circle["y"])), circle["radius"])
    text = small_font.render(circle["letter"], True, BLACK)
    text_rect = text.get_rect(center=(circle["x"], int(circle["y"])))
    screen.blit(text, text_rect)

def update_circle(circle):
    circle["y"] += fall_speed

# ฟังก์ชันสำหรับวาดภาพ

def draw_colorful_background(): 
    """Draws the main menu background with moving stars."""
    screen.blit(bg_image, (0, 0))
    for star in stars:
        pygame.draw.circle(screen, WHITE, (int(star[0]), int(star[1])), star[2])
        star[1] += star[3]
        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)
         
def draw_menu(): 
    """Draws the main menu interface."""
    global STATE
    draw_colorful_background()
    title = font.render("Magic Type", True, WHITE)
    shadow = font.render("Magic Type", True, BLACK)
    screen.blit(shadow, (412, 94))
    screen.blit(title, (410, 90))

    mouse = pygame.mouse.get_pos()
    click = False
    new_state = "menu"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True 

    for text, y in menu_buttons:
        rect = pygame.Rect(520, y, 240, 70) 
        color = BUTTON_HOVER if rect.collidepoint(mouse) else BUTTON_DEFAULT
        pygame.draw.rect(screen, color, rect, border_radius=15)
        txt = small_font.render(text, True, BLACK) 
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)
 
        if rect.collidepoint(mouse) and click:
            if text == "Start": 
                reset_game_state() # รีเซตสถานะของเกมเมื่อเริ่มต้น
                new_state = "game"
            elif text == "Setting": new_state = "setting"
            elif text == "Quit": pygame.quit(); sys.exit()
    
    return new_state

def draw_page(label):
    """
    Draws the Settings screen with the Volume Slider.
    """
    global VOLUME, DRAGGING
    
    mouse = pygame.mouse.get_pos()
    new_state = label.lower() # อยู่ในการตั้งค่าเว้นเสียแต่ไม่ถูกเปลี่ยนแปลง

    # การจัดการกับอีเวนท์สำหรับตัวสไลด์ปรับเสียง และการออกจากการตั้งค่า
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # กดปุ่ม 'Esc' เพื่อไปที่เมนูหลัก
            return "menu" 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if mouse clicked on the slider area
            slider_hitbox_rect = pygame.Rect(250, 400 - 20, 700, 14 + 40) # Add padding for easier clicking
            if slider_hitbox_rect.collidepoint(mouse):
                 DRAGGING = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            DRAGGING = False

    # วาดภาพพื้นหลังและชื่อเกม
    screen.blit(background_setting, (0, 0))

    shadow = font.render(label, True, BLACK)
    title = font.render(label, True, WHITE)
    title_x = WIDTH // 2 - title.get_width() // 2

    screen.blit(shadow, (title_x + 7, 154))
    screen.blit(title, (title_x, 150))

    # ขนาดของตัวสไลด์เสียง
    slider_x, slider_y = 250, 400
    slider_width, slider_height = 700, 14
    knob_radius = 20
    
    # วาดภาพตัวบาร์เลื่อนเสียงเพลง
    pygame.draw.rect(screen, SLIDER_BAR_COLOR, (slider_x, slider_y, slider_width, slider_height))
    
    # คำนวณและวาดภาพตัวลูกบิด
    knob_x = slider_x + int(slider_width * VOLUME)
    pygame.draw.circle(screen, WHITE, (knob_x, slider_y + slider_height // 2), knob_radius)

    # ลอจิกของตัวสไลด์เสียงเพลง
    if DRAGGING:
        # จำกัดค่าเมาส์ไม่ให้เลื่อนเลยตัวสไลด์ของตัวตั้งค่าเพลง
        mouse_x = mouse[0]
        if slider_x <= mouse_x <= slider_x + slider_width:
            VOLUME = (mouse_x - slider_x) / slider_width
            pygame.mixer.music.set_volume(VOLUME)
        # ถ้าลากออกIf dragging outside, clamp to the ends
        elif mouse_x < slider_x:
            VOLUME = 0.0
            pygame.mixer.music.set_volume(VOLUME)
        elif mouse_x > slider_x + slider_width:
            VOLUME = 1.0
            pygame.mixer.music.set_volume(VOLUME)

    # ข้อความปรับตัวเปอร์เซ็นของตัวเสียงเพลง
    vol_text = small_font.render(f"Volume: {int(VOLUME * 100)}%", True, WHITE)
    vol_x = WIDTH // 2 - vol_text.get_width() // 2
    screen.blit(vol_text, (vol_x, 460))
    
    # วาด 'Back' hint เมื่อผู้ใช้กดปุ่ม EscDraw
    back_hint = tiny_font.render("Press ESC to return to Menu", True, BLACK)
    screen.blit(back_hint, (50, 650))
    
    return new_state # การอยู่ในหน้าการตั้งค่า

def run_game():
    # ฟังก์ชันนี้ไว้สำหรับลอจิกตัวอักขระตก
    global game_circles, fall_speed, slow_mode, slow_start_time, last_green_time, last_blue_time
    global time_counter, SCORE # ใช้สำหรับคะแนน score ที่เป็น global

    current_time = time.time()
    new_state = "game"

    # ตัวจัดการอีเวนต์
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                reset_game_state() # รีเซตตัวคะแนนเมื่อออกจากเกม
                return "menu" 
                
            key_pressed = event.unicode.upper()

            for circle in game_circles[:]:
                if key_pressed == circle["letter"]:
                    # อัปเดตคะแนนเมื่อกดแป้นพิมพ์ได้ถูกต้อง
                    SCORE += 10 
                    
                    if circle["color"] == GREEN:
                        slow_mode = True
                        slow_start_time = time.time()
                        fall_speed = 0.5
                    elif circle["color"] == BLUE:
                        game_circles.clear()
                        break
                    game_circles.remove(circle)
                    break 

    # โหมดของตกช้าลง
    if slow_mode and current_time - slow_start_time >= slow_duration:
        slow_mode = False
        fall_speed = normal_speed

    # ลอจิกสำหรับการเกิดของตัวอักษรที่ตกลงมา
    if random.random() < 0.01:
        letter = chr(random.randint(65, 90))
        normal_circle = create_circle(random.randint(50, WIDTH - 50), 0, WHITE, letter, radius=35)
        game_circles.append(normal_circle)
        
    if current_time - last_green_time > 30:
        letter = chr(random.randint(65, 90))
        green_circle = create_circle(random.randint(50, WIDTH - 50), 0, GREEN, letter)
        game_circles.append(green_circle)
        last_green_time = current_time

    if current_time - last_blue_time > 60:
        letter = chr(random.randint(65, 90))
        blue_circle = create_circle(random.randint(50, WIDTH - 50), 0, BLUE, letter)
        game_circles.append(blue_circle)
        last_blue_time = current_time

    # วาดภาพและอัปเดตภาพ
    time_counter += 0.2
    breathe = math.sin(time_counter) * 3
    
    screen.blit(background_game, (0, 0))
    
    # แสดงคะแนนปัจจุบัน
    score_text = small_font.render(f"Score: {SCORE}", True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
    
    screen.blit(character_img, (char_rect.x, char_rect.y + breathe))

    for circle in game_circles[:]:
        update_circle(circle)
        draw_circle(circle)
        
        # เงื่อนไขเกมโอเวอร์
        if circle["y"] > HEIGHT:
            new_state = "game_over" # เปลี่ยนสถานะถ้าวงกลมตกเลยขอบด้านล่างของจอภาพ
            break # ออกจากลูปวงกลมเมื่อเกมโอเวอร์จากของตก
        
    return new_state

def draw_game_over():
    # แสดงภาพ Game Over และแสดงว่าให้รีเซต์หรือกลับไปที่หน้าเมนูของเกม
    screen.fill(BLACK) 
    
    title = font.render("GAME OVER", True, RED)
    score_text = small_font.render(f"FINAL SCORE: {SCORE}", True, WHITE)
    restart_text = tiny_font.render("Press ENTER to RESTART", True, GRAY)
    menu_text = tiny_font.render("Press ESC to RETURN TO MENU", True, GRAY)

    # วาดข้อความตรงกลางหน้าจอ
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4 + 70))
    
    screen.blit(title, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(menu_text, menu_rect)
    
    # การจัดลำดับเหตุการณ์สำหรับเกมโอเวอร์
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # กดปุ่ม ENTER เพื่อเล่นเกมใหม่อีกที
                reset_game_state()
                return "game"
            elif event.key == pygame.K_ESCAPE: # กดปุ่ม ESC เพื่อไปที่ Menu หลักของเกม
                reset_game_state()
                return "menu"
                
    return "game_over" # จะอยู่ในหน้าเกมโอเวอร์ถ้าไม่ได้กดคีย์บนแป้นพิมพ์

# ตัวแปรของเมนู
menu_buttons = [("Start", 320), ("Setting", 420), ("Quit", 520)]
stars = []
for i in range(50):
    x = random.randint(0, WIDTH) 
    y = random.randint(0, HEIGHT)
    r = random.randint(1, 3)
    s = random.uniform(0.5, 1.5)
    stars.append([x, y, r, s])
    
# ลูปหลักของเกม
while True:
    if STATE == "menu":
        STATE = draw_menu()
    elif STATE == "game":
        STATE = run_game()
    elif STATE == "setting":
        STATE = draw_page("SETTING") 
    elif STATE == "game_over":
        STATE = draw_game_over()
        
    pygame.display.update() 
    clock.tick(60)

pygame.quit()
sys.exit()
