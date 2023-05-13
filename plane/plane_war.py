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
    def __init__(self, image_path, speed=0):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self, *args):
        self.rect.y += self.speed


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


pygame.init()
# SEREEN_RECT = pygame.Rect(0, 0, 512, 768)
screen = pygame.display.set_mode(SEREEN_RECT.size)
# bg = pygame.image.load("./bg3.jpg")
bg1 = Background()
bg2 = Background(is_alt=True)
hero = Hero()
bg_group = pygame.sprite.Group(bg1, bg2)
hero_group = pygame.sprite.Group(hero)
# enemy_group = pygame.sprite.Group(*[Enemy() for item in range(20)])
enemy_group = pygame.sprite.Group()
# screen.blit(bg, (0, 0))

# hero = pygame.image.load("./hero.png")
# hero_rect = hero.get_rect()
# hero_rect.centerx = SEREEN_RECT.centerx
# hero_rect.bottom = SEREEN_RECT.bottom - 100
# screen.blit(hero, hero_rect)

clock = pygame.time.Clock()
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY_EVENT, 100)
pygame.time.set_timer(HERO_FIRE_EVENT, 100)
while True:
    clock.tick(1080)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == CREATE_ENEMY_EVENT:
            enemy_group.add(Enemy())
        # elif event.type == HERO_FIRE_EVENT:
        #     hero.fire()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            hero.fire()
    keys_passed = pygame.key.get_pressed()
    if keys_passed[pygame.K_RIGHT]:
        hero_speed = 2
    elif keys_passed[pygame.K_LEFT]:
        hero_speed = -2
    elif keys_passed[pygame.K_UP]:
        hero_speedy = -2
    elif keys_passed[pygame.K_DOWN]:
        hero_speedy = 2
    else:
        hero_speed = 0
        hero_speedy = 0
    pygame.sprite.groupcollide(hero.button_group, enemy_group, True, True)
    # res = pygame.sprite.groupcollide(hero_group, enemy_group, True, True)
    # print(res)
    # if res:
    #     pygame.quit()
    #     exit()
    res = pygame.sprite.spritecollide(hero, enemy_group, True)
    print(res)
    if res:
        hero.kill()
        pygame.quit()
        exit()
    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT:
    #             hero_speed -= 10
    #         if event.key == pygame.K_RIGHT:
    #             hero_speed += 10
    #         if event.key == pygame.K_UP:
    #             hero_rect.y -= 10
    #         if event.key == pygame.K_DOWN:
    #             hero_rect.y += 10
    #     elif event.type == pygame.KEYUP:
    #         if event.key == pygame.K_RIGHT:
    #             hero_speed = 0
    # hero_rect.x += hero_speed
    # hero_rect.y += hero_speedy
    # if hero_rect.left < 0:
    #     hero_rect.left = 0
    # if hero_rect.right > SEREEN_RECT.right:
    #     hero_rect.right = SEREEN_RECT.right
    # # hero_rect.y -= 3
    # if hero_rect.bottom < 0:
    #     hero_rect.top = SEREEN_RECT.bottom
    # screen.blit(bg, (0, 0))
    # screen.blit(hero, hero_rect)
    bg_group.update()
    bg_group.draw(screen)
    hero_group.update()
    hero_group.draw(screen)
    enemy_group.update()
    enemy_group.draw(screen)
    hero.button_group.update()
    hero.button_group.draw(screen)
    pygame.display.update()
