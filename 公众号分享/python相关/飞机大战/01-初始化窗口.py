import pygame
import sys


def run_game():

    # 初始化游戏：init()方法是调用 pygame 自身的初始化方法
    pygame.init()

    # 设置窗口大小
    screen = pygame.display.set_mode((600, 400))
    # 设置窗口名称
    pygame.display.set_caption("我的飞机大战游戏")

    # 开始循环游戏，监听事件
    while True:

        # 检查所有事件，并且执行相应的操作。
        for event in pygame.event.get():

            # 如果当前事件是 推出。
            if event.type == pygame.QUIT:
                # 就执行系统的退出窗口功能，关闭当前游戏窗口。
                sys.exit()

        # 让屏幕显示最近绘制的内容。
        pygame.display.flip()

# 运行
run_game()