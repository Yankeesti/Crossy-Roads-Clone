from typing import Any
import pygame
import config
import obstacles
import random

class RoadSectionManager(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RoadSectionManager, cls).__new__(cls)
             #initialise negative Sections(Sections that can not be accesed by player but are displayed on lower Sections)
            section_neg_two = StaticRoadSection(-2)
            section_neg_one = StaticRoadSection (-1)
            section_neg_two.next_section = section_neg_one
            section_neg_one.previous_section = section_neg_two
            cls._instance.road_sections = [StaticRoadSection(0,previeous_section= section_neg_one,static_obstacle_pos=[])]
            section_neg_one.next_section = cls._instance.road_sections[0]
        return cls._instance
    
    def generate_sections(self,min_generated_sections = 1):
        for i in range(len(self.road_sections),len(self.road_sections)+min_generated_sections):
            self.road_sections.append(StaticRoadSection(i,self.road_sections[i-1]))
            self.road_sections[i-1].next_section = self.road_sections[i] 

    def update(self):
        pass

#Roadsections should only be created by RoadSectionManager
class RoadSection(pygame.sprite.Sprite):
    def __init__(self,index,surface,previeous_section,next_section,static_obstacles_pos):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.index = index
        self.rect.bottomleft = (0,-(index*config.BLOCK_SIZE))
        self.next_section = next_section
        self.previous_section = previeous_section
        self.players_on_section = []
        self.sections_to_draw = None
        self.road_section_manager = RoadSectionManager()
        self.static_obstacles = pygame.sprite.Group()
        self.init_static_obstacles(static_obstacles_pos)

    def init_static_obstacles(self,static_obstacle_pos:list): 
       for pos in static_obstacle_pos:
              self.static_obstacles.add(obstacles.StaticObstacle(pos*config.BLOCK_SIZE,self))
    
    def get_sections_to_draw(self):
        if self.sections_to_draw is not None:
            return self.sections_to_draw
        self.sections_to_draw = [self.previous_section.previous_section,self.previous_section,self]
        next_section = self
        for i in range(0,config.DISPLAYED_ROAD_SECTIONS - 2):
            if next_section.next_section is None:
                self.road_section_manager.generate_sections(config.DISPLAYED_ROAD_SECTIONS - i)
            next_section = next_section.next_section
            self.sections_to_draw.append(next_section)
        return self.sections_to_draw

    def add_player(self,player):
        self.players_on_section.append(player)
        
    def remove_player(self,player):
        self.players_on_section.remove(player)

    def update(self):
        # Add any update logic for the road section here
        pass

    def draw(self,surface,y_offset):
        # print("index",self.index,"y offset", y_offset,"self rect :",self.rect)
        surface.blit(self.image,(0,self.rect[1] - y_offset))
        for static_obstacle in self.static_obstacles:
            surface.blit(static_obstacle.image,(static_obstacle.rect[0],static_obstacle.rect[1] - y_offset))

class StaticRoadSection(RoadSection):
    def __init__(self,index,previeous_section = None,next_section = None,static_obstacle_pos = None):
        image = pygame.Surface((config.WINDOW_WIDTH, config.BLOCK_SIZE),pygame.SRCALPHA)
        if static_obstacle_pos is None:
            static_obstacle_pos = random.sample(range(0,config.ROAD_COLUMNS+2*config.UNSTEPABLEE_COLUMNS),random.randint(1,config.ROAD_COLUMNS//4))
        print(static_obstacle_pos)
        if(index % 2 == 0):
            image.fill((37, 255, 0,255))
        else:
            image.fill((0, 161, 43,255))
        super().__init__(index=index
                         ,surface=image
                         ,previeous_section = previeous_section
                         ,next_section = next_section
                         ,static_obstacles_pos = static_obstacle_pos)

    def update(self):
        pass

class DynamicSection(RoadSection):
    def __init__(self, index, surface, previeous_section, next_section, static_obstacles_pos):
        super().__init__(index, surface, previeous_section, next_section, static_obstacles_pos)