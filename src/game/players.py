from typing import Any
import pygame
from . import config
from . import map
from . import key_handler
import queue


class Player:
    pass


class PlayerManager(object):
    """ "Manager for all players in the game. Singleton class. should only be created when RoadSectionManager was created."""

    _instance = None

    def __new__(cls, controllers=[key_handler.HumanController()]):
        if cls._instance is None:
            cls._instance = super(PlayerManager, cls).__new__(cls)
            cls._instance.players = []
            cls._instance.road_section_manager = map.RoadSectionManager()
            cls._instance.players = [
                Player(
                    cls._instance.road_section_manager.road_sections[0],
                    controller,
                    cls._instance,
                )
                for controller in controllers
            ]
            cls._instance.min_player = max(
                cls._instance.players, key=lambda x: x.rect.y
            )
            cls._instance.max_player = min(
                cls._instance.players, key=lambda x: x.rect.y
            )
            cls._instance.dead_players = []
        return cls._instance

    def player_dead(self, player: Player):
        if player in self.players:
            self.players.remove(player)
            self.dead_players.append(player)

    def update(self):
        if len(self.players) > 0:
            self.min_player = max(self.players, key=lambda x: x.rect[1])
            self.max_player = min(self.players, key=lambda x: x.rect[1])
            for player in self.players:
                player.update()
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):
    def __init__(
        self, currentSection: map.RoadSection, controller, manager: PlayerManager
    ):
        super().__init__()
        self.image = config.PLAYER_IMAGE
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((config.ROAD_COLUMNS // 2) * config.BLOCK_SIZE, 0)
        self.sections = [currentSection]
        currentSection.add_player(self)
        self.controller = controller
        self.moves = queue.Queue()
        self.manager = manager
        self.killing_y_point = config.MAX_BLOCKS_BACK * config.BLOCK_SIZE
        self.highest_section = currentSection
        self.dead = False
        self.moves = {"left": 0, "right": 0, "up": 0, "down": 0, "stay": 0}

    def kill(self):
        if self.dead == False:
            self.controller.setFitness(self.highest_section.index + 1)
            self.manager.player_dead(self)
            super().kill()
            self.dead = True

    def update(self):
        self.killing_y_point -= config.BLOCK_SIZE * config.BACK_BORDER_MOVEMENT_SPEED
        if self.moves.empty() == False:
            self.moves.get()()
        else:
            action = self.controller.get_action(self.calc_input())
            if action == "left":
                self.init_move_left()
                self.moves["left"] += 1
            elif action == "right":
                self.init_move_right()
                self.moves["right"] += 1
            elif action == "up":
                self.init_move_up()
                self.moves["up"] += 1
            elif action == "down":
                self.init_move_down()
                self.moves["down"] += 1
            else:
                self.moves["stay"] += 1
        if self.rect[1] >= self.killing_y_point:
            self.kill()

    def calc_input(self):
        input = []
        input.append((self.killing_y_point - self.rect[1]))  # Distance to death
        input.append(-(self.rect.left - config.BORDER_LEFT))  # space to left border
        input.append(-(self.rect.right - config.BORDER_RIGHT))  # space to right border
        input.append(
            self.sections[0].previous_section.get_obstacal_positions_relative_to_player(
                self
            )
        )  # section before section
        input.append(
            self.sections[0].get_obstacal_positions_relative_to_player(self)
        )  # current section
        input.append(
            self.sections[0].next_section.get_obstacal_positions_relative_to_player(
                self
            )
        )  # section after section
        input.append(
            self.sections[
                0
            ].next_section.next_section.get_obstacal_positions_relative_to_player(self)
        )  # section after section
        input.append(
            self.sections[
                0
            ].next_section.next_section.next_section.get_obstacal_positions_relative_to_player(
                self
            )
        )  # section after section

        return input

    def __repr__(self) -> str:
        return f"Player at {self.rect[0]},{self.rect[1]}, score: {self.highest_section.index}, current section: {self.sections[0]}"

    def init_move_left(self):
        if (
            self.rect.bottomleft[0] - config.BLOCK_SIZE
            >= config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS
            # Check for Obstacles and left Border
            and self.check_move_possible(self.sections, (-config.BLOCK_SIZE, 0))
        ):
            for i in range(1, config.PLAYER_SPEED):
                self.moves.put(self.move_left)
            self.move_left()

    def move_left(self):
        self.rect[0] -= config.BLOCK_SIZE // config.PLAYER_SPEED

    def init_move_right(self):
        if self.rect.bottomright[
            0
        ] + config.BLOCK_SIZE <= config.WINDOW_WIDTH - config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS and self.check_move_possible(
            self.sections, (config.BLOCK_SIZE, 0)
        ):
            for i in range(1, config.PLAYER_SPEED):
                self.moves.put(self.move_right)
            self.move_right()

    def move_right(self):
        # print("right")
        self.rect[0] += config.BLOCK_SIZE // config.PLAYER_SPEED

    def init_move_up(self):
        if self.check_move_possible(
            [self.sections[0].next_section], (0, -config.BLOCK_SIZE)
        ):
            self.sections.insert(1, self.sections[0].next_section)
            self.sections[1].add_player(self)
            for _ in range(1, config.PLAYER_SPEED):
                self.moves.put(self.move_up)
            self.move_up()
            self.moves.put(
                lambda: (
                    self.update_highest_section(),
                    self.sections[0].remove_player(self),
                    setattr(self, "sections", [self.sections[1]]),
                    self.update_killing_y_point(),
                )
            )

    def update_killing_y_point(self):
        new_killing_y_point = (
            self.sections[0].rect.bottomleft[1]
            + config.MAX_BLOCKS_BACK * config.BLOCK_SIZE
        )
        if self.killing_y_point > new_killing_y_point:
            self.killing_y_point = new_killing_y_point

    def move_up(self):
        # print("up")
        self.rect[1] -= config.BLOCK_SIZE // config.PLAYER_SPEED

    def init_move_down(self):
        if self.rect[1] < -config.BLOCK_SIZE and self.check_move_possible(
            [self.sections[0].previous_section], (0, config.BLOCK_SIZE)
        ):
            self.sections.insert(0, self.sections[0].previous_section)
            self.sections[0].add_player(self)
            for _ in range(1, config.PLAYER_SPEED):
                self.moves.put(self.move_down)
            self.move_down()
            self.moves.put(
                lambda: (
                    self.sections[1].remove_player(self),
                    setattr(self, "sections", [self.sections[0]]),
                )
            )

    def move_down(self):
        self.rect[1] += config.BLOCK_SIZE // config.PLAYER_SPEED

    def check_move_possible(self, sections, move):
        for section in sections:
            if section.move_possible(self, move) == False:
                return False
        return True

    def update_highest_section(self):
        highest_current_section = max(self.sections, key=lambda x: x.index)
        if highest_current_section.index > self.highest_section.index:
            self.highest_section = highest_current_section
