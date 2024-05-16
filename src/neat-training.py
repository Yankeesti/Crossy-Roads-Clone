import pygame
import neat
import game
import os
import itertools
import importlib

directions = {0: "left", 1: "right", 2: "up", 3: "down", 4: "Stay"}


class genome_controller:
    def __init__(self, genome, config):
        self.genome = genome
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        if genome.fitness is None:
            genome.fitness = 1

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
        print("Fitness:", fitness, "Genome ID:", self.genome.key)
        self.genome.fitness = fitness


def eval_genomes(genomes, config):
    importlib.reload(game)
    pygame.init()
    controllers = [genome_controller(genome, config) for genome_id, genome in genomes]
    gameObj = game.Game(controllers=controllers)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        if gameObj.update() == False:
            break
    pygame.quit()
    importlib.reload(game)


def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    p.run(eval_genomes, 50)


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
