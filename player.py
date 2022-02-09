import abc

from networkx.classes import graph

from parameters import Parameters


class Player:
    # p: Parameters  # The parameters object of the game
    # g: graph  # The graph/network of the game
    name: str  # name of the number
    version: str  # name of the team (e.g. omada 01)
    id: int  # id of the player
    my_type: str  # type of the player
    player_seed: int  # seed of random number generator of the player (not the global seed of the game)

    # constructor
    def __init__(self):
        pass

    def __repr__(self):
        return f"Player()"

    def __str__(self):
        return f"Player({self.name}, {self.version}, {self.id}, {self.my_type})"

    @abc.abstractmethod
    def initialize(self, game_info, id, my_type, player_seed) -> None:
        pass

    @abc.abstractmethod
    def move(self, node) -> int:
        pass
