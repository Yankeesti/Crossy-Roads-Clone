import unittest
import pygame
import config
from map import RoadSectionManager
from map import RoadSectionManagerSingleton
from players import *

class test_RoadSectionManager(unittest.TestCase):
    def test_generate_sections(self):
        road_section_manager = RoadSectionManager()
        road_section_manager.generate_sections(2)
        self.assertEqual(len(road_section_manager.road_sections),3)
        #Test Indexes
        self.assertEqual(road_section_manager.road_sections[0].index,0)
        self.assertEqual(road_section_manager.road_sections[1].index,1)
        self.assertEqual(road_section_manager.road_sections[2].index,2)
        #Test correct Positioning of Sections
        self.assertEqual(road_section_manager.road_sections[0].rect.bottomleft,(0,0))
        self.assertEqual(road_section_manager.road_sections[1].rect.bottomleft,(0,-config.BLOCK_SIZE))
        self.assertEqual(road_section_manager.road_sections[2].rect.bottomleft,(0,-2*config.BLOCK_SIZE))
        #Test correct linking of Sections
        self.assertIs(road_section_manager.road_sections[0].next_section,road_section_manager.road_sections[1])
        self.assertIsNone(road_section_manager.road_sections[0].previous_section)
        self.assertIs(road_section_manager.road_sections[1].next_section,road_section_manager.road_sections[2])
        self.assertIs(road_section_manager.road_sections[1].previous_section,road_section_manager.road_sections[0])
        self.assertIs(road_section_manager.road_sections[2].previous_section,road_section_manager.road_sections[1])
        self.assertIsNone(road_section_manager.road_sections[2].next_section)

    def test_generate_sections_multipleBatches(self):
        road_section_manager = RoadSectionManager()
        road_section_manager.generate_sections(1)
        road_section_manager.generate_sections(2)
        self.assertEqual(len(road_section_manager.road_sections),4)
        #Test Indexes
        self.assertEqual(road_section_manager.road_sections[0].index,0)
        self.assertEqual(road_section_manager.road_sections[1].index,1)
        self.assertEqual(road_section_manager.road_sections[2].index,2)
        self.assertEqual(road_section_manager.road_sections[3].index,3)
        #Test correct Positioning of Sections
        self.assertEqual(road_section_manager.road_sections[0].rect.bottomleft,(0,0))
        self.assertEqual(road_section_manager.road_sections[1].rect.bottomleft,(0,-config.BLOCK_SIZE))
        self.assertEqual(road_section_manager.road_sections[2].rect.bottomleft,(0,-2*config.BLOCK_SIZE))
        self.assertEqual(road_section_manager.road_sections[3].rect.bottomleft,(0,-3*config.BLOCK_SIZE))

    def test_correct_road_section_linking(self):
        road_section_manager = RoadSectionManager()
        road_section_manager.generate_sections(1)
        road_section_manager.generate_sections(2)
        self.assertEqual(len(road_section_manager.road_sections),4)

        self.assertIs(road_section_manager.road_sections[0].next_section,road_section_manager.road_sections[1])
        self.assertIsNone(road_section_manager.road_sections[0].previous_section)
        self.assertIs(road_section_manager.road_sections[1].next_section,road_section_manager.road_sections[2])
        self.assertIs(road_section_manager.road_sections[1].previous_section,road_section_manager.road_sections[0])
        self.assertIs(road_section_manager.road_sections[2].previous_section,road_section_manager.road_sections[1])
        self.assertIs(road_section_manager.road_sections[2].next_section,road_section_manager.road_sections[3])
        self.assertIs(road_section_manager.road_sections[3].previous_section,road_section_manager.road_sections[2])
        self.assertIsNone(road_section_manager.road_sections[3].next_section)

class test_Player(unittest.TestCase):
    def test_correct_positioning(self):
        player = Player()
        self.assertEqual(player.rect.bottomleft,(5*100,0))

class test_HumanClient(unittest.TestCase):
    def test_construktor_works(self):
        player = HumanClient()
        self.assertEqual(player.rect.bottomleft,(5*100,0))

class test_PlayerManager(unittest.TestCase):
    def test_sort_players(self):
        players = [Player(),Player(),Player()]
        players[0].rect.bottomleft = (0,-100)
        players[1].rect.bottomleft = (-100,0)
        players[2].rect.bottomleft = (-30,-50)

        player_manager = PlayerManager(players.copy())
        self.assertEqual(3,len(player_manager.players))
        self.assertIs(player_manager.players[0],players[1])
        self.assertIs(player_manager.players[1],players[2])
        self.assertIs(player_manager.players[2],players[0])

        players[1].rect.bottomleft = (0,-300)
        player_manager.update()
        self.assertIs(player_manager.players[0],players[2])
        self.assertIs(player_manager.players[1],players[0])
        self.assertIs(player_manager.players[2],players[1])


if __name__ == '__main__':
    unittest.main()
    