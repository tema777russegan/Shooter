#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

MissedCounter = 0
bullets = sprite.Group()
score = 0
num_fire = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 75:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global MissedCounter
        if self.rect.y >= 500:
            self.rect.x = randint(80, 600)
            self.rect.y = -50
            self.speed = randint(1, 3)
            MissedCounter += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -20:
            self.kill()
            
class Aster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = -50
            self.rect.x = randint(80, 620)
            self.speed = randint(1, 3)



mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

font.init()
font = font.SysFont("Arial", 30)
scoreText = font.render("счёт:", True, (255, 255, 255))
missedText = font.render("пропущено:", True, (255, 255, 255))
reloadText = font.render('Wait, reload...', 1, (255, 255, 255))

win_width = 700
win_height = 500
Rocket = Player('rocket.png', 300, 380, 65, 110, 6)
rockets = sprite.Group
rockets.add(Rocket)
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

ufos = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 5):
   UFO = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
   ufos.add(UFO)

for i in range(1, 3):
   Asteroid = Aster("asteroid.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
   asteroids.add(Asteroid)

game = True
finish = False
clock = time.Clock()
FPS = 60
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               if num_fire < 12 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    Rocket.fire()
               if num_fire  >= 12 and rel_time == False :
                    last_time = timer()
                    rel_time = True
           if e.key == K_UP:
               finish = False
               MissedCounter = 0
               score = 0
               num_fire = 0
               life = 3
               for UFO in ufos:
                   UFO.kill()
               for i in range(1, 5):
                   UFO = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
                   ufos.add(UFO)
               Rocket.rect.x = 300
               for Asteroid in asteroids:
                   Asteroid.kill()
               for i in range(1, 3):
                   Asteroid = Aster("asteroid.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
                   asteroids.add(Asteroid)

    if sprite.groupcollide(ufos, asteroids, True, False):
        UFO = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
        ufos.add(UFO)

    if sprite.groupcollide(ufos, bullets, True, True):
        score += 1
        UFO = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
        ufos.add(UFO)
    
    sprite.groupcollide(asteroids, bullets, False, True)

    if score >= 30 and not sprite.spritecollide(Rocket, ufos, False):
        winText = font.render("YOU WIN!", True, (0, 255, 0))
        window.blit(winText, (280, 200))
        finish = True

    if MissedCounter >= 10:
        finish = True
        looseText = font.render("YOU LOOSE!", True, (255, 0, 0))
        window.blit(looseText, (280, 200))

    if sprite.spritecollide(Rocket, ufos, False) or sprite.spritecollide(Rocket, asteroids, False):
        finish = True
        looseText = font.render("YOU LOOSE!", True, (255, 0, 0))
        window.blit(looseText, (280, 200))

    if finish != True:

        window.blit(background,(0, 0))
        window.blit(scoreText,(10, 20))
        window.blit(missedText,(10, 50))
        Rocket.update()
        ufos.update()
        bullets.update()
        asteroids.update()

        if rel_time == True:
          now_time = timer()
       
          if now_time - last_time < 1:
              window.blit(reloadText, (260, 400))
          else:
              num_fire = 0
              rel_time = False

        Rocket.reset()
        ufos.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        missedAmountText = font.render(str(MissedCounter), True, (255, 255, 255))
        window.blit(missedAmountText, (150, 50))

        scoreAmount = font.render(str(score), True, (255, 255, 255))
        window.blit(scoreAmount, (75, 20))

    display.update()
    clock.tick(FPS)