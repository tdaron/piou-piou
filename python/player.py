import entity
import pygame
from bullet import Bullet

class Player(entity.Entity):

    entities = []

    def __init__(self, id, display: pygame.display, init_position, damage, sprite, bullet_speed):
        super().__init__(display, damage, 1)
        self.ID = id
        self.lives = 3
        self.sprite = pygame.image.load(sprite)
        self.bullet_speed = bullet_speed
        self.rect = pygame.Rect((init_position[0]+self.sprite.get_width()//8, init_position[1]+self.sprite.get_height()//8), (self.sprite.get_width()*3//4, self.sprite.get_height()*3//4))
        self.width = self.rect.width
        self.last_message = None
        self.has_moved = False
        self.init_pos = init_position
        self.invulnerable = False
        self.invulnerableTime = 0
        self.lvl = 4
        self.god = False
        self.score = 0

    def get_hit(self, dmg):
        if self.invulnerable or self.god:
            return
        self.lives -= 1
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]
        self.invulnerable = True
        self.god = False
        self.invulnerableTime = 120 * 3

    def draw(self):
        if (self.invulnerableTime % 19) == 0:  # This weird thing is to blink player
            self.display.blit(self.sprite, self.rect)
        if self.invulnerableTime > 0:
            self.invulnerableTime -= 1
        else:

            if self.invulnerable:
                self.invulnerableTime = 0
                self.invulnerable = False

    def move_p(self, up_speed, down_speed, right_speed, left_speed, g_speed=2):
        prev_x = self.rect.x
        prev_y = self.rect.y

        self.rect.x += (right_speed - left_speed) * g_speed
        self.rect.y += (down_speed - up_speed) * g_speed

        if self.rect.x + self.sprite.get_size()[0] > self.display.get_size()[0] or self.rect.x < 0:
            self.rect.x = prev_x
        if self.rect.y + self.sprite.get_size()[1] > self.display.get_size()[1] or self.rect.y < 0:
            self.rect.y = prev_y


    def move_k(self, keys, speed=4):
        prev_x = self.rect.x
        prev_y = self.rect.y

        self.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * speed
        self.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * speed

        if self.rect.x + self.sprite.get_size()[0] > self.display.get_size()[0] or self.rect.x < 0:
            self.rect.x = prev_x
        if self.rect.y + self.sprite.get_size()[1] > self.display.get_size()[1] or self.rect.y < 0:
            self.rect.y = prev_y

    def self_kill(self):
        self.kill()
        self.destroy()

    def shoot(self):
        u = pygame.mixer.Sound("./Assets/Audio/gun-sound.wav")
        pygame.mixer.Sound.play(u)
        for i in range(self.lvl):
            if i < 3 and self.lvl < 2:
                player_projectile = Bullet(display=self.display,
                                           sprite="Assets/Projectiles/Small_yellow_shpere_1.png",
                                           init_position=(self.rect.x + self.rect.width * (i+1) // (self.lvl+1), self.rect.y),
                                           speed=self.bullet_speed, damage=self.damage, danger=False)
                player_projectile.shooter = self

            elif i < 3 and self.lvl >= 2:
                player_projectile = Bullet(display=self.display,
                                           sprite="Assets/Projectiles/Narrow_purple_1.png",
                                           init_position=(self.rect.x + self.rect.width * (i+1) // (self.lvl+1), self.rect.y),
                                           speed=self.bullet_speed, damage=self.damage, danger=False)
                player_projectile.shooter = self

            elif i == 3:

                player_projectile = Bullet(display=self.display,
                                           sprite="Assets/Projectiles/Narrow_purple_1.png",
                                           init_position=(self.rect.x + self.rect.width * (i+1) // (self.lvl+1), self.rect.y),
                                           speed=[2,-2], damage=self.damage, danger=False)
                player_projectile.shooter = self

            elif i == 4:
                player_projectile = Bullet(display=self.display,
                                           sprite="Assets/Projectiles/Narrow_purple_1.png",
                                           init_position=(self.spri.x + self.rect.width * (i+1) // (self.lvl+1), self.rect.y),
                                           speed=[-2,-2], damage=self.damage, danger=False)
                player_projectile.shooter = self
