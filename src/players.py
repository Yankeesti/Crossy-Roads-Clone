from typing import Any
import pygame
import config

class PlayerManager():
    def __init__(self,road_section_manager : map.RoadSectionManager,controllers):
        self.players = [Player(road_section_manager.road_sections[0],controller) for controller in controllers]
        self.sort_players()
    
    def sort_players(self):
        self.players.sort(key=lambda x: x.rect.y, reverse=True)
        
    def remove_player(self,player):
        self.players.remove(player)
        self.remove(player)

    def sort_players(self):
        self.players.sort(key=lambda x: x.rect.y, reverse=True)

    def update(self):
        for player in self.players:
            player.update()
        self.sort_players() 

class Player(pygame.sprite.Sprite):
    def __init__(self,currentSection:map.RoadSection,controller):
        super().__init__()
        self.image = config.PLAYER_IMAGE
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((config.ROAD_COLUMNS // 2+1)*config.BLOCK_SIZE,0 )
        self.sections = [currentSection]
        currentSection.add_player(self)
        self.controller = controller

    def update(self):
        action = self.controller.get_action()
        if action == "left":
            self.move_left()
        elif action == "right":
            self.move_right()
        elif action == "up":
            self.move_up()
        elif action == "down":
            self.move_down()

    def setManager(self,manager):
        self.manager = manager
    def move_left(self):
        self.x_position -= 1
    def move_right(self):
        self.x_position += 1
    def move_up(self):
        self.y_position += 1
    def move_down(self):
        self.y_position -= 1

class HumanController():
    def __init__(self):
        pass
    def get_action(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return "left"
                if event.key == pygame.K_d:
                    return "right"
                if event.key == pygame.K_w:
                    return "up"
                if event.key == pygame.K_s:
                    return "down"
        return "stay"
