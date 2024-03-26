import pygame
import config
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE))
        self.image.fill((255, 155, 82))
        self.rect = self.image.get_rect()
        self.rect.center = (450, 250)