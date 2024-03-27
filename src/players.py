from typing import Any
import pygame
import config

class PlayerManager():
    def __init__(self,players = []):
        self.players = players
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
    def __init__(self,surface = config.PLAYER_IMAGE):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((config.ROAD_COLUMNS // 2+1)*config.BLOCK_SIZE,0 )
        
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

class HumanClient(Player):
    def __init__(self):
        image = config.PLAYER_IMAGE
        super().__init__(image)
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