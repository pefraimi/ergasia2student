import random
import networkx as nx

from player import Player


class PlayerC(Player):
    def initialize(self, game_info, id, my_type, player_seed) -> None:
        # This function is called once before the game starts.
        # Can be used for initializing auxiliary data of the player
        self.name = 'Omada 3'
        self.version = '0.1'

        self.game_info = game_info
        self.id = id
        self.my_type = my_type
        self.player_seed = player_seed
        self.rng = random.Random(self.player_seed)

    def move(self, node) -> int:
        # This function is called everytime player b has been selected for a move

        neighbors = self.game_info.g.neighbors(node)
        list_of_neighbors = list(neighbors)
        node_types = nx.get_node_attributes(self.game_info.g, "types")

        # Choose first foreign neighbor
        targets = [v for v in list_of_neighbors if node_types[v] != self.my_type]
        node = None
        if targets:
            node = targets[0]
        return node
