from typing import Iterable
import pygame
import key_handler
import config
import map
import players


WIN = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Crossy Roads")

BORDER_SURFACE = pygame.Surface((config.BLOCK_SIZE*config.UNSTEPABLEE_COLUMNS, config.WINDOW_HEIGHT))
BORDER_SURFACE.fill((0,0,0))
BORDER_SURFACE.set_alpha(128)

class Camera():
    def __init__(self) -> None:
        super().__init__()
        self.road_section_manager = map.RoadSectionManager()
        self.player_manager = players.PlayerManager([])
        self.display_surface = pygame.display.get_surface()

    def draw(self,player:players.Player):
        y_offset = player.rect[1] - (config.DISPLAYED_ROAD_SECTIONS-3)*config.BLOCK_SIZE
        for section in player.sections[0].get_sections_to_draw():
            if section is None:
                for i,section in enumerate(player.sections[0].get_sections_to_draw()):
                    if section is None:
                        print(i," : None")
                    else:
                        print(i," : ",section.index)
            self.display_surface.blit(section.image,(0,section.rect[1] - y_offset))
        for player in self.player_manager.players:
            self.display_surface.blit(player.image,(player.rect[0],player.rect[1] - y_offset))
        #drawn grey transparent rectangle to highlight unplayable area
        self.display_surface.blit(BORDER_SURFACE,(0,0))
        self.display_surface.blit(BORDER_SURFACE,(config.WINDOW_WIDTH - config.BLOCK_SIZE*config.UNSTEPABLEE_COLUMNS,0))
        pygame.display.update()
        

class Game:
    def __init__(self,controllers=[key_handler.HumanController()]):
        self.road_section_manager = map.RoadSectionManager()
        self.playerManager = players.PlayerManager(controllers= controllers)
        self.road_section_manager.generate_sections(config.DISPLAYED_ROAD_SECTIONS+3)
        self.camera = Camera()

    def main(self):
        clock = pygame.time.Clock()
        self.camera.draw(self.playerManager.min_player)
        run = True
        while run:
            clock.tick(60)
            run = key_handler.handle_key_press()["run"]
            self.playerManager.update()
            self.road_section_manager.update()
            self.camera.draw(self.playerManager.min_player)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.main()