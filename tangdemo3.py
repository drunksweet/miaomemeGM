import pygame

import random


# 块超类

class Block:

    def __init__(self, pos_y):

        self.pos_y = pos_y

        self.pos_x = -screen_width*0.25

        self.a = 100

        self.b = screen_width*0.25


    def move(self, vel):

        self.pos_y += vel



# 黑块类

class BlackBlock(Block):

    def __init__(self, pos_y):

        super().__init__(pos_y=pos_y)

        self.pos_x = random.choice([screen_width*0, screen_width*0.125,screen_width*0.25, screen_width*0.375,screen_width*0.5, screen_width*0.625,screen_width*0.75, screen_width*0.875])

        self.color = (255 ,193 ,37)

        self.is_black = True

        self.has_clicked = False





    def clicked(self):

        self.color = (100,100,100)

        if self.has_clicked:

            return False

        else:

            self.has_clicked = True

            return True



# 白块类

class WhiteBlock(Block):

    def __init__(self, pos_x, pos_y):

        super().__init__(pos_y=pos_y)

        self.pos_x = pos_x

        self.color = (0, 0, 0)

        self.is_black = False

        self.has_clicked = False



    def clicked(self):

        self.color = (255, 0, 0)

        self.has_clicked = True

        return False



# 添加块的逻辑实现

def add_blocks(pos_y=0):
    blocks = [WhiteBlock(screen_width*0, pos_y), WhiteBlock(screen_width*0.125, pos_y), WhiteBlock(screen_width*0.25, pos_y), WhiteBlock(screen_width*0.375, pos_y),
              WhiteBlock(screen_width*0.5, pos_y), WhiteBlock(screen_width*0.625, pos_y), WhiteBlock(screen_width*0.75, pos_y), WhiteBlock(screen_width*0.875, pos_y)]

    black_block = BlackBlock(pos_y)

    blocks[{screen_width*0: 0, screen_width*0.125: 1, screen_width*0.25: 2, screen_width*0.375: 3,
            screen_width*0.5: 4, screen_width*0.625: 5, screen_width*0.75: 6, screen_width*0.875: 7}[black_block.pos_x]] = black_block

    return blocks

def judge(click_x):
    global screen_width, screen_height, game_over, total_score, score
    for j in range(8):
        if block_scr[0][j].pos_x < click_x < (block_scr[0][j].pos_x + screen_width/8):
            if block_scr[0][j].clicked():
                score += 1
            elif block_scr[0][j].is_black:
                pass
            else:

                game_over = True

                total_score = font.render('%d' % score, True, (0, 255, 0))

#实现多次初始化

def init():

    global running, block_scr, score, start, game_over, level, v_n, v_list, game_over_has_played,screen_height,window_height



    running = True

    block_scr = []

    score = 0

    start = False

    game_over = False

    game_over_has_played = False

    level = score // 4

    v_n = 0   #让块下落得更加丝滑

    v_list = ([int(1.5 + level * 0.125)] * int((int(2.5 + level * 0.125) - (1.5 + level * 0.125)) // 0.125) +

              [int(2.5 + level * 0.125)] * int(((1.5 + level * 0.125) - int(1.5 + level * 0.125)) // 0.125))

    initial_pos_y = window_height

    for i in range(6):

        block_scr.append(add_blocks(initial_pos_y +i * 100))

        for j in range(i):

            for block in block_scr[j]:

                block.pos_y += 100


# 获取屏幕大小
pygame.init()

screen_info = pygame.display.Info()

screen_width = screen_info.current_w*0.4
screen_height = screen_info.current_h*0.6
window_height = screen_info.current_h*0.9

pygame.mixer.init()


# 设置窗口大小，限制窗口大小不超过屏幕的一半
screen = pygame.display.set_mode((screen_width, window_height))

# screen = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)

pygame.display.set_caption('喵咪咪')

font = pygame.font.SysFont('arial', 20)

clock = pygame.time.Clock()

init()

# 以上是游戏初始化

while running:

    clock.tick(60)

    screen.fill((0, 0, 0))

    # 设置块的速度

    if score // 4 > level:

        level = score // 4

        v_list = ([int(1.5 + level * 0.125)] * int((int(2.5 + level * 0.125) - (1.5 + level * 0.125)) // 0.125) +

                  [int(2.5 + level * 0.125)] * int(((1.5 + level * 0.125) - int(1.5 + level * 0.125)) // 0.125))

    if start:

        v = v_list[v_n]

        v_n += 1

        if v_n == 8:

            v_n = 0

        for blank in block_scr:

            for block in blank:

                block.move(v)

    else:

        v = 0

    # 检查最底下的块是否超出边界

    if block_scr[0][0].pos_y >= screen_height*0.9:

        # n = 0
        #
        # for block in block_scr[0]:
        #
        #     if not block.has_clicked:
        #
        #         n += 1
        #
        # if n == 8:
        #
        #     game_over = True
        #
        #     game_over_image = font.render('Game Over', True, (0, 255, 0))
        #
        #     total_score = font.render('%d' % score, True, (0, 255, 0))

        del block_scr[0]

        block_scr.append(add_blocks(block_scr[-1][0].pos_y - 100))

    # 检查事件

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if not start:

                start = True

            if game_over:

                game_over = False

                init()

                continue

            click_y = screen_height * 0.9
            if event.key == pygame.K_1:
                click_x = screen_width*0.125/2
                judge(click_x)
            elif event.key == pygame.K_2:
                click_x = screen_width*(0.125+0.25)/2
                judge(click_x)
            elif event.key == pygame.K_3:
                click_x = screen_width*(0.25+0.375)/2
                judge(click_x)
            elif event.key == pygame.K_4:
                click_x = screen_width*(0.375+0.5)/2
                judge(click_x)
            elif event.key == pygame.K_5:
                click_x = screen_width*(0.5+0.625)/2
                judge(click_x)
            elif event.key == pygame.K_6:
                click_x = screen_width*(0.625+0.75)/2
                judge(click_x)
            elif event.key == pygame.K_7:
                click_x = screen_width*(0.75+0.875)/2
                judge(click_x)
            elif event.key == pygame.K_8:
                click_x = screen_width*(0.875+1)/2
                judge(click_x)




    # 渲染块

    for blank in block_scr:

        for block in blank:

            pygame.draw.rect(screen, block.color, (block.pos_x, block.pos_y+window_height-screen_height, block.b, block.a), 0)


    # 渲染有的没的

    pygame.draw.line(screen, [255 ,20 ,147], [0,window_height-50],[screen_width,window_height-50],10)
    # 游戏结束显示字体,停放bgm

    if game_over:

        pygame.mixer.music.stop()

        if not game_over_has_played:

            game_over_has_played = True


        screen.blit(total_score, (20, 50))

        start = False

    # 分数显示

    score_image = font.render('%d' % score, True, (0, 255, 0))

    screen.blit(score_image, (0, 0))

    # 更新画面

    pygame.display.update()

pygame.quit()