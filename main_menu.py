import pygame
import sys #ใช้ปิดโปรแกรมออกจากระบบ ปิดหน้าต่าง
import random #ใช้สุ่มตำแหน่งดาวหรือเอฟเฟกต์
pygame.init()
pygame.display.set_caption("Magic Type")
screen = pygame.display.set_mode((1280, 720)) #ขนาดหน้าจอ
clock = pygame.time.Clock() #ใช้ควบคุมความเร็วเฟรมของเกม
font = pygame.font.SysFont(None, 120)  #ตัวใหญ่ไว้สำหรับหัวข้อ
small_font = pygame.font.SysFont(None, 55) #ตัวเล็กสำหรับข้อความปุ่ม

#สร้างตัวเเปรบอก สถานะ อยู่หน้าไหนของเกม
state = "menu" #กำหนดสถานะเริ่มต้นของเกมให้เป็น “หน้าเมนูหลัก”
buttons = [("Start", 320), ("Setting", 420), ("Quit", 520)]
 
#สุ่มจุดแสงเล็กๆ สำหรับพื้นหลัง
stars = []
for i in range(50):#สร้างจุดดาวแบบสุ่ม 50 ดวง
#ฟังก์ชันหลักที่ใช้ในการสุ่มตัวเลข ใน Python
    x = random.randint(0, 800) #ตำแหน่ง สุ่มจำนวนเต็ม
    y = random.randint(0, 600)
    r = random.randint(1, 3) #ขนาด จำนวนเต็ม
    s = random.uniform(0.5, 1.5) #ความเร็วดาวหมุนความโปร่งใส จำนวนทศนิยมเหมาะกับค่าที่ต้องการความละเอียด
    stars.append([x, y, r, s])

bg_image = pygame.image.load("mainpic.jpg").convert()
bg_image = pygame.transform.scale(bg_image, (1280, 720))
def draw_colorful_background(): #ฟังก์ชันนี้สามารถแก้ไขตัวแปร color_shift ที่อยู่นอกฟังก์ชันได้เนื่องจากต้องเพิ่มค่า color_shift ทุกเฟรมเพื่อเปลี่ยนสีพื้นหลังแบบอนิเมชัน ถ้าไม่มีglobalพื้นหลังจะไม่เปลี่ยนสี
    global color_shift
    color_shift = (color_shift + 1) % 765  #ตัวหมุนสีค่าระหว่าง 0-765 (255*3) เกิน 765 ให้กลับมาเริ่มที่ 0 อัตโนมัติ
    screen.blit(bg_image, (0, 0)) #วาดรูปเป็นพื้นหลัง
#ตัวแปร color_shift จะเพิ่มค่าทีละ 1 ทุกเฟรมและถูกจำกัดไว้ระหว่าง 0 ถึง 765 ด้วยการใช้ modulo ค่านี้ใช้หมุนสี RGB ทีละช่วง ทำให้พื้นหลังค่อยๆเปลี่ยนสีไปเรื่อยๆไม่สะดุดเพราะแต่ละช่วงของ 765 หน่วยตรงกับการเปลี่ยนสีของ Red, Green และ Blue ตามลำดับ

#วาดดาวให้เคลื่อนที่บนพื้นหลัง
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (int(star[0]), int(star[1])), star[2])
        star[1] += star[3]
        if star[1] > 1280:
            star[1] = 0
            star[0] = random.randint(0, 1220)
         
def draw_menu(): #แสดงหน้าเมนูหลักของเกม
    draw_colorful_background()  #พื้นหลังสีสันไล่สีที่มีดาวเคลื่อนไหว
    title = font.render("Magic Type", True, (255, 255, 255))
    shadow = font.render("Magic Type", True, (0, 0, 0))
    screen.blit(shadow, (412, 94))
    screen.blit(title, (410, 90))

#ตำเเหน่งเมาส์ในตัวเเปร ตั้งค่าเริ่มต้นไว้ก่อนว่ายังไม่คลิกเมาส์
    mouse = pygame.mouse.get_pos() #พิกัดเมาส์
    click = False
#ตรวจจับเหตุการณ์ต่างๆ การคลิก, ปิดหน้าต่าง
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True  #กดเมาส์ซ้ายตั้งค่า click ให้เป็นจริง เพื่อใช้ว่าผู้เล่นคลิกปุ่ม

#วนลูปสร้างปุ่มทั้งหมดจากลิสต์ buttons แต่ละปุ่มมีกรอบสี่เหลี่ยมไว้ตรวจการคลิก
    for text, y in buttons:
        rect = pygame.Rect(520, y, 240, 70) #สร้างกรอบสี่เหลี่ยม
        color = (255, 180, 80) if rect.collidepoint(mouse) else (220, 120, 60)     #คำสั่งสำคัญตรวจว่าเมาส์อยู่ในพื้นที่ของกรอบสี่เหลี่ยมมั้ย
        pygame.draw.rect(screen, color, rect, border_radius=15)  #วาดปุ่มเป็นสี่เหลี่ยมสีที่กำหนดไว้ พร้อมมุมโค้งเล็กน้อย
        txt = small_font.render(text, True, (30, 30, 30)) #สีตัวอักษร
        screen.blit(txt, (rect.x + 70, rect.y + 18))  #วางข้อความไว้ตรงกลางปุ่ม
 
        if rect.collidepoint(mouse) and click:  #ตรวจว่าผู้ใช้คลิกบนปุ่มนั้นหรือไม่
            if text == "Start": return "game"
            elif text == "Setting": return "setting"
            elif text == "Quit": pygame.quit(); sys.exit()
    return "menu"  #ถ้าไม่ได้กดปุ่มไหนเลย จะยังคงอยู่ที่หน้าเมนูเหมือนเดิม

#จอสีดำ แสดงหัวข้อกลางหน้าจอ
def draw_page(label):
    screen.fill((10, 10, 10))   #พื้นหลังของหน้าจอให้เป็นสีดำเข้ม
    head = font.render(label, True, (255, 255, 255))  #สร้างข้อความชื่อหน้าเกม จากตัวแปร label
    screen.blit(head, (530, 200))  #ข้อความแสดงบนหน้าจอ
    
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
