import pygame
from random import randrange

SCREEN_RECT = pygame.Rect(0, 0, 512, 768)


# 创建游戏精灵基类
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=0):
        # 调用父类的初始化方法
        super().__init__()
        # 加载图像
        self.image = pygame.image.load(image_name)
        # 设置尺寸
        self.rect = self.image.get_rect()
        # 记录速度
        self.speed = speed

    def update(self, *args):
        # 默认在垂直方向移动
        self.rect.y += self.speed


# 创建精灵类，继承游戏精灵基类
class Background(GameSprite):
    def __init__(self):
        super().__init__("./bg3.jpg")


class Hero(GameSprite):
    def __init__(self):
        super().__init__("./hero2.png")
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 100

        # 创建子弹的精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self, *args):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        for i in range(6):
            hero_bullet = Bullet()
            hero_bullet.rect.bottom = self.rect.y - i * 20
            hero_bullet.rect.centerx = self.rect.centerx

            # 3. 将精灵添加到精灵组
            self.bullet_group.add(hero_bullet)


class Enemy(GameSprite):
    def __init__(self):
        super().__init__("./enemy2.png")
        self.speed = randrange(1, 10)
        self.rect.bottom = 0
        self.rect.x = randrange(0, SCREEN_RECT.width - self.rect.width, self.rect.width + 5)

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.bottom <= 0:
            self.rect.y = SCREEN_RECT.bottom


class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./bullet2.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
# 创建游戏主窗口
screen = pygame.display.set_mode(SCREEN_RECT.size)

# 创建精灵和精灵组
bg = Background()
hero = Hero()
bg_group = pygame.sprite.Group(bg)
hero_group = pygame.sprite.Group(hero)
enemy_group = pygame.sprite.Group()  # 定时添加敌机

# 创建游戏时钟
clock = pygame.time.Clock()

# 定时器绑定事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY_EVENT, 500)
pygame.time.set_timer(HERO_FIRE_EVENT, 200)

# 游戏循环
while True:
    # 事件监听
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == CREATE_ENEMY_EVENT:
            enemy_group.add(Enemy())
        elif event.type == HERO_FIRE_EVENT:
            hero.fire()
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     hero.fire()

    # 获取所有按键，按住方向键可以一直移动，松开方向键飞机停止
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_RIGHT]:
        hero.speed = 2
    elif keys_pressed[pygame.K_LEFT]:
        hero.speed = -2
    else:
        hero.speed = 0  # 没按方向键，速度设置为0

    # 碰撞检测
    pygame.sprite.groupcollide(hero.bullet_group, enemy_group, True, True)
    res = pygame.sprite.spritecollide(hero, enemy_group, True)
    # if res:
    #     hero.kill()
    #     pygame.quit()
    #     exit()

    # 设置屏幕刷新帧率
    clock.tick(1080)
    # 更新和绘制精灵
    bg_group.update()
    bg_group.draw(screen)
    hero_group.update()
    hero_group.draw(screen)
    enemy_group.update()
    enemy_group.draw(screen)
    hero.bullet_group.update()
    hero.bullet_group.draw(screen)
    # 更新屏幕显示
    pygame.display.update()
