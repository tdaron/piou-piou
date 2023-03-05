import entity
import pygame
import bullet

class Enemy(entity.Entity):

    entities = []

    def __init__(self, display, init_position, sprite, bullet_sprite, bullet_speed, speed=(0, 5), damage=30, health=5, reload_time=3, type='None'):
        super().__init__(display, damage, health)
        self.reload_time = reload_time
        self.bullet_speed = bullet_speed
        self.clock = 0
        img = pygame.transform.rotate(pygame.image.load(sprite).convert_alpha(), 180)
        self.sprite = pygame.transform.scale(img, (img.get_width()/2, img.get_height()/2))
        self.speed = speed
        self.rect = pygame.Rect((init_position[0]+self.sprite.get_width()//8, init_position[1]+self.sprite.get_height()//8), (self.sprite.get_width()*3//4, self.sprite.get_height()*3//4))


        self.width = self.rect.width
        self.bullet_sprite = bullet_sprite
        self.type = type
        if type == 'cyclic':
            self.cycle_count = 0


    def get_hit(self, dmg):
        self.health -= dmg

    def draw(self):
        self.display.blit(self.sprite, self.rect)

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.clock += 0.1

    def self_kill(self):
        self.kill()
        self.destroy()

    @staticmethod
    def move_all():
        for enemy in Enemy.entities:
            enemy.move()
            if enemy.type=="cyclic":
                enemy.cycle_count+=1
                if int(enemy.cycle_count)==100:
                    enemy.speed = [enemy.speed[1],enemy.speed[0]]
                if int(enemy.cycle_count)==500:
                    enemy.speed = [-1*enemy.speed[1],-1*enemy.speed[0]]
                if int(enemy.cycle_count) == 600:
                    enemy.speed = [enemy.speed[1],enemy.speed[0]]
                if int(enemy.cycle_count) == 10000:
                    enemy.speed = [-1*enemy.speed[1],-1*enemy.speed[0]]
                    enemy.cycle_count = 0

    def shoot(self,speed):
        bullet.Bullet(display=self.display,
                        sprite=self.bullet_sprite,
                        init_position=(self.sprite.x + self.sprite.get_width(), self.sprite.y + self.sprite.get_height()), speed=speed,
                        damage=self.damage, danger=True)
