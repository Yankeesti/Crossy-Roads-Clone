import pygame
from enums import RoadSectionType, Direction

BLOCK_SIZE = 90
ROAD_COLUMNS = 9
DISPLAYED_ROAD_SECTIONS = 10
UNSTEPABLEE_COLUMNS = 2  # unusable cullums at each side of the road
MAX_BLOCKS_BACK = 6
BACK_BORDER_MOVEMENT_SPEED = 0.0  # Blocks per Tick
PLAYER_SPEED = 15  # Ticks needed to move 1 Block


# Surfaces
TREE_IMAGE = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
CAR_IMAGE = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE * 1.8))
PLAYER_IMAGE = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
WINDOW_WIDTH = BLOCK_SIZE * (ROAD_COLUMNS + UNSTEPABLEE_COLUMNS * 2)
WINDOW_HEIGHT = BLOCK_SIZE * DISPLAYED_ROAD_SECTIONS

# RoadSection Configurations
ROAD_SECTION_GROUP_CONFIGURATION_MAX_CAR_SPEED = 0.15
ROAD_SECTION_GROUP_CONFIGURATION = [
    {
        "chance": 0,
        "road_sections": [
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 2,
                "car_speed": (
                    0.1,
                    0.5,
                ),  # (percentage of max speed, percentage of max speed)
                "car_direction": Direction.RIGHT,
                "car_offset_from_screen_edge": 0,
                "car_distance": (1.8, 5),
            },
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 3,
                "car_speed": (0.1, 0.8),
                "car_direction": Direction.RIGHT,
                "car_offset_from_screen_edge": 0,
                "car_distance": (1.8, 5),
            },
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 5,
                "car_speed": (0.2, 1),
                "car_direction": Direction.RIGHT,
                "car_offset_from_screen_edge": 0,
                "car_distance": (1.8, 5),
            },
        ],
    },
    {
        "chance": 1,
        "road_sections": [
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 1,
                "car_speed": (0.4, 1),
                "car_direction": [Direction.RIGHT, Direction.LEFT],
                "car_direction_probabilitys": [0.5,0.5],
                "car_offset_from_screen_edge": 0,
                "car_distance": (3, 5),
            },
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 2,
                "car_speed": (0.4, 0.6),
                "car_direction": [Direction.RIGHT, Direction.LEFT],
                "car_direction_probabilitys": [0.5,0.5],
                "car_offset_from_screen_edge": 0,
                "car_distance": (1.5, 5),
            },
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 4,
                "car_speed": (0.3, 0.8),
                "car_direction": [Direction.RIGHT, Direction.LEFT],
                "car_direction_probabilitys": [0.5,0.5],
                "car_offset_from_screen_edge": 0,
                "car_distance": (1.8, 2),
            },
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 1,
                "car_speed": (0.3, 0.8),
                "car_direction": [Direction.RIGHT, Direction.LEFT],
                "car_direction_probabilitys": [0.5,0.5],
                "car_offset_from_screen_edge": 0,
                "car_distance": (3, 5),
            },
        ],
    },
    {
        "chance": 0,
        "road_sections": [
            {
                "type": RoadSectionType.DYNAMIC,
                "car_number": 2,
                "car_speed": (0.3, 0.9),
                "car_direction": [Direction.RIGHT, Direction.LEFT],
                "car_direction_probabilitys": [0.5,0.5],
                "car_offset_from_screen_edge": 0,
                "car_distance": (1.8, 5),
            }
        ],
    },
]


ROAD_SECTION_GROUP_CONFIGURATION_WEIGHTS = [
    ROAD_SECTION_CONFIGURATION["chance"]
    for ROAD_SECTION_CONFIGURATION in ROAD_SECTION_GROUP_CONFIGURATION
]
