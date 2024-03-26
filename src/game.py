import pygame
import key_handler
import game_objects
import config
import map


WIN = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

playerSprite = game_objects.Player()

player = pygame.sprite.GroupSingle()
player.add(playerSprite)

road_section_manager = map_objekts.RoadSectionManager()
road_section_manager.generate_sections(config.DISPLAYED_ROAD_SECTIONS)

def draw_window():
    WIN.fill((255, 255, 255))
    road_section_manager.draw(WIN)
    player.draw(WIN)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    draw_window()
    clock = pygame.time.Clock()
    road_section_manager.update_shown_sections(3)
    i = 0
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


if __name__ == "__main__":
    main()