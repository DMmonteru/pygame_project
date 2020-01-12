import pygame
import os
import random

pygame.init()
pygame.display.set_caption('maze_runner')
W, H = 800, 400
SCREEN = (W, H)
screen = pygame.display.set_mode(SCREEN)

hero = (60, 70)
hero_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# анимация
clock = pygame.time.Clock()
CHANGE = 31
pygame.time.set_timer(CHANGE, 10)
count = 0
enemy_animation_count = 0
dragon_animation_count = 0

# события
NEW_PLATFORM = 16
NEW_COIN = 16
NEW_KNIFE = 1
NEW_ENEMY = 1
NEW_DRAGON = 1

v = 20  # скорость движения посторонних объектов
jump_v = 0  # скорость прыжка
g = 20  # ускорение
playerx = 30  # начальная координата X
playery = 100  # начальная координата Y
# при увеличении этих констант, частота уменьшается
# и ноборот
enemy_frequency = 20000
platform_frequency = 400
coin_frequency = 2000
knife_frequency = 15000
dragon_frequency = 10000
coins = 0  # счёт
x = 0
speed = 50  # FPS
font = pygame.font.SysFont('comicsans', 30)  # шрифт


# best score
def updatefile():
    global coins
    with open('best_score.txt', 'r') as bs:
        last = int(bs.readline())

    if last < coins:
        with open('best_score.txt', 'w') as bs:
            bs.write(str(coins))
        return coins
    return last


# загрузка изображений
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


# главный герой
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
        self.dragons = pygame.sprite.Group()

        self.with_knife = False
        self.knife = None

        self.alive = True

    def update(self):
        global playery
        global coins
        global best_score

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
            if not self.with_knife:
                if updatefile() < coins:
                    with open('best_score.txt', 'w') as bs:
                        bs.write(str(coins))
                self.alive = False

        if pygame.sprite.spritecollideany(self, self.dragons, False):
            if not self.with_knife:
                if updatefile() < coins:
                    with open('best_score.txt', 'w') as bs:
                        bs.write(str(coins))
                self.alive = False


player = Hero(hero_sprites)
# платформы
platforms_heights = [140, 280]


class Platform(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('road.png')
        self.image = pygame.transform.scale(self.image, (random.randint(100, 300), 10))
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = random.choice(platforms_heights)
        pygame.time.set_timer(NEW_PLATFORM, platform_frequency)


# противник №1 - самурай
class Enemy(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.animation_attack = [load_image('enemy1.png'),
                                 load_image('enemy2.png'),
                                 load_image('enemy3.png'),
                                 load_image('enemy4.png'),
                                 load_image('enemy5.png'),
                                 load_image('enemy6.png')]

        self.image = self.animation_attack[0]
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = H - hero[1] - 30
        pygame.time.set_timer(NEW_ENEMY, enemy_frequency)

    def update(self):
        self.rect.x -= 6
        self.image = self.animation_attack[enemy_animation_count % len(self.animation_attack)]


enemies_list = pygame.sprite.Group()
enemy = Enemy(enemies_list)
enemies_list.add(enemy)
player.enemies = enemies_list


# противник №2 - дракон
class Dragon(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.animation = [load_image('dragon1.png'),
                          load_image('dragon2.png'),
                          load_image('dragon3.png'),
                          load_image('dragon4.png'),
                          load_image('dragon5.png'),
                          load_image('dragon6.png'),
                          load_image('dragon7.png'),
                          load_image('dragon8.png')]

        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect.x = W
        self.rect.y = platforms_heights[1] - 120
        pygame.time.set_timer(NEW_DRAGON, dragon_frequency)

    def update(self):
        self.rect.x -= 6
        self.image = self.animation[dragon_animation_count % len(self.animation)]


dragon_list = pygame.sprite.Group()
dragon = Dragon(dragon_list)
dragon_list.add(dragon)
player.dragons = dragon_list


# секиры(ножи)
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
                H - 52]


# монеты
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

Platform(platforms)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # прыжок
        if event.type == CHANGE:
            if jump_v:
                jumping = True
                playery -= jump_v
                jump_v -= g
                if jump_v <= 0:
                    jump_v = 0
            else:
                for i in hero_sprites:
                    if not pygame.sprite.spritecollideany(i, platforms):
                        playery += g

            # анимация
            count += 1
            enemy_animation_count += 1
            dragon_animation_count += 1
            for i in platforms:
                i.rect.x -= v
            for i in coins_list:
                i.rect.x -= v
            for i in knife_list:
                i.rect.x -= v

        # события
        if event.type == NEW_ENEMY:
            Enemy(enemies_list)
        if event.type == NEW_DRAGON:
            Dragon(dragon_list)
        else:
            if event.type == NEW_PLATFORM:
                Platform(platforms)
            if event.type == NEW_COIN:
                Coin(coins_list)
            if event.type == NEW_KNIFE:
                Knife(knife_list)

        # прыжок по нажатию
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump_v = 65

    # анимация фонового изображения
    bgx = x % bg.get_rect().width
    screen.blit(bg, (bgx - bg.get_rect().width, 0))
    if bgx < W:
        screen.blit(bg, (bgx, 0))
    x -= 1

    # отрисовка
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
        dragon_list.update()
        dragon_list.draw(screen)
    else:
        text_lost = font.render('you lost', 1, (255, 255, 255))
        screen.blit(text_lost, (W // 2 - 40, H // 2 - 20))
        text_bs = font.render(f'best score - {str(updatefile())}', 1, (255, 255, 255))
        screen.blit(text_bs, (W // 2 - 70, H // 2))
    pygame.display.update()
    clock.tick(speed)

pygame.quit()
