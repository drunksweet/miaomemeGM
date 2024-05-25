import pygame
import random

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (190, 190, 190)
RED = (255, 0, 0)

# 定义块的大小和速度
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 100
BLOCK_SPEED = 5

# 定义游戏窗口大小
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 400

# 初始化 Pygame
pygame.init()

# 设置游戏窗口和标题
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('别踩白块1.5')

# 加载音效和音乐
pygame.mixer.init()
pygame.mixer.music.load('music/01.mp3')
score_sound = pygame.mixer.Sound('music/01.mp3')
game_over_sound = pygame.mixer.Sound('music/01.mp3')

# 设置字体和时钟
font = pygame.font.SysFont('arial', 20)
clock = pygame.time.Clock()


# 定义方块精灵类
class BlockSprite(pygame.sprite.Sprite):
    def __init__(self, color, x, y, is_black):
        super().__init__()
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_black = is_black
        self.has_clicked = False

    def update(self, vel):
        self.rect.y += vel


# 添加方块的逻辑实现
def add_blocks(pos_y=-100):
    blocks = pygame.sprite.Group()
    colors = [WHITE, WHITE, WHITE, WHITE]
    black_index = random.randint(0, 3)
    colors[black_index] = BLACK
    for i, color in enumerate(colors):
        block = BlockSprite(color, i * BLOCK_WIDTH, pos_y, color == BLACK)
        blocks.add(block)
    return blocks


# 初始化游戏
def init():
    global running, blocks_group, score, start, game_over, level, v_n, v_list, game_over_has_played
    pygame.mixer.music.play(-1)
    running = True
    blocks_group = pygame.sprite.Group()
    score = 0
    start = False
    game_over = False
    game_over_has_played = False
    level = 0
    v_n = 0
    v_list = [1.5]
    for i in range(5):
        blocks = add_blocks()
        blocks_group.add(blocks)
        for block in blocks:
            block.rect.y += 100 * i


# 游戏初始化
init()

# 游戏主循环
while running:
    clock.tick(60)

    temp = blocks_group.sprites()
    print(f"blocks: {len(temp) }, {temp} ")
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                start = True
            if game_over:
                mouse_x, mouse_y = event.pos
                if 0 < mouse_x < 20 and 0 < mouse_y < 20:
                    game_over = False
                    init()
            else:
                for block in blocks_group.sprites():
                    if block.rect.collidepoint(event.pos):
                        if not block.has_clicked:
                            if block.is_black:
                                game_over = True
                                game_over_has_played = True
                            else:
                                block.has_clicked = True
                                score += 1
                                score_sound.play()

    # 更新方块精灵位置
    if start:
        v_n = score // 4
        if v_n >= len(v_list):
            v_n = len(v_list) - 1
        blocks_group.update(BLOCK_SPEED * v_list[v_n])

    # 检查最底下的方块是否超出边界
    if blocks_group.sprites()[0].rect.y >= WINDOW_HEIGHT:
        if all(block.has_clicked for block in blocks_group.sprites()):
            blocks_group.remove(blocks_group.sprites()[:4])
            new_blocks = add_blocks(blocks_group.sprites()[-1].rect.y - BLOCK_HEIGHT)
            blocks_group.add(new_blocks)
        else:
            game_over = True
            start = False

    # 绘制屏幕
    screen.fill(WHITE)
    blocks_group.draw(screen)

    if game_over:
        pygame.mixer.music.stop()
        if not game_over_has_played:
            game_over_sound.play()
        game_over_image = font.render('Game Over', True, RED)
        total_score = font.render('%d' % score, True, RED)
        screen.blit(game_over_image, (20, 0))
        screen.blit(total_score, (20, 50))
    else:
        score_image = font.render('%d' % score, True, BLACK)
        screen.blit(score_image, (0, 0))

    pygame.display.flip()

pygame.quit()
