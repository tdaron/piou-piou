import pygame


class Entity(pygame.sprite.Sprite):
    all_sprite_list = pygame.sprite.Group()
    entities = []

    def __init__(self, display, damage, health):
        self.display: pygame.display = display
        super().__init__()
        self.damage = damage
        self.health = health
        Entity.all_sprite_list.add(self)
        self.__class__.entities.append(self)

    def destroy(self):
        Entity.all_sprite_list.remove(self)
        self.__class__.entities.remove(self)

    @staticmethod
    def draw_all():
        for obj in Entity.all_sprite_list.sprites(): # https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group.sprites
            obj.draw()
