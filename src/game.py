from typing import Iterable
import pygame
import key_handler
import config
import map
import players


WIN = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

road_section_manager = map.RoadSectionManager()



def draw_window():
    WIN.fill((255, 255, 255))
    road_section_manager.draw(WIN)
    pygame.display.update()

def main(controllers = [game_objects.HumanController()]):
    clock = pygame.time.Clock()
    draw_window()
    road_section_manager.generate_sections(config.DISPLAYED_ROAD_SECTIONS+5)
    while run:
        clock.tick(60)
        run = key_handler.handle_key_press()["run"]
        i+= 1
        if i% 10 == 0:
            player.remove(playerSprite)
        if(i % 20 == 0):
            player.add(playerSprite)
        draw_window()
    pygame.quit()

class Camera(pygame.sprite.Group):
    def __init__(self,road_section_manager:map.RoadSectionManager,player_manager:players.PlayerManager) -> None:
        super().__init__()

    def draw(self):
        pass

class Game:
    def __init__(self,controllers = [game_objects.HumanController()]):
        self.road_section_manager = map.RoadSectionManager()
        self.playerManager = players.PlayerManager(road_section_manager = road_section_manager,controllers= controllers)
        self.road_section_manager.generate_sections(config.DISPLAYED_ROAD_SECTIONS+3)

    def main(self):
        clock = pygame.time.Clock()
        draw_window()
        while run:
            clock.tick(60)
            run = key_handler.handle_key_press()["run"]
            self.playerManager.update()
            self.playerManager.update()
            draw_window()
        pygame.quit()

if __name__ == "__main__":
    main()