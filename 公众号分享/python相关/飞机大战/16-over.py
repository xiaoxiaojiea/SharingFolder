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
        self.rect = self.image.get_rect()
        # print(self.rect)  # <rect(0, 0, 128, 128)>
        # 得到游戏窗口的边界对象
        self.screen_rect = screen.get_rect()
        # print(self.screen_rect)  # <rect(0, 0, 500, 600)>

        # 设置飞船的x轴中心是屏幕的中心
        self.rect.centerx = self.screen_rect.centerx
        # self.rect.left = 186

        # 设置飞船的底部是屏幕的底部
        self.rect.bottom = self.screen_rect.bottom
        # self.rect.bottom = 472+128  # bottom

        # print(self.rect)  # <rect(186, 472, 128, 128)>

        # 移动标志（目的是让他连续移动）: 按下右箭头键时将moving_right设置为True,松开时设置为False.
        self.moving_right = False
        self.moving_left = False

    # 在指定位置设置飞船
    def blitme(self):
        # 将飞船image，绘制在rect位置
        self.screen.blit(self.image, self.rect)

    # 飞船更新函数。
    def update(self):

        if self.moving_right:
            #
            self.rect.centerx += 1

        elif self.moving_left:
            self.rect.centerx -= 1



# 一些设置类
"""
1, __init__ 方法：放了一些常量数据定义。
"""
class Settings():

    # 放了一些数据定义。
    def __init__(self):

        # 常量数据设置。
        self.screen_width = 900
        self.screen_height = 700
        self.bg_color = (230,230,230)

        # 子弹数据设置
        self.bullet_speed_factor = 1  # 速度
        self.bullet_width = 3  # 宽
        self.bullet_height = 15 # 高
        self.bullet_color = 60, 60, 60  # 颜色

        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1


# 抽取模块：放置一些功能函数。
class game_functions():

    # 检查按键的事件。
    def check_events(self,mySettings,screen,ship,bullets):

        # 遍历所有事件，检查事件是什么。
        for event in pygame.event.get():

            # 退出事件
            if event.type == pygame.QUIT:
                pygame.QUIT()
                sys.exit()

            # 键盘按下事件
            elif event.type == pygame.KEYDOWN:
                # 键盘按下，去执行这个函数。
                self.check_keydown_events(mySettings, screen,event,ship,bullets)

            # 键盘抬起事件。
            elif event.type == pygame.KEYUP:
                # 键盘抬起，去执行这个函数。
                self.check_keyup_events(event,ship)


    # 键盘按下事件
    def check_keydown_events(self, mySettings, screen,event,ship,bullets):

        # 按下 右键。
        if event.key == pygame.K_RIGHT:
            # 飞船向右移动
            ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            # 飞船向左移动
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
            # 不让移动
            ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            ship.moving_left = False


    # 屏幕更新函数: （屏幕，设置参数，飞船对象）
    def updata_screen(self,screen,mySettings,ship,bullets,aliens):

        # 屏幕绘制背景图像。
        screen.fill(mySettings.bg_color)

        # 绘制子弹。
        for bullet in bullets.sprites():
            # 遍历出子弹组中的每一个子弹，绘制在屏幕上。
            bullet.draw_bullet()

        # 调用绘制飞船的方法（放在fill后边，确保飞船绘制在背景上面）
        ship.blitme()

        # 绘制外星人
        aliens.draw(screen)

        # 显示屏幕。
        pygame.display.flip()


    # 子弹的更新。
    def update_bullets(self,mySetting,screen,ship,aliens,bullets):
        # 调用
        bullets.update()

        # 删除消失的子弹
        for bullet in bullets.copy():
            # 子弹的底部坐标小于0，就删掉这个子弹。
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        # print(len(bullets))

        # 检查是否有子弹击中了外星人
        # 如果是这样，就删除相应的子弹和外星人
        """
            这行代码遍历编组bullets中的每颗子弹，再遍历编组aliens中的每个外星人。
            每当 有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键值对。
            两个实参True告诉Pygame删除发生碰撞的子弹和外星人。

        """
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

        # 外星人没有之后，删除现有的子弹并新建一群外星人
        if len(aliens) == 0:
            bullets.empty()
            # 调用创建外星人群组的方法。
            self.create_fleet(mySetting, screen, ship, aliens)


    # 计算每行可以容纳多少个外星人
    def get_number_aliens_x(self,mySettings, alien_width):
        # 去两边算算还有多少空间
        available_space_x = mySettings.screen_width - 2 * alien_width
        # 再算算 一个飞机+空半个飞机 可以放几个
        number_aliens_x = int(available_space_x / (2 * alien_width))

        return number_aliens_x

    # 创建一个外星人并将其放在当前行
    def create_alien(self,mySettings, screen, aliens, alien_number,row_number):
        # 创建一个外星人
        alien = Alien(mySettings, screen)
        # 得到外星人的宽度
        alien_width = alien.rect.width

        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number

        # 外星人x轴位置 = 本身宽度 + yi个飞机的位置*当前是第几个
        alien.x = alien_width + 2 * alien_width * alien_number

        alien.rect.x = alien.x
        # 加入到 外星人群组中。
        aliens.add(alien)

    # 计算屏幕可容纳多少行外星人
    def get_number_rows(self,mySettings, ship_height, alien_height):
        # 屏幕可用y = 屏幕height - 飞船高 - 3个飞机宽度的间隔
        available_space_y = (mySettings.screen_height - (3 * alien_height) - ship_height)
        # 计算可放几行
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows



    # 创建外星人群组
    def create_fleet(self, mySettings, screen, ship, aliens):
        # 得到一个外星人
        alien = Alien(mySettings, screen)
        # 得到一行可以放的外星人的数量
        number_aliens_x = self.get_number_aliens_x(mySettings, alien.rect.width)
        # 计算屏幕可以放多少行外星人
        number_rows = self.get_number_rows(mySettings, ship.rect.height, alien.rect.height)

        # 可以放几行外星人。
        for row_number in range(number_rows):
            # 一行可以放几个外星人
            for alien_number in range(number_aliens_x):
                # 创建外星人
                self.create_alien(mySettings, screen, aliens, alien_number,row_number)


    # 更新外星人群中所有外星人的位置
    def update_aliens(self,mySettings,screen,ship,aliens):
        # 检查外星人是否走向边缘了。
        self.check_fleet_edges(mySettings, aliens)

        # 更新
        aliens.update()

        # 检测外星人和飞船之间的碰撞
        """
            方法spritecollideany()接受两个实参：一个精灵和一个编组。
            它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生了碰撞的成员后就停止遍历编组。
        """
        if pygame.sprite.spritecollideany(ship, aliens):
            self.ship_hit()

        # 检查外星人是不是到底部了。
        self.check_aliens_bottom(screen,aliens)



    # 有外星人到达边缘时采取相应的措施
    def check_fleet_edges(self,mySettings, aliens):
        # 只要有一个外星人到达边缘，那就设置其反向运动。
        for alien in aliens.sprites():
            if alien.check_edges():
                # 设置运动方向反向（就是乘以 -1）
                self.change_fleet_direction(mySettings, aliens)
                break

    # 将整群外星人下移，并改变它们的方向
    def change_fleet_direction(self,mySettings, aliens):

        # 当每次触碰到边缘，就整体往下移动一次。
        for alien in aliens.sprites():
            alien.rect.y += 30
        # 改变方向
        mySettings.fleet_direction *= -1

    # 响应被外星人撞到的飞船
    def ship_hit(self):
        # 关闭窗口
        pygame.quit()
        # 结束程序
        sys.exit()

    # 检查是否有外星人到达了屏幕底端
    def check_aliens_bottom(self, screen, aliens):
        # 得到屏幕的矩形对象
        screen_rect = screen.get_rect()

        # 循环判断每个外星人。
        for alien in aliens.sprites():
            # 如果某一个外星人底部大于屏幕底部
            if alien.rect.bottom >= screen_rect.bottom:
                # 调用终止函数。
                self.ship_hit()

                break


# 子弹类
class Bullet(Sprite):

    # 传入数据，屏幕，飞船
    def __init__(self, mySettings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # 在(0,0)处创建一个表示子弹的矩形，
        self.rect = pygame.Rect(0, 0, mySettings.bullet_width, mySettings.bullet_height)

        # 再设置正确的位置
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)  # self.y表示子弹的y轴位置。

        self.color = mySettings.bullet_color
        self.speed_factor = mySettings.bullet_speed_factor

    # 子弹会自己向上跑
    def update(self):
        self.y -= self.speed_factor  # y减少，就是往上跑。
        # 将y的新数据写入子弹的属性中。
        self.rect.y = self.y

    # 在屏幕上绘制子弹
    def draw_bullet(self):
        # 在screen上绘制color的rect
        pygame.draw.rect(self.screen, self.color, self.rect)


# 外星人类
class Alien(Sprite):
    # 传入参数，以及屏幕
    def __init__(self, mySettings, screen):
        super(Alien, self).__init__()
        # 得到传入数据
        self.screen = screen
        self.mySettings = mySettings

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('./images/alien.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    # 在指定位置绘制外星人
    def blitme(self):
        # blit()不会更新屏幕-它在缓冲区中绘制图像。
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 速度*方向参数
        self.x += (0.5 * self.mySettings.fleet_direction)
        self.rect.x = self.x

    # 检测外星人是否位于屏幕边缘,如果外星人位于屏幕边缘，就返回True
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        # 外星人右边 大于等于 屏幕右边
        if self.rect.right >= screen_rect.right:
            return True

        # 外星人左边 小于等于 0
        elif self.rect.left <= 0:
            return True



# 程序执行主类。
def run_game():

    # 初始化一下pygame， 检查一遍，这个工具包是否完整。
    pygame.init()

    # 得到设置类对象：（）
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

    # 外星人群 数组
    aliens = Group()
    # 创建外星人群
    game_function.create_fleet(mySettings, screen,ship, aliens)

    while True:
        # 检查按键
        game_function.check_events(mySettings,screen,ship,bullets)

        # 调用飞机更新方法。
        ship.update()

        # 更新子弹(更新+删除消失的)
        game_function.update_bullets(mySettings,screen,ship,aliens,bullets)

        # 让外星人移动
        game_function.update_aliens(mySettings,screen,ship,aliens)

        # 更新屏幕
        game_function.updata_screen(screen,mySettings,ship,bullets,aliens)

# 运行
run_game()