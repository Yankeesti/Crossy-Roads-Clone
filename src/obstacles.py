import pygame
import config
def get_random_x_positions(amount : int):
    pass

def ObstacleFactory(x_positions : list,type : str):
    """Creates Obstacles from type type at x_positions"""
    return [StaticObstacle(x_pos) for x_pos in x_positions]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image,x_pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x_pos,0)
    
    def adjust_y(self,section):
        self.rect.midleft = (self.rect.midleft[0],section.rect.midleft[1])

class StaticObstacle(Obstacle):
    def __init__(self,x_pos, image = config.TREE_IMAGE):
        super().__init__(image,x_pos)
