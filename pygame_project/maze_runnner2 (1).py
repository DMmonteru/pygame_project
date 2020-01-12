import pygame
import os
import random

pygame.init()
pygame.display.set_caption('maze_runner')
hero = (60, 70)
hero_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
CHANGE = 31
W, H = 800, 400
SCREEN = (W, H)
count = 0
enemy_animation_count = 0
screen = pygame.display.set_mode(SCREEN)
clock = pygame.time.Clock()
pygame.time.set_timer(CHANGE, 10)
NEW_PLATFORM = 16
NEW_COIN = 16
NEW_KNIFE = 1
NEW_ENEMY = 2
v = 20
jump_v = 0
g = 20
playerx = 30
playery = 100
enemy_change = False
attack = False
defend = False
# при увеличении этих констант, частота уменьшается
# и ноборот
enemy_frequency = 20000
platform_frequency = 700
coin_frequency = 2000
knife_frequency = 20000
coins = 0
x = 0
speed = 50
run = True
font = pygame.font.SysFont('comicsans', 30)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


bg = load_image('bg.png').convert()

pygame.time.set_timer(NEW_PLATFORM, 100)
pygame.time.set_timer(NEW_COIN, 100)


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.animations_with = [pygame.transform.scale(load_image('run1.png'), hero),
                                pygame.transform.scale(load_image('run2.png'), hero),
                                pygame.transform.scale(load_image('run3.png'), hero),
                                pygame.transform.scale(load_image('run4.png'), hero)]

        self.animations_without = [pygame.transform.scale(load_image('run1_without.png'), hero),
                                   pygame.transform.scale(load_image('run2_without.png'), hero),
                                   pygame.transform.scale(load_image('run3_without.png'), hero),
                                   pygame.transform.scale(load_image('run4_without.png'), hero)]

        pygame.time.set_timer(CHANGE, 1)

        self.image = self.animations_without[0]
        self.rect = self.image.get_rect()
        self.rect.x = playerx
        self.rect.y = playery

        pygame.time.set_timer(CHANGE, 100)

        self.coins = None

        self.enemies = pygame.sprite.Group()

        self.with_knife = False
        self.knife = None

        self.alive = True
        self.jumping = False

    def update(self):
        global playery
        global coins

        if self.with_knife:
            self.image = self.animations_with[count % len(self.animations_with)]
        else:
            self.image = self.animations_without[count % len(self.animations_without)]

        if playery >= H - hero[1] - 20:
            playery -= 4
        elif playery <= 10:
            playery = 10
            self.rect.y = 10
        else:
            self.rect.y = playery
        self.rect.x = playerx

        coins_hit_list = pygame.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            coins += 1
            coin.kill()

        knife_hit_list = pygame.sprite.spritecollide(self, self.knife, False)
        for knife in knife_hit_list:
            if not self.with_knife:
                knife.kill()
            self.with_knife = True

        if pygame.sprite.spritecollideany(self, self.enemies, False):
            if ((enemy_animation_count // 6) % 2 == 0 and defend) or ((enemy_animation_count // 6) % 2 != 0 and attack):
                self.alive = True
            else:
                self.alive = False
                self.kill()


player = Hero(hero_sprites)

platforms_heights = [100, 210, 340]


class Platform(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('road.png')
        self.image = pygame.transform.scale(self.image, (random.randint(100, 300), 10))
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = random.choice(platforms_heights)
        pygame.time.set_timer(NEW_PLATFORM, platform_frequency)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__()
        self.animation_run = [pygame.transform.scale(load_image('en_1.png'), hero),
                              pygame.transform.scale(load_image('en_2.png'), hero),
                              pygame.transform.scale(load_image('en_3.png'), hero),
                              pygame.transform.scale(load_image('en_4.png'), hero),
                              pygame.transform.scale(load_image('en_5.png'), hero),
                              pygame.transform.scale(load_image('en_6.png'), hero)]
        self.animation_attack = [pygame.transform.scale(load_image('enemy1.png'), hero),
                                 pygame.transform.scale(load_image('enemy2.png'), hero),
                                 pygame.transform.scale(load_image('enemy3.png'), hero),
                                 pygame.transform.scale(load_image('enemy4.png'), hero),
                                 pygame.transform.scale(load_image('enemy5.png'), hero),
                                 pygame.transform.scale(load_image('enemy6.png'), hero)]

        self.image = self.animation_run[0]
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = H - hero[1] - 20
        pygame.time.set_timer(NEW_ENEMY, enemy_frequency)

    def update(self):
        global enemy_change
        if not enemy_change:
            self.image = self.animation_run[enemy_animation_count % len(self.animation_run)]
        else:
            self.image = self.animation_attack[enemy_animation_count % len(self.animation_attack)]


enemies_list = pygame.sprite.Group()
enemy = Enemy(enemies_list)
enemies_list.add(enemy)
player.enemies = enemies_list


class Knife(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('knife.png')
        self.image = pygame.transform.scale(self.image, (50, 60))
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = platforms_heights[1] - 80
        pygame.time.set_timer(NEW_KNIFE, knife_frequency)


knife_list = pygame.sprite.Group()
knife = Knife(knife_list)
knife_list.add(knife)
player.knife = knife_list

coins_height = [platforms_heights[0] - 32, platforms_heights[1] - 32,
                platforms_heights[2] - 32]


class Coin(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('coin.png')
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = random.choice(coins_height)
        pygame.time.set_timer(NEW_COIN, coin_frequency)


coins_list = pygame.sprite.Group()
coin = Coin(coins_list)
coins_list.add(coin)
player.coins = coins_list

text_lost = font.render('you lost', 1, (255, 255, 255))

Platform(platforms)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == CHANGE:
            if jump_v:
                playery -= jump_v
                jump_v -= g
                if jump_v <= 0:
                    jump_v = 0
            else:
                for i in hero_sprites:
                    if not pygame.sprite.spritecollideany(i, platforms):
                        playery += g
            count += 1
            for i in platforms:
                i.rect.x -= v
            for i in coins_list:
                i.rect.x -= v
            for i in knife_list:
                i.rect.x -= v

        if event.type == NEW_ENEMY:
            Enemy(enemies_list)
            enemy_animation_count += 1
            if (enemy_animation_count // 6) % 2 != 0:
                enemy_change = True
            else:
                enemy_change = False
        else:
            if event.type == NEW_PLATFORM:
                Platform(platforms)
            if event.type == NEW_COIN:
                Coin(coins_list)
            if event.type == NEW_KNIFE:
                Knife(knife_list)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump_v = 50
            elif event.key == pygame.K_LEFT:
                defend = True
            elif event.key == pygame.K_RIGHT:
                attack = True
        defend = False
        attack = False

    bgx = x % bg.get_rect().width
    screen.blit(bg, (bgx - bg.get_rect().width, 0))
    if bgx < W:
        screen.blit(bg, (bgx, 0))
    x -= 1
    text_score = font.render(f'Score: {str(coins)}', 1, (255, 255, 255))
    if player.alive:
        screen.blit(text_score, (W - 100, 10))
        hero_sprites.draw(screen)
        hero_sprites.update()
        platforms.draw(screen)
        platforms.update()
        coins_list.draw(screen)
        coins_list.update()
        knife_list.draw(screen)
        knife_list.update()
        enemies_list.update()
        enemies_list.draw(screen)
    else:
        screen.blit(text_lost, (W // 2 - 60, H // 2 - 20))
    pygame.display.update()
    clock.tick(speed)
pygame.quit()
