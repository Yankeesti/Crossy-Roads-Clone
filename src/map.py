from typing import Any
import pygame
import config

class RoadSectionManager(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.road_sections = []

    def generate_sections(self,min_generated_sections = 1):
        for i in range(len(self.road_sections),len(self.road_sections)+min_generated_sections):
            self.road_sections.append(StaticRoadSection(i))

    def update_shown_sections(self,targeted_section_index):
        highest_shown_section_index = targeted_section_index + config.DISPLAYED_ROAD_SECTIONS -3
        self.empty()
        if(len(self.road_sections) < targeted_section_index + config.DISPLAYED_ROAD_SECTIONS -2):
            self.generate_sections(targeted_section_index + config.DISPLAYED_ROAD_SECTIONS -2 - len(self.road_sections))
        for loop_index,section_index in enumerate(range(highest_shown_section_index,highest_shown_section_index - config.DISPLAYED_ROAD_SECTIONS,-1)):
            print("y_position: ",config.BLOCK_SIZE * loop_index ,"section_index: ",section_index)
            self.road_sections[section_index].set_y_position(config.BLOCK_SIZE * loop_index )
            self.add(self.road_sections[section_index])

class RoadSection(pygame.sprite.Sprite):
    def __init__(self,index,surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.index = index
        self.y_position = 0
        self.rect.y = self.y_position
        self.rect.x = 0
        self.players = pygame.sprite.Group()

    def update(self):
        # Add any update logic for the road section here
        pass

    def set_y_position(self,y_position):
        self.y_position = y_position
        self.rect.y = y_position

    def add_player(self,player):
        self.players.add(player)
    
    def remove_player(self,player):
        self.players.remove(player)



class StaticRoadSection(RoadSection):
    def __init__(self,index):
        image = pygame.Surface((config.WINDOW_WIDTH, config.BLOCK_SIZE),pygame.SRCALPHA)
        if(index % 2 == 0):
            image.fill((37, 255, 0,255))
        else:
            image.fill((0, 161, 43,255))
        super().__init__(index,image)

    def update(self):
        pass