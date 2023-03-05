from entity import Entity
import pygame


class Bullet(Entity):
    entities = []
    player_bullet_sprites = pygame.sprite.Group()
    enemy_bullet_sprites = pygame.sprite.Group()

    def __init__(self, display, sprite, init_position, speed, damage, danger=True):
        super().__init__(display, damage, 1)
        self.danger = danger
        self.display = display
        self.damage = damage
        self.speed = speed
        self.shooter = None

        if danger:
            Bullet.enemy_bullet_sprites.add(self)
            img = pygame.transform.rotate(pygame.image.load(sprite).convert_alpha(), 180)
            self.sprite = pygame.transform.scale(img, (img.get_width(), img.get_height()))
        else:
            Bullet.player_bullet_sprites.add(self)
            self.sprite = pygame.image.load(sprite)
        self.rect = pygame.Rect((init_position[0]-self.sprite.get_width()//2, init_position[1]-self.sprite.get_height()//2), (self.sprite.get_width()*1//2, self.sprite.get_height()*1//2))
        print(self.sprite.get_size())
        print(self.rect.size)
        self.width = self.rect.width


    def draw(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.display.blit(self.sprite, self.rect)

    def self_kill(self):
        self.kill()
        self.destroy()
