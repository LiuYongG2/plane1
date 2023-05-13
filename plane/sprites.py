import pygame
import random
from random import randint

# random.randrange(start, stop=None, step=1)

random.randrange(1, stop=20, step=1)
ENEMY_IMAGE_PATH = "./enemy2.png"
ENEMY_MIN_SPEED = 2
ENEMY_MAX_SPEED = 5
SEREEN_RECT = pygame.Rect(0, 0, 512, 768)


class GameSpritr(pygame.sprite.Sprite):
    def __init__(self, image_path, speed=0,speedy=0):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speed = speedy

    def update(self, *args):
        self.rect.y += self.speed
        self.rect.x += self.speedy


class Enemy(GameSpritr):
    def __init__(self):
        super().__init__("F:/altext/Python project/pythonProject5/plane/enemy2.png")
        self.rect.bottom = 0
        self.rect.x = random.randrange(0, SEREEN_RECT.width - self.rect.width, self.rect.width + 3)
        self.speed = random.randrange(1, 2)

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y > SEREEN_RECT.height:
            self.kill()


class Background(GameSpritr):
    def __init__(self, is_alt=False):
        super().__init__("./bg3.jpg", 2)
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.y >= SEREEN_RECT.height:
            self.rect.y = -self.rect.height


class Hero(GameSpritr):
    def __init__(self):
        super().__init__("./hero.png")
        self.rect.centerx = SEREEN_RECT.centerx
        self.rect.bottom = SEREEN_RECT.bottom - 100
        self.button_group = pygame.sprite.Group()

    def update(self, *args):
        # self.rect.x += self.speed
        # if hero_rect.left < 0:
        #     hero_rect.left = 0
        # if hero_rect.right > SEREEN_RECT.right:
        #     hero_rect.right = SEREEN_RECT.right
        self.rect.x += hero_speed
        self.rect.y += hero_speedy
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SEREEN_RECT.right:
            self.rect.right = SEREEN_RECT.right
        # hero_rect.y -= 3
        if self.rect.bottom < 0:
            self.rect.top = SEREEN_RECT.bottom

    def fire(self):
        for i in range(10):
            hero_bullet = Bullet()
            hero_bullet.rect.bottom = self.rect.y - 20 * i
            hero_bullet.rect.centerx = self.rect.centerx
            self.button_group.add(hero_bullet)


class Bullet(GameSpritr):
    def __init__(self):
        super().__init__("F:/altext/Python project/pythonProject5/plane/hero.png", -10)

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
