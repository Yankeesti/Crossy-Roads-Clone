from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2

class RoadSectionType(Enum):
    STATIC = 1
    DYNAMIC = 2