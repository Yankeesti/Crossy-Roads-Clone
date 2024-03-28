from typing import Any
import pygame
import config

class RoadSectionManagerSingleton(object):
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RoadSectionManagerSingleton, cls).__new__(cls)
        return cls._instance
    def init_RoadSectionManager(self):
        section_neg_two = StaticRoadSection(-2)
        section_neg_one = StaticRoadSection (-1)
        section_neg_two.next_section = section_neg_one
        section_neg_one.previous_section = section_neg_two
        self.road_sections = [StaticRoadSection(0,previeous_section= section_neg_one)]
        section_neg_one.next_section = self.road_sections[0]

class RoadSectionManager():
    def __init__(self):
        super().__init__()
        #initialise negative Sections(Sections that can not be accesed by player but are displayed on lower Sections)
        section_neg_two = StaticRoadSection(-2)
        section_neg_one = StaticRoadSection (-1)
        section_neg_two.next_section = section_neg_one
        section_neg_one.previous_section = section_neg_two
        self.road_sections = [StaticRoadSection(0,previeous_section= section_neg_one)]
        section_neg_one.next_section = self.road_sections[0]
    def generate_sections(self,min_generated_sections = 1):
        for i in range(len(self.road_sections),len(self.road_sections)+min_generated_sections):
            self.road_sections.append(StaticRoadSection(i,self.road_sections[i-1]))
            self.road_sections[i-1].next_section = self.road_sections[i] 

class RoadSection(pygame.sprite.Sprite):
    def __init__(self,index,surface,previeous_section,next_section,road_section_manager):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.index = index
        self.rect.bottomleft = (0,-(index*config.BLOCK_SIZE))
        self.next_section = next_section
        self.previous_section = previeous_section
        self.players_on_section = []
        self.sections_to_draw = self.get_sections_to_draw
        
    
    def get_sections_to_draw(self):
        pass

    def add_player(self,player):
        self.players_on_section.append(player)
        
    def remove_player(self,player):
        self.players_on_section.remove(player)

    def update(self):
        # Add any update logic for the road section here
        pass



class StaticRoadSection(RoadSection):
    def __init__(self,index,player_manager,previeous_section = None,next_section = None):
        image = pygame.Surface((config.WINDOW_WIDTH, config.BLOCK_SIZE),pygame.SRCALPHA)
        if(index % 2 == 0):
            image.fill((37, 255, 0,255))
        else:
            image.fill((0, 161, 43,255))
        super().__init__(index=index
                         ,surface=image
                         ,player_manager= player_manager
                         ,previeous_section = previeous_section
                         ,next_section = next_section)

    def update(self):
        pass
