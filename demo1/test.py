# 导入库
import pygame
pygame.init()

# 设置窗口
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("滚动背景教程")

# 加载背景图像
background_img = pygame.image.load("./data/bg.jpg")

# 滚动背景
scroll_x = 0
scroll_y = 0
background_x = 0
background_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # 水平滚动背景
    # scroll_x -= 1
    # background_x -= 1
    scroll_y -= 1
    background_y -= 1

    # 画两次背景图像以创建无缝滚动效果
    screen.blit(background_img, (scroll_x, scroll_y))
    # screen.blit(background_img, (background_x, scroll_y))
    screen.blit(background_img, (scroll_x, background_y))

    # 当背景超出屏幕时，重置背景位置
    # if scroll_x <= -screen_width:
    #     scroll_x = screen_width

    # if background_x <= -screen_width:
    #     background_x = screen_width
    if scroll_y <= -screen_height:
        scroll_y = screen_height

    if background_y <= -screen_height:
        background_y = screen_height

    pygame.display.update()

# 添加游戏对象
player_img = pygame.image.load("player.png")
player_x = 400
player_y = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # 水平滚动背景
    scroll_x -= 1
    background_x -= 1

    # 画两次背景图像以创建无缝滚动效果
    screen.blit(background_img, (scroll_x, scroll_y))
    screen.blit(background_img, (background_x, scroll_y))

    # 当背景超出屏幕时，重置背景位置
    if scroll_x <= -screen_width:
        scroll_x = screen_width

    if background_x <= -screen_width:
        background_x = screen_width

    # 添加游戏对象
    screen.blit(player_img, (player_x, player_y))

    pygame.display.update()