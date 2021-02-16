import pygame
import sys


def run_game():

    pygame.init()

    # screen当前游戏的窗口对象
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("我的飞机大战游戏")

    # 设置窗口背景色元组
    bg_color = (230,230,230)


    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        # 设置屏幕的背景色。每次重新绘制的时候就绘制这个颜色。
        screen.fill(bg_color)

        pygame.display.flip()

# 运行
run_game()