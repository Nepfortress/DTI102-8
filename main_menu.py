import pygame
import sys  #ระบบปฎิบัติการปิดหน้าต่าง ออกจากเกม
pygame.init()
pygame.display.set_caption("Magic Type")
screen = pygame.display.set_mode((1920, 1080))
font = pygame.font.SysFont(None, 80)

#สร้างตัวเเปรบอก สถานะ อยู่หน้าไหนของเกม
state = "menu"
buttons = [("Start", 500), ("Setting", 600), ("Quit", 700)] #สร้างปุ่ม

def draw_menu():  #ฟังก์ชันเมนูหลัก
    screen.fill((0, 70, 50)) #RBG
    title = font.render("Magic Type", True, (255, 255, 255))
    screen.blit(title, (800, 300))

#ตำเเหน่งเมาส์ในตัวเเปร ตั้งค่าเริ่มต้นไว้ก่อนว่ายังไม่คลิกเมาส์
    mouse = pygame.mouse.get_pos()
    click = False

#ถ้าผู้ใช้กดปุ่มปิดหน้าต่าง จะออกจากเกมทันที
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = True  #กดเมาส์ซ้ายตั้งค่า click ให้เป็นจริง เพื่อใช้ตรวจว่าผู้เล่นคลิกปุ่ม

#ตรวจจับว่าเมาส์ชี้โดนปุ่มหรือยัง
    for text, y in buttons:      #วนลูปปุ่มจากตัวแปร buttons เพื่อเอามาแสดงบนหน้าจอ
        rect = pygame.Rect(800, y, 300, 80) #สร้างกรอบสี่เหลี่ยม
        color = (100, 100, 150) if rect.collidepoint(mouse) else (70, 70, 100)    #เมาส์อยู่บนปุ่ม ให้เปลี่ยนสีให้สว่างขึ้นเล็กน้อยเพื่อให้รู้ว่ากำลังชี้อยู่
        pygame.draw.rect(screen, color, rect, border_radius=10)   #วาดปุ่มเป็นสี่เหลี่ยมสีที่กำหนดไว้ พร้อมมุมโค้งเล็กน้อย

        txt = font.render(text, True, (255, 255, 255))   #สีตัวอักษร
        screen.blit(txt, (rect.x + 50, rect.y + 8))  #วางข้อความไว้ตรงกลางปุ่ม

        if rect.collidepoint(mouse) and click:   #ตรวจว่าผู้ใช้คลิกบนปุ่มนั้นหรือไม่
            if text == "Start":  return "game"
            if text == "Setting": return "setting"
            if text == "Quit": pygame.quit(); sys.exit()
    return "menu"    #ถ้าไม่ได้กดปุ่มไหนเลย จะยังคงอยู่ที่หน้าเมนูเหมือนเดิม

def draw_black(label):     #ฟังก์ชันภาพหลังสีดำ
    screen.fill((0,0,0))
    for event in pygame.event.get():   #ตรวจเหตุการณ์
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()  
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #ถ้าผู้เล่นกดปุ่ม ESC ให้กลับไปหน้า "menu"
            return "menu"     #ถ้ากดปุ่ม ESC ให้กลับไปหน้าเมนู
    return label.lower()   #ถ้าไม่ได้กดอะไรเลย ให้คงสถานะเดิมไว้

while True:
    if state == "menu":
        state = draw_menu()
    elif state == "game":
        state = draw_black("GAME")
    elif state == "setting":
        state = draw_black("SETTING")
    pygame.display.update()    #เเสดงหน้าจอผลทั้งหมด
