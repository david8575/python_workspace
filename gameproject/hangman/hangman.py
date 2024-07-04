import pygame, math, random
# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [500, 900]
screen = pygame.display.set_mode(size)
title = "HANG_MAN"
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()

black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)

hint_font = pygame.font.Font("C:/Users/david/AppData/Local/Microsoft/Windows/Fonts/BMDOHYEON_ttf.ttf", 80)
entry_font = pygame.font.Font("C:/Users/david/AppData/Local/Microsoft/Windows/Fonts/BMDOHYEON_ttf.ttf", 60)
no_font = pygame.font.Font("C:/Users/david/AppData/Local/Microsoft/Windows/Fonts/BMDOHYEON_ttf.ttf", 40)

f = open("C:/Users/david/Desktop/SeHun/python_workplace/gameproject/hangman/voca.txt", "r", encoding='UTF-8')
raw_data = f.read()
f.close()
data_list = raw_data.split("\n")
data_list = data_list[:-1]
while True:
    r_index = random.randrange(0, len(data_list))
    word = data_list[r_index].replace(u"\xa0", u" ").split(" ")[1]
    if len(word) <= 6:
        break

def tup_r(tup):
    temp_list = []
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)

exit = False
drop = False
enter_go = False

try_num = 0
entry_text = ""
cnt = 0
word = word.upper()
word_show = "_" * len(word)
ok_list = []
no_list = []

# 4. 메인 이벤트
while not exit:
    # 4-1. FPS 설정
    clock.tick(60)
    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if (key_name == "return" or key_name == "enter"):
                if entry_text != "" and (ok_list + no_list).count(entry_text) == 0:
                    enter_go = True
            elif len(key_name) == 1:
                if (ord(key_name) >= 65 and ord(key_name) <= 90) or (ord(key_name) >= 97 and ord(key_name) <= 122):
                    entry_text = key_name.upper()
                else: entry_text = ""
            else: entry_text = ""
            
    # 4-3. 입력, 시간에 따른 변화
    if try_num == 8: 
        cnt+=1
        word_show = word
    if enter_go == True:
        ans = entry_text
        result = word.find(ans)
        if result == -1: 
            try_num+=1
            no_list.append(ans)
        else:
            ok_list.append(ans)
            for i in range(len(word)):
                if word[i] == ans:
                    word_show = word_show[:i] + ans + word_show[i+1:]
        enter_go = False
        entry_text = ""
    # 4-4. 그리기
    screen.fill(white)
    A = tup_r((0, size[1]*2/3))
    B = (size[0], A[1])
    C = tup_r((size[0]/6, A[1]))
    D = (C[0], C[0])
    E = tup_r((size[0]/2, D[0]))
    F = tup_r((E[0], E[1] + size[0]/6))
    r_head = round(size[0]/12)
    if drop: G = (F[0], F[1] + r_head + cnt*5)
    else : G = (F[0], F[1] + r_head)
    H = (G[0], G[1] + r_head)
    I = (H[0], H[1] + r_head)
    l_arm = r_head*2
    J = tup_r(
        (I[0]-l_arm*math.cos(30*math.pi/180), 
        I[1]+l_arm*math.sin(30*math.pi/180))
    )
    K = tup_r(
        (I[0]+l_arm*math.cos(30*math.pi/180), 
        I[1]+l_arm*math.sin(30*math.pi/180))
    )
    L = (I[0], I[1] + l_arm)
    l_leg = l_arm*1.5
    M = tup_r(
        (L[0]-l_leg*math.cos(60*math.pi/180), 
         L[1]+l_leg*math.sin(60*math.pi/180))
    )
    N = tup_r(
        (L[0]+l_leg*math.cos(60*math.pi/180), 
        L[1]+l_leg*math.sin(60*math.pi/180))
    )
    pygame.draw.line(screen, black, A, B, 3)
    pygame.draw.line(screen, black, C, D, 3)
    pygame.draw.line(screen, black, D, E, 3)
    if drop == False:
        pygame.draw.line(screen, black, E, F, 3)
    if try_num >= 1: pygame.draw.circle(screen, black, G, r_head, 3)
    if try_num >= 2: pygame.draw.line(screen, black, H, I, 3)
    if try_num >= 3: pygame.draw.line(screen, black, I, K, 3)
    if try_num >= 4: pygame.draw.line(screen, black, I, J, 3)
    if try_num >= 5:pygame.draw.line(screen, black, I, L, 3)
    if try_num >= 6:pygame.draw.line(screen, black, L, M, 3)
    if try_num >= 7:pygame.draw.line(screen, black, L, N, 3)
    if drop == False and try_num == 8:
        O = tup_r((size[0]/2-size[0]/6, E[1]/2+F[1]/2))
        P = (O[0] + cnt*2, O[1])
        if P[0] > size[0]/2+size[0]/6:
            P = tup_r((size[0]/2+size[0]/6, O[1]))
            drop = True
            cnt = 0
        pygame.draw.line(screen, red, O, P, 3)
        
    # 4-5. 힌트 표시하기
    hint = hint_font.render(word_show, True, black)
    hint_size = hint.get_size()
    hint_pos = tup_r((size[0]/2-hint_size[0]/2, size[1]*5/6-hint_size[1]/2))
    screen.blit(hint, hint_pos)
    
    # 4-6. 입력창 표시하기
    entry = entry_font.render(entry_text, True, white)
    entry_size = entry.get_size()
    entry_pos = tup_r((size[0]/2-entry_size[0]/2, size[1]*17/18-entry_size[1]/2))
    entry_bg_size = 80
    pygame.draw.rect(screen, black, tup_r((size[0]/2-entry_bg_size/2,
                                     size[1]*17/18-entry_bg_size/2,
                                     entry_bg_size,entry_bg_size)))
    screen.blit(entry,entry_pos)
    
    # 4-7. 오답 표시하기
    no_text = " ".join(no_list)
    no = no_font.render(no_text, True, red)
    no_pos = tup_r((20, size[1]*2/3+20))
    screen.blit(no,no_pos)
    
    # 4-8. 업데이트
    pygame.display.flip()
    
# 5. 게임종료
pygame.quit()