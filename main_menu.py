import pygame
import sys
import random #ใช้สุ่มตำแหน่งดาวหรือเอฟเฟกต์
pygame.init()
pygame.display.set_caption("Magic Type")
screen = pygame.display.set_mode((1280, 720)) 
clock = pygame.time.Clock() #ควบคุมความเร็วเฟรมของเกม
font = pygame.font.SysFont(None, 120) 
small_font = pygame.font.SysFont(None, 55)

#สร้างตัวเเปรบอก สถานะ อยู่หน้าไหนของเกม
state = "menu"
buttons = [("Start", 320), ("Setting", 420), ("Quit", 520)]
 
#สุ่มจุดแสงเล็กๆ สำหรับพื้นหลัง
stars = []
for i in range(50): #สร้างจุดดาวแบบสุ่ม 50 ดวง
#ฟังก์ชันหลักที่ใช้ในการสุ่มตัวเลข ใน Python
    x = random.randint(0, 800) 
    y = random.randint(0, 600)
    r = random.randint(1, 3) #จำนวนเต็มใช้บอกขนาด
    s = random.uniform(0.5, 1.5) #สุ่มความเร็วดาว
    stars.append([x, y, r, s])

bg_image = pygame.image.load("mainpic.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (1280, 720))
def draw_colorful_background(): 
    global color_shift
    color_shift = (color_shift + 1) % 765  #ตัวหมุนสีค่าระหว่าง 0-765 (255*3) เกิน 765 ให้กลับมาเริ่มที่ 0 อัตโนมัติ
def draw_colorful_background():
    screen.blit(bg_image, (0, 0)) #วาดรูปเป็นพื้นหลัง

#วาดดาวให้เคลื่อนที่บนพื้นหลัง
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), star[2])
        star[1] += star[3]
        if star[1] > 1280:
            star[1] = 0
            star[0] = random.randint(0, 1280)
         
def draw_menu(): 
    draw_colorful_background()
    title = font.render("Magic Type", True, (255, 255, 255))
    shadow = font.render("Magic Type", True, (0, 0, 0))
    screen.blit(shadow, (412, 94))
    screen.blit(title, (410, 90))

#ตำเเหน่งเมาส์ในตัวเเปร ตั้งค่าเริ่มต้นไว้ก่อนว่ายังไม่คลิกเมาส์
    mouse = pygame.mouse.get_pos()
    click = False
#ตรวจจับเหตุการณ์ต่างๆ การคลิก, ปิดหน้าต่าง
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True 

#วนลูปสร้างปุ่มทั้งหมด แต่ละปุ่มมีกรอบสี่เหลี่ยมไว้ตรวจการคลิก
    for text, y in buttons:
        rect = pygame.Rect(520, y, 240, 70) 
        color = (140, 180, 230) if rect.collidepoint(mouse) else (220, 120, 60)
        pygame.draw.rect(screen, color, rect, border_radius=15)  #ปุ่มสี่เหลี่ยมพร้อมมุมโค้ง
        txt = small_font.render(text, True, (0, 0, 10)) 
        txt_rect = txt.get_rect(center=rect.center)  #วางตัวอักษรตรงกลางเหมือนกรอบสี่เหลี่ยม
        screen.blit(txt, txt_rect)
 
        if rect.collidepoint(mouse) and click:  #ตรวจว่าผู้ใช้คลิกบนปุ่มนั้นหรือไม่
            if text == "Start": return "game"
            elif text == "Setting": return "setting"
            elif text == "Quit": pygame.quit(); sys.exit()
    return "menu"  #ถ้าไม่ได้กดปุ่มไหนเลย จะยังคงอยู่ที่หน้าเมนูเหมือนเดิม

#จอสีดำ แสดงหัวข้อกลางหน้าจอ
def draw_page(label):
    screen.fill((10, 10, 10))   #พื้นหลังของหน้าจอให้เป็นสีดำเข้ม
    head = font.render(label, True, (255, 255, 255))  #สร้างข้อความชื่อหน้าเกม จากตัวแปร label
    screen.blit(head, (530, 150))  #ข้อความแสดงบนหน้าจอ
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
    screen.blit(back_txt, (back_rect.x + 45, back_rect.y + 15))
#ถ้าคลิกปุ่ม “Back” → กลับไปหน้าเมนู
    if back_rect.collidepoint(mouse) and click:
        return "menu"
    return label.lower()

#ลูปหลักทำงานตลอดเวลา (เกมจะอยู่ในลูปนี้จนกว่าจะปิด)
while True:
    if state == "menu":
        state = draw_menu()
    elif state == "game":
        state = draw_page("GAME")
    elif state == "setting":
        state = draw_page("SETTING")

    pygame.display.update() #เเสดงหน้าจอผลทั้งหมด
    clock.tick(60) #ความเร็วเกมไม่เกิน60เฟรมต่อวิ ไม่เคลื่อนเร็วเกิน
