from typing import Any
import pygame
import config

class PlayerManager():
    def __init__(self):
        self.players = []

    def add_player(self,player):
        self.players.append(player)
        self.add(player)

    def remove_player(self,player):
        self.players.remove(player)
        self.remove(player)

    def get_player(self):
        return self.players[0]

    def update(self):
        for player in self.players:
            player.update()

class Player(pygame.sprite.Sprite):
    def __init__(self,current_roads_section):
        super().__init__()
        self.image = config.PLAYER_IMAGE
        self.rect = self.image.get_rect()
        self.x_position = 5
        self.y_position = 0
        self.kill_time = config.MAX_TICKS_ON_ROAD_SECTION
        self.score = 0
        self.current_roads_section = current_roads_section
        self.current_roads_section.add(self)
        
    
    def move_left(self):
        self.x_position -= 1
    def move_right(self):
        self.x_position += 1
    def move_up(self):
        self.y_position += 1
    def move_down(self):
        self.y_position -= 1

class HumanClient(Player):
    def __init__(self,current_roads_section):
        super().__init__(current_roads_section)
        self.image.fill((255, 0, 0))

    def update(self):
        self.kill_time -= 1
        if self.kill_time <= 0:
            print("You died score: ",self.score)
            self.kill()
        self.key_press()
    
    def key_press(self):
       for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_a:
                   self.move_left()
               if event.key == pygame.K_d:
                   self.move_right()
               if event.key == pygame.K_w:
                   self.move_up()
               if event.key == pygame.K_s:
                   self.move_down()