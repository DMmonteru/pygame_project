import pygame
import os
import random

pygame.init()
hero = (60, 70)
all_sprites = pygame.sprite.Group()
border_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
CHANGE = 31
W, H = 800, 400
SCREEN = (W, H)
count = 0
screen = pygame.display.set_mode(SCREEN)
clock = pygame.time.Clock()
pygame.time.set_timer(CHANGE, 10)
NEW_PLATFORM = 16
NEW_COIN = 16
v = 20
jump_v = 0
g = 20
playerx = 30
playery = 100
# при увеличении этих констант, частота уменьшается
# и ноборот
platform_frequency = 700
coin_frequency = 2000
coins = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


bg = load_image('bg.png').convert()
x = 0
speed = 50
run = True
pygame.time.set_timer(NEW_PLATFORM, 100)
pygame.time.set_timer(NEW_COIN, 100)
font = pygame.font.SysFont('comicsans', 30)


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.run1 = load_image('run1.png')
        self.run2 = load_image('run2.png')
        self.run3 = load_image('run3.png')
        self.run4 = load_image('run4.png')

        self.run1 = pygame.transform.scale(self.run1, hero)
        self.run2 = pygame.transform.scale(self.run2, hero)
        self.run3 = pygame.transform.scale(self.run3, hero)
        self.run4 = pygame.transform.scale(self.run4, hero)

        self.animations = [self.run1, self.run2, self.run3, self.run4]

        pygame.time.set_timer(CHANGE, 1)

        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = playerx
        self.rect.y = playery

        pygame.time.set_timer(CHANGE, 100)

        self.coins = None

        self.enemies = pygame.sprite.Group()

        self.alive = True

    def update(self):
        global playery
        global coins
        self.image = self.animations[count % len(self.animations)]
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

        if pygame.sprite.spritecollideany(self, self.enemies, False):
            self.alive = False


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

player = Hero(all_sprites)
player.coins = coins_list
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
                for i in all_sprites:
                    if not pygame.sprite.spritecollideany(i, platforms):
                        playery += g
            count += 1
            for i in platforms:
                i.rect.x -= v
            for i in coins_list:
                i.rect.x -= v
        if event.type == NEW_PLATFORM:
            Platform(platforms)
        if event.type == NEW_COIN:
            Coin(coins_list)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_v = 50

    bgx = x % bg.get_rect().width
    screen.blit(bg, (bgx - bg.get_rect().width, 0))
    if bgx < W:
        screen.blit(bg, (bgx, 0))
    x -= 1
    text = font.render(f'Score: {str(coins)}', 1, (255, 255, 255))
    if player.alive:
        screen.blit(text, (W - 100, 10))
        all_sprites.draw(screen)
        all_sprites.update()
        platforms.draw(screen)
        platforms.update()
        coins_list.draw(screen)
        coins_list.update()
    pygame.display.update()
    clock.tick(speed)
