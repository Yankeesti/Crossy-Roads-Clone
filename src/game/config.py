import pygame
from .enums import RoadSectionType, Direction

BLOCK_SIZE = 100
ROAD_COLUMNS = 9
DISPLAYED_ROAD_SECTIONS = 10
UNSTEPABLEE_COLUMNS = 2  # unusable cullums at each side of the road
BORDER_LEFT = BLOCK_SIZE * UNSTEPABLEE_COLUMNS
BORDER_RIGHT = BLOCK_SIZE * (ROAD_COLUMNS + UNSTEPABLEE_COLUMNS)
MAX_BLOCKS_BACK = 6
BACK_BORDER_MOVEMENT_SPEED = 0.05  # Blocks per Tick
PLAYER_SPEED = 10  # Ticks needed to move 1 Block


# Surfaces
TREE_IMAGE = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
CAR_IMAGE = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE * 1.8))
PLAYER_IMAGE = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
WINDOW_WIDTH = BLOCK_SIZE * (ROAD_COLUMNS + UNSTEPABLEE_COLUMNS * 2)
WINDOW_HEIGHT = BLOCK_SIZE * DISPLAYED_ROAD_SECTIONS

#Camer
CAMERA_SPEED = 10
# RoadSection Configurations
ROAD_SECTION_GROUP_CONFIGURATION_MAX_CAR_SPEED = 0.1
ROAD_SECTION_GROUP_CONFIGURATION = [
    {"chance": 0.2, "road_section_number": 1},
    {"chance": 0.2, "road_section_number": 2},
    {"chance": 0.2, "road_section_number": 3},
    {"chance": 0.2, "road_section_number": 4},
    {"chance": 0.2, "road_section_number": 5},
]


ROAD_SECTION_GROUP_CONFIGURATION_WEIGHTS = [
    ROAD_SECTION_CONFIGURATION["chance"]
    for ROAD_SECTION_CONFIGURATION in ROAD_SECTION_GROUP_CONFIGURATION
]
