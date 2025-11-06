import pygame
import sys  #ใช้ปิดโปรแกรมออกจากระบบ ปิดหน้าต่าง
import random #ใช้สุ่มตำแหน่งดาวหรือเอฟเฟกต์
pygame.init()
pygame.display.set_caption("Magic Type")
screen = pygame.display.set_mode((1920, 1080)) #ขนาดหน้าจอ
clock = pygame.time.Clock() #ใช้ควบคุมความเร็วเฟรมของเกม
font = pygame.font.SysFont(None, 80) #ตัวใหญ่ไว้สำหรับหัวข้อ
small_font = pygame.font.SysFont(None, 50) # ตัวเล็กสำหรับข้อความปุ่ม

#สร้างตัวเเปรบอก สถานะ อยู่หน้าไหนของเกม
state = "menu" #กำหนดสถานะเริ่มต้นของเกมให้เป็น “หน้าเมนูหลัก”
buttons = [("Start", 320), ("Setting", 420), ("Quit", 520)]
 
# สุ่มจุดแสงเล็ก ๆ สำหรับพื้นหลัง
stars = []
for i in range(50):
    x = random.randint(0, 1280) #ตำแหน่ง
    y = random.randint(0, 720) #ตำแหน่ง
    r = random.randint(1, 3) #ขนาด
    s = random.uniform(0.5, 1.5) #ความเร็วเคลื่อนที่
    stars.append([x, y, r, s])

# สีพื้นหลังเริ่มต้น หมุนเฉดสีพื้นหลังเพื่อให้ค่อยๆเปลี่ยนสี
color_shift = 0
def draw_colorful_background(): #วาดพื้นหลังแบบไล่สีและดาวเคลื่อนไหว
    global color_shift
    color_shift = (color_shift + 0.5) % 360  #ทำให้ค่าสีหมุนวน 0–360องศา เป็นเอฟเฟกต์เปลี่ยนสีไปเรื่อย ๆ
    color1 = pygame.Color(0) #สร้างสีสองเฉดโดยใช้ระบบสีHSVA (เฉด, ความอิ่มสี, ความสว่าง, ความโปร่งใส)เพื่อใช้ทำการไล่สีพื้นหลัง
    color1.hsva = (color_shift, 70, 50, 100)
    color2 = pygame.Color(0)
    color2.hsva = ((color_shift + 60) % 360, 70, 80, 100)

    # วาดพื้นหลังแบบไล่สี (gradient) วาดเส้นแนวนอนแต่ละบรรทัดเพื่อสร้าง “เอฟเฟกต์ไล่สี” จากบนลงล่าง
    for y in range(720):
        ratio = y / 720
        r = int(color1.r * (1 - ratio) + color2.r * ratio)
        g = int(color1.g * (1 - ratio) + color2.g * ratio)
        b = int(color1.b * (1 - ratio) + color2.b * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (1280, y))
    
    # วาดแสงดาว ดาวสีขาวทำให้ดาวตกลงมา ถ้าดาวตกพ้นขอบล่างให้กลับขึ้นไปข้างบนอีกครั้ง
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), star[2])
        star[1] += star[3]
        if star[1] > 720:
            star[1] = 0
            star[0] = random.randint(0, 1280)

def draw_menu(): #แสดงหน้าเมนูหลักของเกม
    draw_colorful_background()  # พื้นหลังสีสันไล่สีที่มีดาวเคลื่อนไหว
    title = font.render("Magic Type", True, (255, 255, 255))
    screen.blit(title, (480, 200))

#ตำเเหน่งเมาส์ในตัวเเปร ตั้งค่าเริ่มต้นไว้ก่อนว่ายังไม่คลิกเมาส์
    mouse = pygame.mouse.get_pos()
    click = False

#ตรวจจับเหตุการณ์ต่างๆ การคลิก, ปิดหน้าต่าง
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True #กดเมาส์ซ้ายตั้งค่า click ให้เป็นจริง เพื่อใช้ว่าผู้เล่นคลิกปุ่ม

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

#ล้างจอเป็นสีดำ แล้วแสดงหัวข้อกลางหน้าจอ
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

# ลูปหลักทำงานตลอดเวลา (เกมจะอยู่ในลูปนี้จนกว่าจะปิด)
while True:
    if state == "menu":
        state = draw_menu()
    elif state == "game":
        state = draw_page("GAME")
    elif state == "setting":
        state = draw_page("SETTING")

    pygame.display.update()  #เเสดงหน้าจอผลทั้งหมด
    clock.tick(60) #ความเร็วเกมไม่เกิน60เฟรมต่อวิ ไม่เคลื่อนเร็วเกิน
