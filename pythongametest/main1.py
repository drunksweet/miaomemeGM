import pygame
import random


class Player_short(object):
    """
    player对象
    """

    def __init__(self):
        self.image = pygame.image.load('test2.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (37.5,187.5)
        self.vel_y = 0
        self.jumped = False

    def move(self,init_x):
        x_move = init_x
        self.rect.x += x_move
        screen.blit(self.image, self.rect)

    def randommove(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            list1 = [20,  30, -10,-25]
            self.move(random.choice(list1))
            self.vel_y = -10
            self.jumped = True



    def jump(self):
        y_move = 0

        # 添加角色重力（跳跃之后自然下落）
        self.vel_y += 1.2

        if self.vel_y > 10:
            self.vel_y = 10

        y_move += self.vel_y

        self.rect.y += y_move

        # 控制人物的最低位置
        if self.rect.bottom > 225:
            self.rect.bottom = 225

        # 绘制人物
        screen.blit(self.image, self.rect)

class Player_double(object):
    """
    player对象
    """

    def __init__(self):
        self.image = pygame.image.load('test3.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (112.5,187.5)
        self.vel_y = 0
        self.jumped = False

    def move(self,init_x):
        x_move = init_x
        self.rect.x += x_move
        screen.blit(self.image, self.rect)

    def randommove(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            list1 = [-20,-30,  30, 20]
            self.move(random.choice(list1))
            self.vel_y = -14
            self.jumped = True



    def jump(self):
        y_move = 0

        # 添加角色重力（跳跃之后自然下落）
        self.vel_y += 1.2

        if self.vel_y > 10:
            self.vel_y = 10

        y_move += self.vel_y

        self.rect.y += y_move

        # 控制人物的最低位置
        if self.rect.bottom > 225:
            self.rect.bottom = 225

        # 绘制人物
        screen.blit(self.image, self.rect)


class Player_long(object):
    """
    player对象
    """

    def __init__(self):
        self.image = pygame.image.load('test3.jpg').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (187.5,187.5)
        self.vel_y = 0
        self.jumped = False

    def move(self,init_x):
        x_move = init_x
        self.rect.x += x_move
        screen.blit(self.image, self.rect)

    def randommove(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            list1 = [-20,-30,  30, 20]
            self.move(random.choice(list1))
            self.vel_y = -16
            self.jumped = True



    def jump(self):
        y_move = 0

        # 添加角色重力（跳跃之后自然下落）
        self.vel_y += 1.2

        if self.vel_y > 10:
            self.vel_y = 10

        y_move += self.vel_y

        self.rect.y += y_move

        # 控制人物的最低位置
        if self.rect.bottom > 225:
            self.rect.bottom = 225

        # 绘制人物
        screen.blit(self.image, self.rect)


# --------------------------------加载基本的窗口和时钟----------------------------
pygame.init()
screen_width = 600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('player_control')
clock = pygame.time.Clock()  # 设置时钟
# -------------------------------- 加载对象 ----------------------------------
bg = pygame.image.load("test1.jpg").convert()
player_short = Player_short()
player_double =Player_double()
player_long = Player_long()



# -------------------------------- 游戏主循环 ----------------------------------
run = True
while run:
    clock.tick(60)
    screen.blit(bg, (0, 0))
    # -------------------------------- 角色更新 ----------------------------------
    player_short.jump()
    player_short.randommove()

    player_double.jump()
    player_double.randommove()

    player_long.jump()
    player_long.randommove()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # ------------------------------- 窗口更新并绘制 ------------------------------
    pygame.display.update()
pygame.quit()
