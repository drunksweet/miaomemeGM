import threading
import pygame
import sys
import random
from pygame.sprite import Sprite


class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    GREY = (190, 190, 190)
    YELLOW = (255, 255, 0)


class WINDOW:
    WIDTH = 600
    HEIGHT = 900
    HEIGHT_SCREEN = HEIGHT*0.6
    X_LEN = 8
    Y_LEN = 6


class BLOCK:
    WIDTH = WINDOW.WIDTH // WINDOW.X_LEN
    HEIGHT = WIDTH
    SPEED = 5

    class FORM:
        NORM = 1
        LONG = 2
        SOLID = 3

        def random():
            return random.randint(1, 3)


# 初始化 Pygame
pygame.init()

# 设置游戏窗口和标题
screen = pygame.display.set_mode((WINDOW.WIDTH, WINDOW.HEIGHT))
pygame.display.set_caption('别踩白块1.5')

# 加载音效和音乐
pygame.mixer.init()
# pygame.mixer.music.load('music/01.mp3')
# score_sound = pygame.mixer.Sound('music/01.mp3')
# game_over_sound = pygame.mixer.Sound('music/01.mp3')

# 设置字体和时钟
font = pygame.font.SysFont('arial', 20)
clock = pygame.time.Clock()


class Block(Sprite):
    def __init__(self, color, x, y, is_black):
        super().__init__()
        self.image = pygame.Surface((BLOCK.WIDTH, BLOCK.HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)
        self.is_black = is_black
        self.has_clicked = (color == COLOR.WHITE)
        self.form = BLOCK.FORM.NORM
        self.has_changed = False
        self.last_clicked_time = -1
        self.last_y = 0
        self.key = pygame.K_0

    def toLong(self, h, color):
        x, y = self.rect.bottomleft
        self.image = pygame.Surface((BLOCK.WIDTH, h * BLOCK.HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def move(self, vel):
        self.rect.y += vel

    def clicked(self, color=COLOR.GREY):
        if self.has_clicked or not self.is_black:
            return False
        elif self.form == BLOCK.FORM.NORM:
            self.image.fill(color)
            self.has_clicked = True
        elif self.form == BLOCK.FORM.LONG:
            self.has_clicked = True
        elif self.form == BLOCK.FORM.SOLID:
            if self.last_clicked_time == -1:
                self.has_clicked = False
                self.last_clicked_time = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.last_clicked_time < 300:
                    self.has_clicked = True
                    self.image.fill(color)
                self.last_clicked_time = -1
            self.last_clicked_time = pygame.time.get_ticks()
        return True

    def is_changed(self,mouse_y):
        if self.form == BLOCK.FORM.LONG:
            if not self.has_changed:
                # mouse_x, mouse_y = pygame.mouse.get_pos()
                distance_from_bottom = self.rect.bottom - mouse_y
                # 创建一个新的Surface对象，将点击位置以上的区域填充为透明
                transparent_surface = pygame.Surface((self.rect.width, distance_from_bottom))
                transparent_surface.set_colorkey(COLOR.GREEN)  # 设置透明颜色
                transparent_surface.set_alpha(70)  # 设置透明度
                transparent_surface.fill(COLOR.GREY)
                # 计算透明 Surface 的位置，使其位于黑块底部
                transparent_y = (mouse_y - self.rect.top)
                # 将透明区域绘制到黑块Surface上
                self.image.blit(transparent_surface, (0, transparent_y))
                self.last_y = mouse_y
            if not pygame.key.get_pressed()[self.key]:
                self.has_changed = True
        elif self.form == BLOCK.FORM.NORM:
            self.last_y = self.rect.top
            self.has_changed = True
        elif self.form == BLOCK.FORM.SOLID:
            if self.has_clicked:
                self.last_y = self.rect.bottom + BLOCK.HEIGHT
                self.has_changed = True

        return self.has_changed


def get_black_block(pos_y=[0], form=0):
    if form == 0:
        form = BLOCK.FORM.random()
    x_pos = random.randint(0, WINDOW.X_LEN-1)
    block = Block(COLOR.BLACK, x_pos * BLOCK.WIDTH, pos_y[0], True)
    pos_y[0] -= BLOCK.HEIGHT;
    y_len = 0
    if form == BLOCK.FORM.LONG:
        y_len = random.randint(2, 5)
        pos_y[0] -= (y_len - 1) * BLOCK.HEIGHT
        block.toLong(y_len, COLOR.GREEN)
    elif form == BLOCK.FORM.SOLID:
        block.image.fill(COLOR.YELLOW)

    block.form = form
    print(pos_y, y_len, block.rect)
    return block


# 黑块末尾
end_pos_y = [BLOCK.HEIGHT*2]
# 被选中的黑块
selected_block = None


def init():
    global running, blocks_group, score, start, game_over, level, v_n, v_list, game_over_has_played
    # pygame.mixer.music.play(-1)
    running = True
    blocks_group = pygame.sprite.Group()
    score = 0
    start = False
    game_over = False
    game_over_has_played = False
    level = score // 4
    v_n = 0
    v_list = ([int(1.5 + level * 0.125)] * int((int(2.5 + level * 0.125) - (1.5 + level * 0.125)) // 0.125) +
              [int(2.5 + level * 0.125)] * int(((1.5 + level * 0.125) - int(1.5 + level * 0.125)) // 0.125))

    for _ in range(WINDOW.Y_LEN + 1):
        # 添加新块
        blocks_group.add(get_black_block(pos_y=end_pos_y))


init()

mouse_y = WINDOW.HEIGHT*0.95

while running:
    clock.tick(60)
    screen.fill(COLOR.WHITE)
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
        # blocks_group.update(v)
        for block in blocks_group:
            block.move(v)
        # 更新末尾位置
        end_pos_y[0] += v
        if end_pos_y[0] > 0:
            end_pos_y[0] = 0
    else:
        v = 0

    # 检查最底下的方块是否超出边界
    bottom_block = blocks_group.sprites()[0]
    if bottom_block.rect.y >= WINDOW.HEIGHT:
        if not bottom_block.has_clicked:
            game_over = True
            start = False
        # 移除最底下的方块
        blocks_group.sprites()[0].kill()

    # 末尾为0，则添加新的方块到最后
    if end_pos_y[0] == 0:
        blocks_group.add(get_black_block(pos_y=end_pos_y))

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if not start:
                start = True


            if game_over:
                game_over = False
                init()
                continue

            if event.key == pygame.K_1:
                mouse_x = WINDOW.WIDTH*0.125/2

            elif event.key == pygame.K_2:
                mouse_x = WINDOW.WIDTH*(0.125+0.25)/2

            elif event.key == pygame.K_3:
                mouse_x = WINDOW.WIDTH*(0.25+0.375)/2
                
            elif event.key == pygame.K_4:
                mouse_x = WINDOW.WIDTH*(0.375+0.5)/2
                
            elif event.key == pygame.K_5:
                mouse_x = WINDOW.WIDTH*(0.5+0.625)/2
                
            elif event.key == pygame.K_6:
                mouse_x = WINDOW.WIDTH*(0.625+0.75)/2
                
            elif event.key == pygame.K_7:
                mouse_x = WINDOW.WIDTH*(0.75+0.875)/2
                
            elif event.key == pygame.K_8:
                mouse_x = WINDOW.WIDTH*(0.875+1)/2
                
            for block in blocks_group.sprites():
                if block.rect.collidepoint(mouse_x,mouse_y):
                    if selected_block == block:
                        block.clicked()
                    elif selected_block == None and not block.has_clicked:
                        selected_block = block
                        block.clicked()
                        block.key = event.key
                    # thread = threading.Thread(target=transparent_block, args=(block,))
                    # thread.start()
                    break
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            print(key, "Key is pressed")

        elif event.type == pygame.QUIT:
            running = False

    if selected_block != None:
        if selected_block.is_changed(mouse_y):
            score += (selected_block.rect.bottom - selected_block.last_y) // BLOCK.HEIGHT
            selected_block = None
        # score_sound.play(0)

    # 绘制屏幕
    screen.fill(COLOR.WHITE)
    blocks_group.draw(screen)
    pygame.draw.line(screen, [255 ,20 ,147], [0,mouse_y],[WINDOW.WIDTH,mouse_y],5)

    # if game_over:
    #     pygame.mixer.music.stop()
    #     if not game_over_has_played:
    #         game_over_sound.play()
    #     game_over_image = font.render('Game Over', True, COLOR.RED)
    #     total_score = font.render('%d' % score, True, COLOR.RED)
    #     screen.blit(game_over_image, (20, 0))
    #     screen.blit(total_score, (20, 50))
    # else:
    #     score_image = font.render('%d' % score, True, COLOR.GREEN)
    #     screen.blit(score_image, (0, 0))

    pygame.display.flip()
    pygame.display.update()

pygame.quit()