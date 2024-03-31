import pygame
import config
import random
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image,x_pos,road_section): 
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x_pos,road_section.rect.bottomleft[1])

    def __repr__(self) -> str:
        return f"Static Obstacle at {self.rect[0]},{self.rect[1]}"

class StaticObstacle(Obstacle):
    def __init__(self,x_pos, road_section,image = config.TREE_IMAGE):
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE))
        image.fill((0,0,0))

        super().__init__(image,x_pos,road_section)

class DynamicObstacle(Obstacle):
    def __init__(self,x_pos, road_section,image = config.TREE_IMAGE):
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE))
        image.fill((100,0,0))
        super().__init__(image,x_pos,road_section)

    
    
