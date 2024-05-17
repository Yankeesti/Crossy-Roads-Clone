from typing import Iterable
import pygame
from . import config
from . import map
from . import players


WIN = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Crossy Roads")

BORDER_SURFACE = pygame.Surface(
    (config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS, config.WINDOW_HEIGHT)
)
BORDER_SURFACE.fill((0, 0, 0))
BORDER_SURFACE.set_alpha(128)


class Camera:
    def __init__(self) -> None:
        super().__init__()
        self.road_section_manager = map.RoadSectionManager()
        self.player_manager = players.PlayerManager([])
        self.display_surface = pygame.display.get_surface()
        self.last_player_position = (1, 1)
        self.player_to_draw = self.player_manager.min_player
        self.y_offset = -config.WINDOW_HEIGHT

    def draw(self):  # draws the road sections and players
        self.display_surface.fill((0, 0, 0))
        self.y_offset = (
            self.player_to_draw.rect[1]
            - (config.DISPLAYED_ROAD_SECTIONS - 3) * config.BLOCK_SIZE
        )
        for section in self.player_to_draw.sections[0].get_sections_to_draw():
            section.draw(self.display_surface, self.y_offset)
        for player in self.player_manager.players:
            self.display_surface.blit(
                player.image, (player.rect[0], player.rect[1] - self.y_offset)
            )
        # drawn grey transparent rectangle to highlightws unplayable area
        self.display_surface.blit(BORDER_SURFACE, (0, 0))
        self.display_surface.blit(
            BORDER_SURFACE,
            (config.WINDOW_WIDTH - config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS, 0),
        )
        pygame.display.update()

    def set_player_to_draw(self, player: players.Player):
        self.player_to_draw = player

    def draw_operated_over_keyboard(self, input):
        self.display_surface.fill((0, 0, 0))
        if input == "up":
            self.y_offset -= config.BLOCK_SIZE / config.CAMERA_SPEED
        elif input == "down":
            self.y_offset += config.BLOCK_SIZE / config.CAMERA_SPEED

        road_sections = self.road_section_manager.get_sections_to_draw(self.y_offset)

        for section in road_sections:
            section.draw(self.display_surface, self.y_offset)
        for player in self.player_manager.players:
            self.display_surface.blit(
                player.image, (player.rect[0], player.rect[1] - self.y_offset)
            )

        self.display_surface.blit(BORDER_SURFACE, (0, 0))
        self.display_surface.blit(
            BORDER_SURFACE,
            (config.WINDOW_WIDTH - config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS, 0),
        )
        pygame.display.update()


class Game:
    def __init__(self, controllers):
        self.road_section_manager = map.RoadSectionManager()
        self.playerManager = players.PlayerManager(controllers=controllers)
        self.road_section_manager.generate_sections(config.DISPLAYED_ROAD_SECTIONS + 20)
        self.camera = Camera()
        for _ in range(300):
            self.road_section_manager.update()

    def update(self):
        if self.playerManager.update() == False:
            return False
        self.road_section_manager.update()

    def reset(self, controllers):
        map.RoadSectionManager._instance = None
        players.PlayerManager._instance = None
        self.__init__(controllers)


# if __name__ == "__main__":
#     game = Game(controllers= [key_handler.HumanController()])
#     camera = Camera()

#     clock = pygame.time.Clock()
#     camera.draw()
#     while True:
#         clock.tick(60)
#         if key_handler.handle_key_press() == False or game.update() == False:
#             break
#         camera.draw()
#     pygame.quit()
