
import pygame
import random
from constant import *



class Player_short(object):
    """
    player对象
    """

    def __init__(self,screen):
        self.image = pygame.image.load('src/drawable/topcat1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK.WIDTH, BLOCK.HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (37.5,112.5)
        self.vel_y = 0
        self.jumped = False
        self.screen = screen

    def move(self,init_x):
        self.rect.x = init_x
        self.screen.blit(self.image, self.rect)
        self.vel_y = -10
        self.jumped = True

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
        if self.rect.bottom > 150:
            self.rect.bottom = 150

        # 绘制人物
        self.screen.blit(self.image, self.rect)

class Player_double(object):
    """
    player对象
    """

    def __init__(self,screen):
        self.image = pygame.image.load('src/drawable/topcat2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK.WIDTH, BLOCK.HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (112.5,112.5)
        self.vel_y = 0
        self.jumped = False
        self.screen = screen


    def move(self,init_x):
        self.rect.x = init_x
        self.screen.blit(self.image, self.rect)
        self.vel_y = -14
        self.jumped = True

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
        if self.rect.bottom > 150:
            self.rect.bottom = 150

        # 绘制人物
        self.screen.blit(self.image, self.rect)


class Player_long(object):
    """
    player对象
    """

    def __init__(self,screen):
        self.image = pygame.image.load('src/drawable/longcat1/head.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (BLOCK.WIDTH, BLOCK.HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (187.5,112.5)
        self.vel_y = 0
        self.jumped = False
        self.screen = screen

    def move(self,init_x):
        self.rect.x = init_x
        self.screen.blit(self.image, self.rect)
        self.vel_y = -16
        self.jumped = True

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
        if self.rect.bottom > 150:
            self.rect.bottom = 150

        # 绘制人物
        self.screen.blit(self.image, self.rect)


#######jumpcats