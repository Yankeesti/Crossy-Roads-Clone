import pygame
import config
import random
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image,x_pos,road_section): 
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x_pos,road_section.rect.bottomleft[1])
        self.road_section = road_section

    def __repr__(self) -> str:
        return f"Static Obstacle at {self.rect[0]},{self.rect[1]}"

class StaticObstacle(Obstacle):
    def __init__(self,x_pos, road_section,image = config.TREE_IMAGE):
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE))
        image.fill((0,0,0))

        super().__init__(image,x_pos,road_section)

class DynamicObstacle(Obstacle):
    def __init__(self,speed, road_section,image = config.CAR_IMAGE):
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE*1.8))
        image.fill((100,0,0))
        super().__init__(image,100,road_section)
        self.speed = speed

    def update(self):
        self.rect.move_ip(self.speed*config.BLOCK_SIZE,0)
        print(self.rect[0])
        if self.rect[0] > config.WINDOW_WIDTH:
            self.rect[0] = -100
    

    

    
    
