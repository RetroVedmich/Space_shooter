from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x <= 700 - 66:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.top, 20, 35, 10)
        bullets.add(bullet)
    def super_fire(self):
        megabullet = SuperBullet('1597842113178278867 (1).png', player.rect.centerx - 50, player.rect.top, 102, 45, 4)
        megabullets.add(megabullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = -300
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class SuperBullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Bonus(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.kill()

window = display.set_mode((700, 500))
display.set_caption('Догонялки')

font.init()
font1 = font.SysFont('Segoe print', 25)
text_kills = font1.render('-0', True, (128, 0, 255))
text_lost = font1.render('-0', True, (128, 0, 255))
text_energy = font1.render('-0', True, (128, 0, 255))

background = transform.scale(image.load('dark-4487690_960_720.jpg'), (700, 500))
papich_image = transform.scale(image.load('mqdefault.jpg'), (700, 500))
loser_image = transform.scale(image.load('Без названия (5).jpg'), (700, 500))
win_image = transform.scale(image.load('8ff3fa9ae206d1d3d9f882620b4cefba.jpg'), (700, 500))
life_image = transform.scale(image.load('pixil-frame-0.png'), (110, 40))
player = Player('rocket.png', 317, 390, 66, 100, 5)
monsters = sprite.Group()
bullets = sprite.Group()
megabullets = sprite.Group()
bonus_group = sprite.Group()

for i in range(1, 3):
    monster = Enemy('ufo.png', randint(80, 700 - 80), -300, 80, 50, randint(1, 4))
    monsters.add(monster)

winner_moment = ''
papich_moment = ''
loser_moment = ''
lost = 0
life = 3

monster_time = 0
monster_deaths = 0
power = 400
bonus_time = 0

clock = time.Clock()
FPS = 60

mixer.init()
kick = mixer.Sound('brue.ogg')
kill = mixer.Sound('wilhelm_scream.ogg')
papich_sound = mixer.Sound('X2Download.ogg')
win_sound = mixer.Sound('7F1OCOSZMcIE.128.ogg')
loser_sound = mixer.Sound('battle-over-loser.ogg')
mixer.music.load('НеизвестенDreamspeedrunminecraft__ComedySong.ru_.ogg')
mixer.music.play()

x1 = 25
x2 = 675
y1 = 25
y2 = 300

game = True
while game:
    text_kills = font1.render('Я ЩАС УБЬЮ ВСЕХ: ' + str(monster_deaths), 1, (128, 0, 255))
    text_lost = font1.render('СБЕЖАВШИХ ИЗ САРАТОВА: ' + str(lost), 1, (128, 0, 255))
    text_energy = font1.render('Бюджет Роскосмоса: ' + str(power), 1, (128, 0, 255))
    

    window.blit(background, (0, 0))
    window.blit(text_kills, (0, 0))
    window.blit(text_lost, (0, 50))
    window.blit(text_energy, (0, 100))
    window.blit(life_image, (590, 10))
    player.reset()
    player.update()
    monsters.draw(window)
    monsters.update()
    bullets.draw(window)
    bullets.update()
    megabullets.draw(window)
    megabullets.update()
    bonus_group.draw(window)
    bonus_group.update()
    
    monster_time += 1
    power += 1

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and power >= 50:
                player.fire()
                power -= 50
            if e.key == K_LCTRL and power >= 250:
                player.super_fire()
                power -= 250
            if e.key == K_q and power >= 100 and life <= 2:
                bonus = Bonus('bonus.png', randint(80, 700 - 80), -300, 50, 50, 5)
                bonus_group.add(bonus)
                power -= 100
    
    if monster_time == 55:
        monster_time = 0
        new_monster = Enemy('ufo.png', randint(80, 700 - 80), -300, 80, 50, randint(1, 4))
        monsters.add(new_monster)
    if monster_deaths >= 99:
        win_sound.play()
        player.rect.x = 200000
        player.rect.y = 5000
        winner_moment = True
    if power >= 400:
        power = 400
    if sprite.spritecollide(player, monsters, True):
        life -= 1
        kick.play()
    if life >= 3:
        life_image = transform.scale(image.load('pixil-frame-0.png'), (110, 40))
        life = 3
    if life == 2:
        life_image = transform.scale(image.load('pixil-frame-0 (1).png'), (110, 40))
    if life == 1:
        life_image = transform.scale(image.load('pixil-frame-0 (2).png'), (110, 40))
    if life <= 0 or lost >= 15:
        player.rect.x = 200000
        player.rect.y = 5000
        life = 1000000000000
        lost = -100000000000
        if monster_deaths == 0:
            papich_moment = True
            papich_sound.play()
        else:
            loser_moment = True
            loser_sound.play()
    if papich_moment == True:
        window.blit(papich_image, (0, 0))
    if loser_moment == True:
        window.blit(loser_image, (0, 0))
    if winner_moment == True:
        window.blit(win_image, (0, 0))
        lost = -10000000000000
    if sprite.groupcollide(bullets, monsters, True, True):
        kill.play()
        monster_deaths += 1
    if sprite.groupcollide(megabullets, monsters, False, True):
        kill.play()
        monster_deaths += 1
    if sprite.spritecollide(player, bonus_group, True):
        life += 1

    display.update()
    clock.tick(FPS)