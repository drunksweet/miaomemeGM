import pygame

import random



# 块超类

class Block:

    def __init__(self, pos_y):

        self.pos_y = pos_y

        self.pos_x = -60

        self.a = 100

        self.b = 60



    def move(self, vel):

        self.pos_y += vel



# 黑块类

class BlackBlock(Block):

    def __init__(self, pos_y):

        super().__init__(pos_y=pos_y)

        self.pos_x = random.choice([0, 60, 120, 180])

        self.color = (0, 0, 0)

        self.is_black = True

        self.has_clicked = False



    def clicked(self):

        self.color = (190, 190, 190)

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

        self.color = (255, 255, 255)

        self.is_black = False

        self.has_clicked = False



    def clicked(self):

        self.color = (255, 0, 0)

        self.has_clicked = True

        return False



# 添加块的逻辑实现

def add_blocks(pos_y=-100):

    blocks = [WhiteBlock(0, pos_y), WhiteBlock(60, pos_y), WhiteBlock(120, pos_y), WhiteBlock(180, pos_y)]

    black_block = BlackBlock(pos_y)

    blocks[{0: 0, 60: 1, 120: 2, 180: 3}[black_block.pos_x]] = black_block

    return blocks

#实现多次初始化

def init():

    global running, block_scr, score, start, game_over, level, v_n, v_list, game_over_has_played

    pygame.mixer.music.play(-1)

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

    for i in range(5):

        block_scr.append(add_blocks())

        for j in range(i):

            for block in block_scr[j]:

                block.pos_y += 100



pygame.init()

pygame.mixer.init()

pygame.mixer.music.load('music\\01.mp3')

game_over_sound = pygame.mixer.Sound('music\\01.mp3')

score_sound = pygame.mixer.Sound('music\\01.mp3')

screen = pygame.display.set_mode((240, 400))

pygame.display.set_caption('别踩白块1.5')

font = pygame.font.SysFont('arial', 20)

clock = pygame.time.Clock()

init()

# 以上是游戏初始化

while running:

    clock.tick(60)

    screen.fill((255, 255, 255))

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

    if block_scr[0][0].pos_y >= 400:

        n = 0

        for block in block_scr[0]:

            if not block.has_clicked:

                n += 1

        if n == 4:

            game_over = True

            game_over_image = font.render('Game Over', True, (0, 255, 0))

            total_score = font.render('%d' % score, True, (0, 255, 0))

        del block_scr[0]

        block_scr.append(add_blocks(block_scr[3][0].pos_y - 100))

    # 检查事件

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:

            if not start:

                start = True

            mouse_x, mouse_y = event.pos

            if game_over:

                if 0 < mouse_x < 20 and 0 < mouse_y < 20:

                    game_over = False

                    init()

                    continue

            for i in range(5):

                if block_scr[i][0].pos_y < mouse_y < (block_scr[i][0].pos_y + 100):

                    for j in range(4):

                        if block_scr[i][j].pos_x < mouse_x < (block_scr[i][j].pos_x + 60):

                            if block_scr[i][j].clicked():

                                score += 1

                                score_sound.play(0)

                            elif block_scr[i][j].is_black:

                                pass

                            else:

                                game_over = True

                                game_over_image = font.render('Game Over', True, (0, 255, 0))

                                total_score = font.render('%d' % score, True, (0, 255, 0))

        elif event.type == pygame.QUIT:

            running = False

    # 显示块

    for blank in block_scr:

        for block in blank:

            pygame.draw.rect(screen, block.color, (block.pos_x, block.pos_y, block.b, block.a), 0)

    # 游戏结束显示字体,停放bgm

    if game_over:

        pygame.mixer.music.stop()

        if not game_over_has_played:

            game_over_sound.play(0)

            game_over_has_played = True

        screen.blit(game_over_image, (20, 0))

        screen.blit(total_score, (20, 50))

        start = False

    # 分数显示

    score_image = font.render('%d' % score, True, (0, 255, 0))

    screen.blit(score_image, (0, 0))

    # 更新画面

    pygame.display.update()

pygame.quit()