import pygame
import neat
import game
import os
import itertools

directions = {0: "left", 1: "right", 2: "up", 3: "down", 4: "Stay"}
gameObj = None
clock = pygame.time.Clock()
camera_navigation_action = "stay"


def handle_key_press():

    global camera_navigation_action
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                camera_navigation_action = "up"
            if event.key == pygame.K_s:
                camera_navigation_action = "down"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                camera_navigation_action = "stay"
        


class genome_controller:
    def __init__(self, genome, config):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        if genome.fitness is None:
            genome.fitness = 1
        self.fitnesses = []

    def get_action(self, inputs):
        flat_list = list(
            itertools.chain.from_iterable(
                (i if isinstance(i, list) else [i] for i in inputs)
            )
        )
        flat_list = list(
            itertools.chain.from_iterable(
                (i if isinstance(i, tuple) else [i] for i in flat_list)
            )
        )
        output = self.net.activate(tuple(flat_list))
        return directions[output.index(max(output))]

    def setFitness(self, fitness):
        self.fitnesses.append(fitness)

    def calc_fitness(self):
        self.genome.fitness = sum(self.fitnesses) / len(self.fitnesses)
        self.fitnesses = []


def eval_genomes(genomes, config):
    pygame.init()
    global camera_navigation_action
    controllers = [genome_controller(genome, config) for genome_id, genome in genomes]
    global gameObj
    for i in range(10):
        if gameObj is None:
            gameObj = game.Game(controllers)
        else:
            gameObj.reset(controllers)
        camera = game.Camera()
        camera.draw_operated_over_keyboard(camera_navigation_action)
        while True:
            if gameObj.update() == False:
                break
            handle_key_press()
            camera.draw_operated_over_keyboard(camera_navigation_action)
    for controller in controllers:
        controller.calc_fitness()


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4")
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    p.run(eval_genomes, 1000)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    run_neat(config)
