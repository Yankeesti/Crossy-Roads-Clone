from typing import Any
import pygame
import config
import map
import key_handler
import queue

class PlayerManager(object):
    """"Manager for all players in the game. Singleton class. should only be created when RoadSectionManager was created."""
    _instance = None
    def __new__(cls,controllers = [key_handler.HumanController()]):
        if cls._instance is None:
            cls._instance = super(PlayerManager, cls).__new__(cls)
            cls._instance.players = []
            cls._instance.road_section_manager = map.RoadSectionManager()
            cls._instance.players = [Player(cls._instance.road_section_manager.road_sections[0],controller) for controller in controllers]
            cls._instance.min_player = max(cls._instance.players,key=lambda x: x.rect.y)
            cls._instance.max_player = min(cls._instance.players,key=lambda x: x.rect.y)
        return cls._instance
    
    def remove_player(self,player):
        self.players.remove(player)
        self.remove(player)
    
    def update(self):
        for player in self.players:
            player.update()
        self.min_player = max(self.players,key=lambda x: x.rect[1])
        self.max_player = min(self.players,key=lambda x: x.rect[1])

class Player(pygame.sprite.Sprite):
    def __init__(self,currentSection,controller):
        super().__init__()
        self.image = config.PLAYER_IMAGE
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((config.ROAD_COLUMNS // 2)*config.BLOCK_SIZE,0 )
        self.sections = [currentSection]
        currentSection.add_player(self)
        self.controller = controller
        self.moves = queue.Queue()

    def update(self):
        if self.moves.empty() == False:
            self.moves.get()()
        else:
            action = self.controller.get_action()
            if action == "left":
                if self.check_move_possible((-config.BLOCK_SIZE,0)):
                    for i in range(1,config.PLAYER_SPEED):
                        self.moves.put(self.move_left)
                    self.move_left()

            elif action == "right":
                if self.check_move_possible((config.BLOCK_SIZE,0)):
                    for i in range(1,config.PLAYER_SPEED):
                        self.moves.put(self.move_right)
                    self.move_right()
            elif action == "up":
                if self.check_move_possible((0,-config.BLOCK_SIZE)):
                    for i in range(1,config.PLAYER_SPEED):
                        self.moves.put(self.move_up)
                    self.move_up()
                    self.moves.put(lambda : setattr(self,"sections",[self.sections[0].next_section]))
            elif action == "down":
                if self.check_move_possible((0,config.BLOCK_SIZE)):
                    self.sections = [self.sections[0].previous_section]
                    for i in range(1,config.PLAYER_SPEED):
                        self.moves.put(self.move_down)
                    self.move_down()

    def setManager(self,manager):
        self.manager = manager
    def move_left(self):
        self.rect[0]-= config.BLOCK_SIZE//config.PLAYER_SPEED
    def move_right(self):
        self.rect[0] += config.BLOCK_SIZE//config.PLAYER_SPEED
    def move_up(self):
        self.rect[1] -= config.BLOCK_SIZE//config.PLAYER_SPEED
        
    def move_down(self,ticks_left = 1):
        self.rect[1] += config.BLOCK_SIZE//config.PLAYER_SPEED

    def check_move_possible(self,move):
        self.rect.move_ip(move)
        for section in self.sections:
            if pygame.sprite.spritecollide(self,section.blocked_columns,False):
                self.rect.move_ip((-move[0],-move[1]))
                return False
        self.rect.move_ip((-move[0],-move[1]))
        return True


