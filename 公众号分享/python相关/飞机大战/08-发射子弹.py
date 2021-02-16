import pygame
import sys
from pygame.sprite import Sprite
from pygame.sprite import Group


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
        # self.shipRect.bottom = 472+128  # bottom

        # print(self.shipRect)  # <rect(186, 472, 128, 128)>

        # 移动标志（目的是让他连续移动）: 按下右箭头键时将moving_right设置为True,松开时设置为False.
        self.moving_right = False
        self.moving_left = False

        # 在指定位置设置飞船
    def blitme(self):
        # 将飞船image，绘制在shipRect位置
        self.screen.blit(self.image, self.shipRect)

    def update(self):
        if self.moving_right:
            self.shipRect.centerx += 1

        elif self.moving_left:
            self.shipRect.centerx -= 1



            # 一些设置类
class Settings():

    def __init__(self):

        # 常量数据设置。
        self.screen_width = 500
        self.screen_height = 600
        self.bg_color = (230,230,230)

        # 子弹数据设置
        self.bullet_speed_factor = 1  # 速度
        self.bullet_width = 3  # 宽
        self.bullet_height = 15 # 高
        self.bullet_color = 60, 60, 60  # 颜色



# 抽取模块
class game_functions():

    def __init__(self):
        pass

    # 检查按键的事件。
    def check_events(self,mySettings,screen,ship,bullets):

        for event in pygame.event.get():

            # 监听框框上的推出按钮
            if event.type == pygame.QUIT:
                sys.exit()

            # 监听键盘按下事件
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(mySettings, screen,event,ship,bullets)

            # 监听键盘抬起事件。
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event,ship)


    # 键盘按下事件
    def check_keydown_events(self, mySettings, screen,event,ship,bullets):
        # 按下 右键
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True

        elif event.key == pygame.K_LEFT:

            ship.moving_left = True
        # 按下空格发子弹
        elif event.key == pygame.K_SPACE:
            # 产生一个子弹
            new_bullet = Bullet(mySettings, screen, ship)
            # 产生的子弹放进子弹组中。
            bullets.add(new_bullet)

            # 键盘抬起事件
    def check_keyup_events(self,event,ship):
        # 抬起 右键
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            ship.moving_left = False



    # 屏幕更新函数: （屏幕，设置参数，飞船对象）
    def updata_screen(self,screen,mySettings,ship,bullets):

        screen.fill(mySettings.bg_color)

        # 绘制子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        # 调用绘制飞船的方法（放在fill后边，确保飞船绘制在背景上面）
        ship.blitme()

        pygame.display.flip()

    def update_bullets(self,bullets):
        # 调用
        bullets.update()

        # 删除消失的子弹
        for bullet in bullets.copy():
            if bullet.bulletRect.bottom <= 0:
                bullets.remove(bullet)
        print(len(bullets))


# 子弹类
class Bullet(Sprite):

    # 传入数据，屏幕，飞船
    def __init__(self, mySettings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，
        self.bulletRect = pygame.Rect(0, 0, mySettings.bullet_width, mySettings.bullet_height)
        # 再设置正确的位置
        self.bulletRect.centerx = ship.shipRect.centerx
        self.bulletRect.top = ship.shipRect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.bulletRect.y)  # self.y表示子弹的y轴位置。

        self.color = mySettings.bullet_color
        self.speed_factor = mySettings.bullet_speed_factor

    # 子弹会自己向上跑
    def update(self):
        self.y -= self.speed_factor  # y减少，就是往上跑。
        # 将y的新数据写入子弹的属性中。
        self.bulletRect.y = self.y

    # 在屏幕上绘制子弹
    def draw_bullet(self):
        # 在screen上绘制color的bulletRect
        pygame.draw.rect(self.screen, self.color, self.bulletRect)



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

    # 创建一个用来存放子弹的数组
    bullets = Group()

    # 得到事件对象
    game_function = game_functions()


    while True:
        # 检查按键
        game_function.check_events(mySettings,screen,ship,bullets)

        # 调用飞机更新方法。
        ship.update()

        # 更新子弹(更新+删除消失的)
        game_function.update_bullets(bullets)


        # 更新屏幕
        game_function.updata_screen(screen,mySettings,ship,bullets)


# 运行
run_game()