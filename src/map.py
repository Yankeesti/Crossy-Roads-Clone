from typing import Any
import pygame
import config



class RoadSectionManager():
    def __init__(self):
        super().__init__()
        self.road_sections = [StaticRoadSection(0)]

    def generate_sections(self,min_generated_sections = 1):
        for i in range(len(self.road_sections),len(self.road_sections)+min_generated_sections):
            self.road_sections.append(StaticRoadSection(i,self.road_sections[i-1]))
            self.road_sections[i-1].next_section = self.road_sections[i]

    

class RoadSection(pygame.sprite.Sprite):
    def __init__(self,index,surface,previeous_section,next_section):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.index = index
        self.rect.bottomleft = (0,-(index*config.BLOCK_SIZE))
        self.next_section = next_section
        self.previous_section = previeous_section
        

    def update(self):
        # Add any update logic for the road section here
        pass



class StaticRoadSection(RoadSection):
    def __init__(self,index,previeous_section = None,next_section = None):
        image = pygame.Surface((config.WINDOW_WIDTH, config.BLOCK_SIZE),pygame.SRCALPHA)
        if(index % 2 == 0):
            image.fill((37, 255, 0,255))
        else:
            image.fill((0, 161, 43,255))
        super().__init__(index,image,previeous_section,next_section)

    def update(self):
        pass