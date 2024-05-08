import unittest
import config
from map import RoadSectionManager
from players import *
from key_handler import HumanController
from obstacles import Obstacle

# class test_Player(unittest.TestCase):
#     def test_correct_positioning(self):
#         player = Player(map.StaticRoadSection(0),map.StaticRoadSection(1),None)
#         self.assertEqual(player.rect.bottomleft,(5*100,0))

# class test_PlayerManager(unittest.TestCase):
#     def test_sort_players(self):
#         players = [Player(),Player(),Player()]
#         players[0].rect.bottomleft = (0,-100)
#         players[1].rect.bottomleft = (-100,0)
#         players[2].rect.bottomleft = (-30,-50)

#         player_manager = PlayerManager(players.copy())
#         self.assertEqual(3,len(player_manager.players))
#         self.assertIs(player_manager.players[0],players[1])
#         self.assertIs(player_manager.players[1],players[2])
#         self.assertIs(player_manager.players[2],players[0])

#         players[1].rect.bottomleft = (0,-300)
#         player_manager.update()
#         self.assertIs(player_manager.players[0],players[2])
#         self.assertIs(player_manager.players[1],players[0])
#         self.assertIs(player_manager.players[2],players[1])


def reset_singletons():
    RoadSectionManager._instance = None
    PlayerManager._instance = None


class test_RoadSectionManager(unittest.TestCase):
    def setUp(self) -> None:
        reset_singletons()

    def test_singleton(self):
        road_section_manager = RoadSectionManager()
        road_section_manager2 = RoadSectionManager()
        self.assertIs(road_section_manager, road_section_manager2)

    def test_constructor(self):
        road_section_manager = RoadSectionManager()
        self.assertEqual(len(road_section_manager.road_sections), 1)
        self.assertEqual(road_section_manager.road_sections[0].index, 0)
        self.assertIsNotNone(
            road_section_manager.road_sections[0].previous_section)
        self.assertIsNotNone(
            road_section_manager.road_sections[0].previous_section.previous_section)
        self.assertIs(
            road_section_manager.road_sections[0].previous_section.next_section, road_section_manager.road_sections[0])
        self.assertIs(road_section_manager.road_sections[0].previous_section.previous_section.next_section,
                      road_section_manager.road_sections[0].previous_section)

    def test_generate_sections(self):
        road_section_manager = RoadSectionManager()
        road_section_manager.generate_sections(2)
        self.assertEqual(len(road_section_manager.road_sections), 3)
        # Test Indexes
        self.assertEqual(road_section_manager.road_sections[0].index, 0)
        self.assertEqual(road_section_manager.road_sections[1].index, 1)
        self.assertEqual(road_section_manager.road_sections[2].index, 2)
        # Test correct Positioning of Sections
        self.assertEqual(
            road_section_manager.road_sections[0].rect.bottomleft, (0, 0))
        self.assertEqual(
            road_section_manager.road_sections[1].rect.bottomleft, (0, -config.BLOCK_SIZE))
        self.assertEqual(
            road_section_manager.road_sections[2].rect.bottomleft, (0, -2*config.BLOCK_SIZE))
        # Test correct linking of Sections

    def test_generate_sections_multipleBatches(self):
        road_section_manager = RoadSectionManager()
        road_section_manager.generate_sections(1)
        road_section_manager.generate_sections(2)
        self.assertEqual(len(road_section_manager.road_sections), 4)
        # Test Indexes
        self.assertEqual(road_section_manager.road_sections[0].index, 0)
        self.assertEqual(road_section_manager.road_sections[1].index, 1)
        self.assertEqual(road_section_manager.road_sections[2].index, 2)
        self.assertEqual(road_section_manager.road_sections[3].index, 3)
        # Test correct Positioning of Sections
        self.assertEqual(
            road_section_manager.road_sections[0].rect.bottomleft, (0, 0))
        self.assertEqual(
            road_section_manager.road_sections[1].rect.bottomleft, (0, -config.BLOCK_SIZE))
        self.assertEqual(
            road_section_manager.road_sections[2].rect.bottomleft, (0, -2*config.BLOCK_SIZE))
        self.assertEqual(
            road_section_manager.road_sections[3].rect.bottomleft, (0, -3*config.BLOCK_SIZE))

    def test_correct_road_section_linking(self):
        road_section_manager = RoadSectionManager()
        road_section_manager.generate_sections(1)
        road_section_manager.generate_sections(2)

        road_section_neg_one = road_section_manager.road_sections[0].previous_section
        self.assertIsNotNone(road_section_neg_one)
        road_section_neg_two = road_section_neg_one.previous_section
        self.assertIsNotNone(road_section_neg_two)

        self.assertEqual(len(road_section_manager.road_sections), 4)

        self.assertIsNone(road_section_neg_two.previous_section)
        self.assertIs(road_section_neg_two.next_section, road_section_neg_one)
        self.assertIs(road_section_neg_one.previous_section,
                      road_section_neg_two)
        self.assertIs(road_section_neg_one.next_section,
                      road_section_manager.road_sections[0])
        self.assertIs(
            road_section_manager.road_sections[0].previous_section, road_section_neg_one)
        self.assertIs(
            road_section_manager.road_sections[0].next_section, road_section_manager.road_sections[1])

        self.assertIs(
            road_section_manager.road_sections[1].previous_section, road_section_manager.road_sections[0])
        self.assertIs(
            road_section_manager.road_sections[1].next_section, road_section_manager.road_sections[2])

        self.assertIs(
            road_section_manager.road_sections[2].previous_section, road_section_manager.road_sections[1])
        self.assertIs(
            road_section_manager.road_sections[2].next_section, road_section_manager.road_sections[3])
        self.assertIs(
            road_section_manager.road_sections[3].previous_section, road_section_manager.road_sections[2])
        self.assertIsNone(road_section_manager.road_sections[3].next_section)


class test_RoadSection(unittest.TestCase):
    def setUp(self) -> None:
        reset_singletons()

    def test_get_section_to_draw_from_zero(self):
        config.DISPLAYED_ROAD_SECTIONS = 5
        roadSectionManager = RoadSectionManager()
        road_section = roadSectionManager.road_sections[0]
        road_sections_to_draw = road_section.get_sections_to_draw()
        self.assertEqual(len(road_sections_to_draw), 6)
        self.assertEqual(road_sections_to_draw[0].index, -2)
        self.assertEqual(road_sections_to_draw[1].index, -1)
        self.assertEqual(road_sections_to_draw[2].index, 0)
        self.assertEqual(road_sections_to_draw[3].index, 1)
        self.assertEqual(road_sections_to_draw[4].index, 2)
        self.assertEqual(road_sections_to_draw[5].index, 3)

    def test_get_section_to_draw_from_one(self):
        config.DISPLAYED_ROAD_SECTIONS = 5
        roadSectionManager = RoadSectionManager()
        roadSectionManager.generate_sections(1)
        road_section = roadSectionManager.road_sections[1]
        road_sections_to_draw = road_section.get_sections_to_draw()
        self.assertEqual(len(road_sections_to_draw), 6)
        self.assertEqual(road_sections_to_draw[0].index, -1)
        self.assertEqual(road_sections_to_draw[1].index, 0)
        self.assertEqual(road_sections_to_draw[2].index, 1)
        self.assertEqual(road_sections_to_draw[3].index, 2)
        self.assertEqual(road_sections_to_draw[4].index, 3)
        self.assertEqual(road_sections_to_draw[5].index, 4)

    def test_get_section_to_draw_when_jump_back(self):
        config.DISPLAYED_ROAD_SECTIONS = 5
        roadSectionManager = RoadSectionManager()
        roadSectionManager.generate_sections(1)
        road_section = roadSectionManager.road_sections[1]
        road_sections_to_draw = road_section.get_sections_to_draw()
        self.assertEqual(len(road_sections_to_draw), 6)
        self.assertEqual(road_sections_to_draw[0].index, -1)
        self.assertEqual(road_sections_to_draw[1].index, 0)
        self.assertEqual(road_sections_to_draw[2].index, 1)
        self.assertEqual(road_sections_to_draw[3].index, 2)
        self.assertEqual(road_sections_to_draw[4].index, 3)
        self.assertEqual(road_sections_to_draw[5].index, 4)

        road_section = road_section.previous_section
        road_sections_to_draw = road_section.get_sections_to_draw()
        self.assertEqual(len(road_sections_to_draw), 6)
        self.assertEqual(road_sections_to_draw[0].index, -2)
        self.assertEqual(road_sections_to_draw[1].index, -1)
        self.assertEqual(road_sections_to_draw[2].index, 0)
        self.assertEqual(road_sections_to_draw[3].index, 1)
        self.assertEqual(road_sections_to_draw[4].index, 2)
        self.assertEqual(road_sections_to_draw[5].index, 3)


class test_PlayerManager(unittest.TestCase):
    def setUp(self) -> None:
        reset_singletons()

    def test_singleton(self):
        player_manager = PlayerManager()
        player_manager2 = PlayerManager()
        self.assertIs(player_manager, player_manager2)

    def test_constructor(self):
        player_manager = PlayerManager()
        self.assertEqual(len(player_manager.players), 1)
        self.assertEqual(player_manager.min_player, player_manager.players[0])
        self.assertEqual(player_manager.max_player, player_manager.players[0])

    def test_min_and_max(self):
        player_manager = PlayerManager(
            [HumanController(), HumanController(), HumanController()])
        player_manager.players[0].rect = (0, -100)
        player_manager.players[1].rect = (-100, 0)
        player_manager.players[2].rect = (-30, -50)
        player_manager.update()
        self.assertIs(player_manager.min_player, player_manager.players[1])
        self.assertIs(player_manager.max_player, player_manager.players[0])

        player_manager.players[1].rect = (0, -300)
        player_manager.update()
        self.assertIs(player_manager.min_player, player_manager.players[2])
        self.assertIs(player_manager.max_player, player_manager.players[1])


class test_Obstacle(unittest.TestCase):
    def setUp(self) -> None:
        reset_singletons()

    def test_correct_positioning(self):
        config.BLOCK_SIZE = 10
        sectionManager = RoadSectionManager()
        road_section = sectionManager.road_sections[0]
        obstacle = Obstacle(pygame.Surface(
            (config.WINDOW_WIDTH, config.BLOCK_SIZE), pygame.SRCALPHA), 95)
        obstacle.adjust_y(road_section)
        self.assertEqual(obstacle.rect.midleft, (95, -5))

        sectionManager.generate_sections(1)
        road_section = sectionManager.road_sections[1]
        obstacle.adjust_y(road_section)
        self.assertEqual(obstacle.rect.midleft, (95, -15))


if __name__ == '__main__':
    unittest.main()
