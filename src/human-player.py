import game
import itertools
import pygame

navigation_action = "stay"


def handle_key_press():
    global navigation_action
    out_put = {"run": True}
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out_put["run"] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                navigation_action = "left"
            if event.key == pygame.K_d:
                navigation_action = "right"
            if event.key == pygame.K_w:
                navigation_action = "up"
            if event.key == pygame.K_s:
                navigation_action = "down"
    return out_put


class HumanController:
    def get_action(self, input):
        global navigation_action
        out_put = navigation_action
        navigation_action = "stay"
        flat_list = list(
            itertools.chain.from_iterable(
                (i if isinstance(i, list) else [i] for i in input)
            )
        )
        flat_list = list(
            itertools.chain.from_iterable(
                (i if isinstance(i, tuple) else [i] for i in flat_list)
            )
        )
        print(input)
        return out_put

    def setFitness(self, fitness):
        print(fitness)


controller = HumanController()
gameClass = game.Game(controllers=[controller])
camera = game.Camera()

clock = pygame.time.Clock()
camera.draw()
while True:
    clock.tick(60)
    if handle_key_press() == False or gameClass.update() == False:
        break
    camera.draw()

gameClass.reset(controllers=[controller])
camera = game.Camera()
camera.set_player_to_draw(gameClass.playerManager.players[0])
camera.draw()
while True:
    clock.tick(60)
    if handle_key_press() == False or gameClass.update() == False:
        break
    camera.draw()
