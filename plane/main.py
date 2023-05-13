# import pygame
#
# pygame.init()
# screen_rect = pygame.Rect(0, 0, 512, 768)
# screen = pygame.display.set_mode(screen_rect.size)
# bg = pygame.image.load("bg3.jpg")
# screen.blit(bg, (0, 0))
#
# hero = pygame.image.load("hero.png")
# hero_rect = hero.get_rect()
# hero_rect.centerx = screen_rect.centerx
# hero_rect.bottom = screen_rect.bottom - 100
# screen.blit(hero, hero_rect)
#
# clock = pygame.time.Clock()
# while True:
#     clock.tick(480)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 hero_rect.x -= 10
#             if event.key == pygame.K_RIGHT:
#                 hero_rect.x += 10
#             if event.key == pygame.K_UP:
#                 hero_rect.y -= 10
#             if event.key == pygame.K_DOWN:
#                 hero_rect.y += 10
#     # hero_rect.y -= 3
#     if hero_rect.bottom < 0:
#         hero_rect.top = screen_rect.bottom
#     screen.blit(bg, (0, 0))
#     screen.blit(hero, hero_rect)
#     pygame.display.update()
# pygame.quit()
import pygame
from sprites import Background, Hero, Enemy, Bullet, SEREEN_RECT

CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class PlaneWarGame:
    def __init__(self):
        pygame.init()
        # SEREEN_RECT = pygame.Rect(0, 0, 512, 768)
        self.screen = pygame.display.set_mode(SEREEN_RECT.size)
        self.__create_sprites()
        # hero = pygame.image.load("./hero.png")
        # hero_rect = hero.get_rect()
        # hero_rect.centerx = SEREEN_RECT.centerx
        # hero_rect.bottom = SEREEN_RECT.bottom - 100
        # screen.blit(hero, hero_rect)

        self.clock = pygame.time.Clock()

        pygame.time.set_timer(CREATE_ENEMY_EVENT, 100)
        pygame.time.set_timer(HERO_FIRE_EVENT, 100)

    def __create_sprites(self):
        # bg = pygame.image.load("./bg3.jpg")
        bg1 = Background()
        bg2 = Background(is_alt=True)
        self.hero = Hero()
        self.bg_group = pygame.sprite.Group(bg1, bg2)
        self.hero_group = pygame.sprite.Group(self.hero)
        # enemy_group = pygame.sprite.Group(*[Enemy() for item in range(20)])
        self.enemy_group = pygame.sprite.Group()
        # screen.blit(bg, (0, 0))

    @staticmethod
    def game_over():
        pygame.quit()
        exit()

    def listen_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy_group.add(Enemy())
            # elif event.type == HERO_FIRE_EVENT:
            #     self.hero.fire()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.hero.fire()
        keys_passed = pygame.key.get_pressed()
        if keys_passed[pygame.K_RIGHT]:
            self.hero_speed = 2
        elif keys_passed[pygame.K_LEFT]:
            self.hero_speed = -2
        elif keys_passed[pygame.K_UP]:
            self.hero_speedy = -2
        elif keys_passed[pygame.K_DOWN]:
            self.hero_speedy = 2
        else:
            self.hero_speed = 0
            self.hero_speedy = 0

    def check_collie(self):
        pygame.sprite.groupcollide(self.hero.button_group, self.enemy_group, True, True)
        # res = pygame.sprite.groupcollide(hero_group, enemy_group, True, True)
        # print(res)
        # if res:
        #     pygame.quit()
        #     exit()
        res = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        print(res)
        if res:
            self.hero.kill()
            self.game_over()

    def auto_update_sprites(self, *groups):
        for group in groups:
            group.update()
            group.draw(self.screen)

    def update_sprites(self):
        self.auto_update_sprites(
            self.bg_group,
            self.hero_group,
            self.enemy_group,
            self.hero.button_group
        )

    def start_game(self):
        while True:
            self.clock.tick(1080)
            self.listen_event()
            self.check_collie()
            self.update_sprites()
            pygame.display.update()


if __name__ == "__main__":
    PlaneWarGame().start_game()
