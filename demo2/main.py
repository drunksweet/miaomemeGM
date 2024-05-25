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


class BLOCK:
    WIDTH = 60
    HEIGHT = 100
    SPEED = 5


class WINDOW:
    WIDTH = 400
    HEIGHT = 600


# 初始化 Pygame
pygame.init()

# 设置游戏窗口和标题
screen = pygame.display.set_mode((WINDOW.WIDTH, WINDOW.HEIGHT))
pygame.display.set_caption('别踩白块1.5')

# 加载音效和音乐
pygame.mixer.init()
pygame.mixer.music.load('music/01.mp3')
score_sound = pygame.mixer.Sound('music/01.mp3')
game_over_sound = pygame.mixer.Sound('music/01.mp3')

# 设置字体和时钟
font = pygame.font.SysFont('arial', 20)
clock = pygame.time.Clock()


class Block(Sprite):
    def __init__(self, color, x, y, is_black):
        super().__init__()
        self.image = pygame.Surface((BLOCK.WIDTH, BLOCK.HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_black = is_black
        self.has_clicked = False

    def move(self, vel):
        self.rect.y += vel

    def clicked(self, color=COLOR.GREY):
        self.image.fill(color)
        self.has_clicked = True


def add_blocks(pos_y=-100):
    blocks = pygame.sprite.Group()
    colors = [COLOR.WHITE for _ in range(4)]
    black_index = random.randint(0, 3)
    colors[black_index] = COLOR.BLACK
    for i, color in enumerate(colors):
        block = Block(color, i * BLOCK.WIDTH, pos_y, color == COLOR.BLACK)
        blocks.add(block)
    return blocks


def init():
    global running, blocks_group, score, start, game_over, level, v_n, v_list, game_over_has_played
    pygame.mixer.music.play(-1)
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
    for i in range(5):
        blocks = add_blocks()
        for block in blocks:
            blocks_group.add(block)
        # blocks_group.add(blocks)
        for block in blocks_group:
            block.rect.y += 100


init()

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
    else:
        v = 0

    # 检查最底下的方块是否超出边界
    if blocks_group.sprites()[0].rect.y >= WINDOW.HEIGHT:
        bottom_blocks = blocks_group.sprites()[:4]
        if all(not block.has_clicked for block in bottom_blocks if block.is_black):
            game_over = True
            start = False

        # 移除前四个方块
        for _ in range(4):
            blocks_group.sprites()[0].kill()
        # 添加新的方块到最后
        new_blocks = add_blocks(blocks_group.sprites()[-1].rect.y - BLOCK.HEIGHT)
        for block in new_blocks:
            blocks_group.add(block)

    # 处理事件
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
            for block in blocks_group.sprites():
                if block.rect.collidepoint(event.pos):
                    if block.clicked():
                        score += 1
                        score_sound.play(0)
                    elif not block.is_black:
                        game_over = True
                        game_over_image = font.render('Game Over', True, COLOR.GREEN)
                        total_score = font.render('%d' % score, True, COLOR.GREEN)

        elif event.type == pygame.QUIT:
            running = False

    # 绘制屏幕
    screen.fill(COLOR.WHITE)
    blocks_group.draw(screen)

    if game_over:
        pygame.mixer.music.stop()
        if not game_over_has_played:
            game_over_sound.play()
        game_over_image = font.render('Game Over', True, COLOR.GREEN)
        total_score = font.render('%d' % score, True, COLOR.GREEN)
        screen.blit(game_over_image, (20, 0))
        screen.blit(total_score, (20, 50))
    else:
        score_image = font.render('%d' % score, True, COLOR.BLACK)
        screen.blit(score_image, (0, 0))

    # pygame.display.flip()
    pygame.display.update()

pygame.quit()
