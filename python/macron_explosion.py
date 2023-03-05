import entity
import pygame

class Explosion(entity.Entity):
    entities = []

    def __init__(self, display, position, frame):
        super().__init__(display, 0, 1)
        self.sprite = frame
        self.position = position
        self.rect = pygame.Rect(position, (64, 64))
        self.count = 0

    def draw(self):
        self.display.blit(self.sprite, self.rect)

    def all_kill(self):
        for explo in Explosion.entities:
            explo.kill()
