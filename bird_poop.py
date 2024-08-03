import pygame, os, math, random
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

size = (800, 900)
screen = pygame.display.set_mode(size)
title = "새똥 피하기"
pygame.display.set_caption(title)

def tup_r(tup):
    temp_list = []
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)

def image_read(file_name, resize):
    img = pygame.image.load(file_name + ".png")
    img_size = img.get_size()
    img_size = (img_size[0] * resize, img_size[1] * resize)
    img = pygame.transform.smoothscale(img, img_size)
    return img

class person:
    def __init__(self):
        self.img = person_static
        self.size = self.img.get_size()
        self.pos = tup_r((size[0] / 2 - person_size[0] / 2, size[1] - person_size[1]))
        self.move = 10
        self.timer = 0
        self.count = 0
        self.is_jumping = False  
        self.vertical_speed = 0  
        self.gravity = 1 

    def show(self):
        screen.blit(self.img, self.pos)

    def update(self):
        if self.is_jumping:
            self.vertical_speed += self.gravity
            self.pos = (self.pos[0], self.pos[1] + self.vertical_speed)

            if self.pos[1] >= size[1] - self.size[1]:
                self.pos = (self.pos[0], size[1] - self.size[1])
                self.is_jumping = False
                self.vertical_speed = 0

class bird:
    def __init__(self):
        self.timer = 0
        self.idx = random.randrange(0, 3)
        self.img = bird_list[self.idx][0]
        self.size = self.img.get_size()
        self.drop_x = random.randrange(100, size[0] - 100 - self.size[0])
        self.drop = False
        self.create_x = size[0]
        self.create_y = random.randrange(80, 350)
        self.target_x = -self.size[0]
        self.target_y = random.randrange(80, 350)
        if random.random() > 0.5:
            self.create_x, self.target_x = self.target_x, self.create_x
        self.dx = self.target_x - self.create_x
        self.dy = self.target_y - self.create_y
        self.dd = (self.dx**2 + self.dy**2) ** 0.5
        self.pos = (self.create_x, self.create_y)
        self.move = random.randrange(2, 10)
        self.move_x = self.move * self.dx / self.dd
        self.move_y = self.move * self.dy / self.dd
        self.angle = math.atan(abs(self.dy / self.dx)) * 180 / math.pi

    def show(self):
        screen.blit(self.img, self.pos)

class dung:
    def __init__(self, x, y, move_x):
        self.pos = x, y
        self.move_x = move_x
        self.move_y = 3
        self.img = dung_img
        self.size = self.img.get_size()
        self.a_y = 0.1

    def show(self):
        screen.blit(self.img, self.pos)

clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)

person_static = image_read("char_static", 0.1)
person_dead = image_read("char_dead", 0.1)
person_size = person_static.get_size()
person_list = [
    image_read("char_1", 0.1),
    image_read("char_2", 0.1),
    image_read("char_3", 0.1),
    image_read("char_2", 0.1),
    image_read("char_1", 0.1),
]

bird_size = 0.15
bird_list = [
    [
        image_read("bird_0_0", bird_size),
        image_read("bird_0_1", bird_size),
        image_read("bird_0_2", bird_size),
        image_read("bird_0_3", bird_size),
        image_read("bird_0_2", bird_size),
        image_read("bird_0_1", bird_size),
        image_read("bird_0_0", bird_size),
    ],
    [
        image_read("bird_1_0", bird_size),
        image_read("bird_1_1", bird_size),
        image_read("bird_1_2", bird_size),
        image_read("bird_1_3", bird_size),
        image_read("bird_1_2", bird_size),
        image_read("bird_1_1", bird_size),
        image_read("bird_1_0", bird_size),
    ],
    [
        image_read("bird_2_0", bird_size),
        image_read("bird_2_1", bird_size),
        image_read("bird_2_2", bird_size),
        image_read("bird_2_3", bird_size),
        image_read("bird_2_2", bird_size),
        image_read("bird_2_1", bird_size),
        image_read("bird_2_0", bird_size),
    ],
]
dung_img = image_read("dung", 0.15)

point_font = pygame.font.Font(
    "", 80
)
finalp_font = pygame.font.Font(
    "", 80
)
cur_font = pygame.font.Font(
    "=", 80
)
ready_font = pygame.font.Font(
    "=", 100
)
start_font = pygame.font.Font(
    "", 30
)

exit = False
game_ready = False
max_score = 0

while not exit:
    player = person()
    birds = bird()
    birds_list = []
    dd_list = []
    left_go = False
    right_go = False
    up_go = False
    game_over = False
    play_again = False
    
    while not exit:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if key_name == "space":
                    game_ready = True
        if game_ready == True:
            break
        birds.timer += 2
        birds.img = bird_list[birds.idx][int(birds.timer) % len(bird_list[birds.idx])]
        birds.pos = tup_r((size[0] / 2 - birds.size[0] / 2, size[1] / 3))
        screen.fill(white)
        birds.show()
        ready_img = ready_font.render("새똥 피하기", True, black)
        ready_size = ready_img.get_size()
        ready_pos = tup_r(
            (size[0] / 2 - ready_size[0] / 2, size[1] / 2 - ready_size[1] / 2)
        )
        screen.blit(ready_img, ready_pos)
        start_img = start_font.render("press space to start the game", True, black)
        start_size = start_img.get_size()
        start_pos = tup_r((size[0] / 2 - start_size[0] / 2, size[1] / 2 + 150))
        screen.blit(start_img, start_pos)
        pygame.display.flip()

    del birds
    game_start_time = pygame.time.get_ticks()
    while not exit:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if key_name == "left":
                    left_go = True
                elif key_name == "right":
                    right_go = True
                elif key_name == "up":
                    if not player.is_jumping: 
                        player.is_jumping = True
                        player.vertical_speed = -15  
                elif key_name == "space" and game_over == True:
                    play_again = True
            if event.type == pygame.KEYUP:
                player.timer = 0
                key_name = pygame.key.name(event.key)
                if key_name == "left":
                    left_go = False
                elif key_name == "right":
                    right_go = False
                elif key_name == "up":
                    up_go = False

        now_time = pygame.time.get_ticks()
        if game_over == False:
            total_time = now_time - game_start_time
        if random.random() < 0.05:
            bb = bird()
            birds_list.append(bb)

        if game_over == True:
            player.img = person_dead
        else:
            if left_go == True and right_go == False and up_go == False:
                player.pos = (player.pos[0] - player.move, player.pos[1])
                player.timer += 0.2
                player.img = person_list[int(player.timer) % len(person_list)]
                player.img = pygame.transform.flip(player.img, True, False)
                if player.pos[0] <= 0:
                    player.pos = (0, player.pos[1])
            elif left_go == False and right_go == True and up_go == False:
                player.pos = (player.pos[0] + player.move, player.pos[1])
                player.timer -= 0.2
                player.img = person_list[int(player.timer) % len(person_list)]

                if player.pos[0] >= size[0] - player.size[0]:
                    player.pos = (size[0] - player.size[0], player.pos[1])
            else:
                player.img = person_static

        player.update()

        for birds in birds_list:
            birds.timer += 2
            birds.img = bird_list[birds.idx][int(birds.timer) % len(bird_list[birds.idx])]
            if birds.move_x > 0:
                birds.img = pygame.transform.flip(birds.img, True, False)
            if birds.dx * birds.dy < 0:
                birds.img = pygame.transform.rotate(birds.img, birds.angle)
            else:
                birds.img = pygame.transform.rotate(birds.img, -birds.angle)
            birds.pos = (birds.pos[0] + birds.move_x, birds.pos[1] + birds.move_y)
            if birds.move_x < 0:
                if birds.pos[0] >= birds.drop_x and birds.drop == False:
                    dd = dung(
                        round(birds.pos[0] + birds.size[0] / 2),
                        birds.pos[1] + birds.size[1],
                        birds.move_x,
                    )
                    dd_list.append(dd)
                    birds.drop = True
            else:
                if birds.pos[0] <= birds.drop_x and birds.drop == False:
                    dd = dung(
                        round(birds.pos[0] + birds.size[0] / 2),
                        birds.pos[1] + birds.size[1],
                        birds.move_x,
                    )
                    dd_list.append(dd)
                    birds.drop = True

        for dd in dd_list:
            dd.move_y += dd.a_y
            dd.pos = (dd.pos[0] + dd.move_x, dd.pos[1] + dd.move_y)
            X, Y = player.pos
            W, H = player.size
            x, y = dd.pos
            w, h = dd.size
            if X - w < x and x < X + W and Y - h < y and y < Y + H - h:
                game_over = True

        del_list = []
        for idx, birds in enumerate(birds_list):
            if birds.pos[0] < -birds.size[0] or birds.pos[0] > size[0]:
                del_list.append(idx)
        del_list.reverse()
        for d in del_list:
            del birds_list[d]

        del_list = []
        for idx, dd in enumerate(dd_list):
            if dd.pos[1] > size[1] - dd.size[1]:
                del_list.append(idx)
        del_list.reverse()
        for d in del_list:
            del dd_list[d]

        if game_over == True and play_again == True:
            break

        screen.fill(white)
        player.show()
        for birds in birds_list:
            birds.show()
        for dd in dd_list:
            dd.show()

        point = point_font.render(str(total_time / 1000), True, black)
        point_size = point.get_size()
        point_pos = tup_r((300, 20))
        screen.blit(point, point_pos)

        if game_over == True:
            if max_score <= total_time / 1000:
                max_score = total_time / 1000
            finish_bg = pygame.Surface(size)
            finish_bg.fill(black)
            finish_bg.set_alpha(200)
            screen.blit(finish_bg, (0, 0))
            finalp_img = finalp_font.render(f"최고 기록 : {max_score}초", True, white)
            finalp_size = finalp_img.get_size()
            finalp_pos = tup_r(
                (size[0] / 2 - finalp_size[0] / 2, size[1] / 2 - finalp_size[1] / 2)
            )
            cur_img = cur_font.render(f"현재 기록 : {total_time/1000}초", True, white)
            cur_size = cur_img.get_size()
            cur_pos = tup_r(
                (size[0] / 2 - cur_size[0] / 2, size[1] / 2 - cur_size[1] / 2 + cur_size[1])
            )
            screen.blit(finalp_img, finalp_pos)
            screen.blit(cur_img, cur_pos)
            start_img = start_font.render("press space to restart the game", True, white)
            start_size = start_img.get_size()
            start_pos = tup_r((size[0] / 2 - start_size[0] / 2, size[1] / 2 + 150))
            screen.blit(start_img, start_pos)
        pygame.display.flip()

pygame.quit()
