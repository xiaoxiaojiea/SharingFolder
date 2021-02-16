import pygame
import sys


# 一些设置类
class Settings():

    def __init__(self):
        # 常量数据设置。
        self.screen_width = 600
        self.screen_height = 400
        self.bg_color = (230, 230, 230)


# 程序执行主类。
def run_game():
    pygame.init()
    # 得到设置类对象
    mySettings = Settings()

    # 数据常量化
    screen = pygame.display.set_mode((mySettings.screen_width, mySettings.screen_height))
    pygame.display.set_caption("我的飞机大战游戏")

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(mySettings.bg_color)

        pygame.display.flip()


# 运行
run_game()