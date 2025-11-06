import pygame
import sys
import random #ใช้สุ่มตำแหน่งดาวหรือเอฟเฟกต์
pygame.init()
pygame.display.set_caption("Magic Type")
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock() #ใช้ควบคุมความเร็วเฟรมของเกม
font = pygame.font.SysFont(None, 80)
small_font = pygame.font.SysFont(None, 50)

#สร้างตัวเเปรบอก สถานะ อยู่หน้าไหนของเกม
state = "menu"
buttons = [("Start", 320), ("Setting", 420), ("Quit", 520)]
 
# สุ่มจุดแสงเล็ก ๆ สำหรับพื้นหลัง
stars = []
for i in range(50):
    x = random.randint(0, 1280)
    y = random.randint(0, 720)
    r = random.randint(1, 3)
    s = random.uniform(0.5, 1.5) #ความเร็วเคลื่อนที่
    stars.append([x, y, r, s])

# สีพื้นหลังเริ่มต้น หมุนเฉดสีพื้นหลังเพื่อให้ค่อยๆเปลี่ยนสี
color_shift = 0
def draw_colorful_background():
    global color_shift
    color_shift = (color_shift + 1) % 765  # หมุนค่าระหว่าง 0-765

    # ไล่สีแบบไปกลับ: จากแดง → เขียว → น้ำเงิน → กลับมาแดง
    if color_shift < 255:
        r = 255
        g = color_shift
        b = 0
    elif color_shift < 510:
        r = 510 - color_shift
        g = 255
        b = color_shift - 255
    else:
        r = 0
        g = 765 - color_shift
        b = 255

    color1 = (r // 2, g // 2, b // 2)  # สีเข้มสำหรับด้านบน
    color2 = (r, g, b)                 # สีสดสำหรับด้านล่าง

    # วาดพื้นหลังแบบไล่สี
    for y in range(720):
        ratio = y / 720
        red = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        green = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        blue = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(screen, (red, green, blue), (0, y), (1280, y))

    # วาดดาว
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), star[2])
        star[1] += star[3]
        if star[1] > 720:
            star[1] = 0
            star[0] = random.randint(0, 1280)
def draw_menu(): #แสดงหน้าเมนูหลักของเกม
    draw_colorful_background()  
    title = font.render("Magic Type", True, (255, 255, 255))
    screen.blit(title, (480, 200))

#ตำเเหน่งเมาส์ในตัวเเปร ตั้งค่าเริ่มต้นไว้ก่อนว่ายังไม่คลิกเมาส์
    mouse = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True 

#วนลูปสร้างปุ่มทั้งหมดจากลิสต์ buttons แต่ละปุ่มมีกรอบสี่เหลี่ยมไว้ตรวจการคลิก
    for text, y in buttons:
        rect = pygame.Rect(520, y, 240, 70) #สร้างกรอบสี่เหลี่ยม
        color = (255, 180, 80) if rect.collidepoint(mouse) else (220, 120, 60)     #เมาส์อยู่บนปุ่ม ให้เปลี่ยนสีให้สว่างขึ้นเล็กน้อยเพื่อให้รู้ว่ากำลังชี้อยู่
        pygame.draw.rect(screen, color, rect, border_radius=15)  #วาดปุ่มเป็นสี่เหลี่ยมสีที่กำหนดไว้ พร้อมมุมโค้งเล็กน้อย
        txt = small_font.render(text, True, (30, 30, 30)) #วาดข้อความชื่อปุ่มลงบนกรอบปุ่ม
        screen.blit(txt, (rect.x + 70, rect.y + 18))

        if rect.collidepoint(mouse) and click:
            if text == "Start": return "game"
            elif text == "Setting": return "setting"
            elif text == "Quit": pygame.quit(); sys.exit()
    return "menu"

#จอเป็นสีดำ แล้วแสดงหัวข้อกลางหน้าจอ
def draw_page(label):
    screen.fill((10, 10, 10))
    head = font.render(label, True, (255, 255, 255))
    screen.blit(head, (530, 200))
    
    mouse = pygame.mouse.get_pos()
    click = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True

#สร้างปุ่มBack ให้ผู้เล่นกดกลับไปเมนูหลัก
    back_rect = pygame.Rect(50, 600, 180, 60)
    color = (200, 60, 60) if back_rect.collidepoint(mouse) else (150, 40, 40)
    pygame.draw.rect(screen, color, back_rect, border_radius=10)
    back_txt = small_font.render("Back", True, (255, 255, 255))
    screen.blit(back_txt, (back_rect.x + 55, back_rect.y + 15))
#ถ้าคลิกปุ่ม “Back” → กลับไปหน้าเมนู
    if back_rect.collidepoint(mouse) and click:
        return "menu"
    return label.lower()

while True:
    if state == "menu":
        state = draw_menu()
    elif state == "game":
        state = draw_page("GAME")
    elif state == "setting":
        state = draw_page("SETTING")

    pygame.display.update() 
    clock.tick(60) #ความเร็วเกมไม่เกิน60เฟรมต่อวิ ไม่เคลื่อนเร็วเกิน
