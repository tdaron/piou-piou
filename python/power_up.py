import random
import math
import pygame
import entity
from player import Player

class Power_up(entity.Entity):

    power_up_sprites = ['Assets/Power_ups/Orbe_jaune.png']
    down_timer = 60000
    up_timer = 10030
    clock = 0

    def __init__(self, display, init_position, category):
        super().__init__(display, 0, 1)
        self.category = category
        self.sprite = pygame.transform.scale_by(pygame.image.load(self.power_up_sprites[self.category]), 0.25)
        self.rect = pygame.Rect(init_position, (self.sprite.get_width(), self.sprite.get_height()))
        self.clock = pygame.time.Clock()
        self.angle = 0
        self.is_angle_set = False

    def move(self, speed=5):
        if not self.is_angle_set:
            self.angle = random.randint(0, 360)
            self.is_angle_set = True

        prev_x = self.rect.x
        prev_y = self.rect.y

        self.rect.x += math.cos(self.angle * math.pi / 180) * speed
        self.rect.y += math.sin(self.angle * math.pi / 180) * speed

        if self.rect.x + self.sprite.get_size()[0] > self.display.get_size()[0] or self.rect.x < 0:
            self.rect.x = prev_x
            self.is_angle_set = False
        if self.rect.y + self.sprite.get_size()[1] > self.display.get_size()[1] or self.rect.y < 0:
            self.rect.y = prev_y
            self.is_angle_set = False


    def draw(self):
        self.display.blit(self.sprite, self.rect)

    def on_touch(self, player: Player):
        if player.lvl == 5:
            player.score += 100
            return 0
        if self.category == 0:
            player.lvl += 1
        if self.category == 1:
            player.lives += 1

    def self_kill(self):
        self.kill()
        self.destroy()
