import pygame
import sys


# 飞船类
class Ship():
    # 传入屏幕（也就是初始化号的窗口对象）。
    def __init__(self,screen):
        # 得到游戏窗口
        self.screen = screen
        # 加载飞船
        self.image = pygame.image.load('./images/me.png')

        # 得到飞船的边界对象
        self.shipRect = self.image.get_rect()
        # print(self.shipRect)  # <rect(0, 0, 128, 128)>
        # 得到游戏窗口的边界对象
        self.screen_rect = screen.get_rect()
        # print(self.screen_rect)  # <rect(0, 0, 500, 600)>

        # 设置飞船的x轴中心是屏幕的中心
        self.shipRect.centerx = self.screen_rect.centerx
        # self.shipRect.left = 186

        # 设置飞船的底部是屏幕的底部
        self.shipRect.bottom = self.screen_rect.bottom
        # self.shipRect.bottom = 472+128

        # print(self.shipRect)  # <rect(186, 472, 128, 128)>

    # 在指定位置设置飞船
    def blitme(self):
        # 将飞船image，绘制在shipRect位置
        self.screen.blit(self.image, self.shipRect)



# 一些设置类
class Settings():

    def __init__(self):

        # 常量数据设置。
        self.screen_width = 500
        self.screen_height = 600
        self.bg_color = (230,230,230)


# 程序执行主类。
def run_game():

    pygame.init()
    # 得到设置类对象
    mySettings = Settings()

    # 数据常量化
    screen = pygame.display.set_mode((mySettings.screen_width,mySettings.screen_height))
    pygame.display.set_caption("我的飞机大战游戏")

    # 得到飞船对象
    ship = Ship(screen)


    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(mySettings.bg_color)

        # 调用绘制飞船的方法
        ship.blitme()

        pygame.display.flip()

# 运行
run_game()