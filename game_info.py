import collections
from collections import Counter
from typing import List, Dict, TypedDict

import networkx as nx

game_move = collections.namedtuple('game_move', ('step', 'player_type', 'node_from', 'node_to'))

class Game_Info:
    g: nx.graph # The graph/network of the game
    num_of_players: int  # the number of distinct players
    n: int  # number of nodes
    m: int  # number of edges per new node (Barabasi-Albert)
    interactive: bool  # flag: interactive execution, else batch execution
    history: List[game_move]
    initial_assignment = Dict

    # constructor
    def __init__(self, num_of_players, g, n, m, interactive):
        self.num_of_players = num_of_players
        self.g = g
        self.n = n
        self.m = m
        self.interactive = interactive
        self.initial_assignment = None
        self.history: List[game_move] = None

    def __repr__(self):
        return "Game_Info()"

    def __str__(self):
        return f"num_of_players:{self.num_of_players}, g:{self.g}, n:{self.n}, m:{self.m}, player_seed:{self.player_seed}, interactive:{self.interactive}"

    def number_of_active_players(self) -> int:
        return 0

    def get_number_of_active_players(self):
        node_types = nx.get_node_attributes(self.g, "types")
        type_values = [k[0] for k in node_types.values()]
        counter = Counter(type_values)
        distinct_type_keys = counter.keys()
        distinct_type_counts = counter.values()

        # distinct_type_values = set(type_values)
        num_of_distinct_type_values = len(distinct_type_keys)
        return counter, num_of_distinct_type_values, distinct_type_keys, distinct_type_counts