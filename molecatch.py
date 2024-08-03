import pygame, os, random, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션
size = (1000, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MOLE_CATCH")

# 3. 게임 내 설정
clock = pygame.time.Clock()
black = (0,0,0)
white = (255, 255, 255)
x_list = [165, 500, 830]
y_list = [248, 580, 916]

        
def tup_r(tup):
    temp_list = []
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)

bg = pygame.image.load("bg.png")
bg = pygame.transform.smoothscale(bg, size)
mole_1 = pygame.image.load("mole_1.png")
mole_2 = pygame.image.load("mole_2.png")
mole_size = mole_1.get_size()
mole_size = tup_r((mole_size[0]*0.25, mole_size[1]*0.25))
mole_1 = pygame.transform.smoothscale(mole_1, mole_size)
mole_2 = pygame.transform.smoothscale(mole_2, mole_size)
hammer = pygame.image.load("hammer.png")
hammer_size = hammer.get_size()
hammer_size = tup_r((hammer_size[0]*0.1, hammer_size[1]*0.1))
hammer = pygame.transform.smoothscale(hammer, hammer_size)
hammer_stage = 0
hammer_stay = 200
hammer_rotation = 0

class mole:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.img = mole_1
        self.crop = 0
        self.move = 7
        self.stage = 0
        self.time = 200
        self.clicked = False
        self.size = mole_size
        
    def crop_change(self):
        if self.stage == 0:
            if random.random() < 0.1: self.stage = 1
        elif self.stage == 1:
            self.crop += self.move
            if self.crop > self.size[1]: 
                self.stage = 2
                self.crop = self.size[1]
                self.stay_start = now_time
        elif self.stage == 2:
            if now_time - self.stay_start >= self.time:
                self.stage = 3
        elif self.stage == 3:
            self.crop -= self.move
            if self.crop < 0:
                self.crop = 0
                self.stage = 0
                self.img = mole_1
                self.clicked = False
        self.croped = self.img.subsurface((0,0,self.size[0], self.crop))
        self.pos = tup_r((x_list[self.i]-self.size[0]/2, y_list[self.j]-self.crop))
        self.range = (self.pos[0], self.pos[1], self.size[0], self.crop)

    def show(self):
        screen.blit(self.croped, self.pos)

moles = []
for i in range(3):
    for j in range(3):
        moles.append(mole(i,j))

click = False
exit = False
# 4. 메인 이벤트
while not exit:
    
    # 4-1. FPS설정
    clock.tick(60)
    
    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = True
            
            
    # 4-3. 입력, 시간에 따른 변화
    now_time = pygame.time.get_ticks()
    
    if hammer_stage == 0:
        if hammer_rotation != 0:
            hammer = pygame.transform.rotate(hammer, -hammer_rotation)
            hammer_rotation = 0
        x, y = pygame.mouse.get_pos()
        hammer_pos = (x - hammer_size[0] / 2, y - hammer_size[1] / 2)
        if click:
            hammer_stage = 1
            stay_time = now_time
    elif hammer_stage == 1:
        if hammer_rotation != 90:
            hammer = pygame.transform.rotate(hammer, 90 - hammer_rotation)
            hammer_rotation = 90
        x, y = pygame.mouse.get_pos()
        hammer_pos = (x - hammer_size[0] / 2, y - hammer_size[1] / 2)
        if now_time - stay_time >= hammer_stay:
            hammer_stage = 0
    
    for mole_obj in moles:
        mole_obj.crop_change()
        
        if click == True:
            for mole_obj in moles:
                if mole_obj.clicked == False:
                    x, y = pygame.mouse.get_pos()
                    x1,y1,w,h = mole_obj.range
                    if x >= x1 and x <= x1+w and y >= y1 and y <= y1+h:
                        mole_obj.clicked = True
                        mole_obj.stage = 3
                        mole_obj.img = mole_2
            click = False
    # 4-4. 그리기
    screen.blit(bg, (0,0))
    for mole_obj in moles:
        mole_obj.show()
    screen.blit(hammer, hammer_pos)
    x,y = pygame.mouse.get_pos()
    hammer_pos = (x-hammer_size[0]/2, y-hammer_size[1]/2)
    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
pygame.quit()