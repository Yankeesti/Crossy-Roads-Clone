from typing import Any
import pygame
import config
import map
import key_handler
import queue

class Player():
    pass

class PlayerManager(object):
    """"Manager for all players in the game. Singleton class. should only be created when RoadSectionManager was created."""
    _instance = None
    def __new__(cls,controllers = [key_handler.HumanController()]):
        if cls._instance is None:
            cls._instance = super(PlayerManager, cls).__new__(cls)
            cls._instance.players = []
            cls._instance.road_section_manager = map.RoadSectionManager()
            cls._instance.players = [Player(cls._instance.road_section_manager.road_sections[0],controller,cls._instance) for controller in controllers]
            cls._instance.min_player = max(cls._instance.players,key=lambda x: x.rect.y)
            cls._instance.max_player = min(cls._instance.players,key=lambda x: x.rect.y)
            cls._instance.dead_players = []
        return cls._instance
    
    def player_dead(self,player : Player):
        self.players.remove(player)
        self.dead_players.append(player)
    
    def update(self):
        for player in self.players:
            player.update()
        if(len(self.players) > 0):
            self.min_player = max(self.players,key=lambda x: x.rect[1])
            self.max_player = min(self.players,key=lambda x: x.rect[1])
            return True
        else:
            return False

class Player(pygame.sprite.Sprite):
    def __init__(self,currentSection,controller,manager :PlayerManager):
        super().__init__()
        self.image = config.PLAYER_IMAGE
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((config.ROAD_COLUMNS // 2)*config.BLOCK_SIZE,0 )
        self.sections = [currentSection]
        currentSection.add_player(self)
        self.controller = controller
        self.moves = queue.Queue()
        self.manager = manager
        self.killing_y_point = config.MAX_BLOCKS_BACK*config.BLOCK_SIZE
        self.score = 0

    def update(self):
        self.killing_y_point -= config.BLOCK_SIZE*config.BACK_BORDER_MOVEMENT_SPEED
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
                    self.moves.put(lambda: (
                            setattr(self, "sections", [self.sections[0].next_section]),
                            setattr(self, "score", self.score + 1),
                            setattr(self,"killing_y_point",self.sections[0].rect[1] +config.MAX_BLOCKS_BACK*config.BLOCK_SIZE)
                    ))

            elif action == "down":
                if self.check_move_possible((0,config.BLOCK_SIZE)):
                    self.sections = [self.sections[0].previous_section]
                    for i in range(1,config.PLAYER_SPEED):
                        self.moves.put(self.move_down)
                    self.move_down()
        if self.rect[1] >= self.killing_y_point:
            self.manager.player_dead(self)

    def __repr__(self) -> str:
        return f"Player at {self.rect[0]},{self.rect[1]}, score: {self.score}"

    def setManager(self,manager):
        self.manager = manager
    def move_left(self):
        self.rect[0]-= config.BLOCK_SIZE//config.PLAYER_SPEED
    def move_right(self):
        self.rect[0] += config.BLOCK_SIZE//config.PLAYER_SPEED
    def move_up(self):
        self.rect[1] -= config.BLOCK_SIZE//config.PLAYER_SPEED
        
    def move_down(self):
        self.rect[1] += config.BLOCK_SIZE//config.PLAYER_SPEED



    def check_move_possible(self,move):
        self.rect.move_ip(move)
        for section in self.sections:
            if pygame.sprite.spritecollide(self,section.blocked_columns,False):
                self.rect.move_ip((-move[0],-move[1]))
                return False
        self.rect.move_ip((-move[0],-move[1]))
        return True


