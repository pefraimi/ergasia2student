import collections
import copy
import random
import sys
import time
import traceback
from typing import List

import seaborn as sns  # for color palettes

import networkx as nx
import matplotlib.pyplot as plt

from game_info import Game_Info, game_move
from parameters import Parameters
from player_a import PlayerA
from player_b import PlayerB
from player_c import PlayerC
from player_d import PlayerD

from player_runtime import Player_Runtime


def draw_graph(g, node_pos, player_runtimes, counter):
    color_map = []
    node_types = nx.get_node_attributes(g, "types")
    for v in g.nodes:
        node_type = node_types[v]
        player_colors = sns.color_palette("tab10")
        color = player_colors[ord(node_type[0]) - 65]
        color_map.append(color)

    f = plt.figure(1)
    ax = f.add_subplot(1, 1, 1)
    for player_runtime in player_runtimes.values():
        id = player_runtime.id
        player_label = player_runtime.player_type
        num = counter[player_label]
        num_str = str(num).rjust(4)
        str_label = player_label + num_str
        str_name = '(' + player_runtime.player.name + ')'
        legend_label = str_label + ' ' + str_name.rjust(10)
        ax.plot([0], [0],
                color=player_colors[id],
                label=legend_label)

    nx.draw(g, pos=node_pos, node_color=color_map, with_labels=True)
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)
    plt.legend(loc='lower right')
    f.tight_layout()
    plt.show()


def get_random_node(g, rng) -> int:
    num_of_nodes = g.number_of_nodes()
    node = rng.randint(0, num_of_nodes - 1)
    return node


def run_moran_game(p):
    # Create random number generator
    rng = random.Random(p.seed)

    # Create random graph
    G = nx.barabasi_albert_graph(p.n, p.m, rng.randint(0, 10000000))

    # Player runtimes
    player_runtimes = dict()

    if p.num_of_players >= 1:
        player_runtimes[0] = Player_Runtime()
        player_runtimes[0].player_class = PlayerD
    if p.num_of_players >= 2:
        player_runtimes[1] = Player_Runtime()
        player_runtimes[1].player_class = PlayerA
    if p.num_of_players >= 3:
        player_runtimes[2] = Player_Runtime()
        player_runtimes[2].player_class = PlayerB
    if p.num_of_players >= 4:
        player_runtimes[3] = Player_Runtime()
        player_runtimes[3].player_class = PlayerC

    # Initial Assignment
    n = G.number_of_nodes()
    nodes_per_player = (int)(n / p.num_of_players)
    remainder = n % p.num_of_players

    number_of_nodes_of_player = dict()
    for i in range(p.num_of_players):
        if i == 0:
            # player 0 gets the remainder nodes
            number_of_nodes_of_player[i] = nodes_per_player + remainder
        else:
            number_of_nodes_of_player[i] = nodes_per_player

    node_type = dict()
    nodes_of_player = dict()
    unassigned_nodes = set(range(n))
    for i in range(p.num_of_players):
        num_of_unassigned_nodes = len(unassigned_nodes)
        nodes_i = rng.sample(list(unassigned_nodes), number_of_nodes_of_player[i])
        set_i = set(nodes_i)
        nodes_of_player[i] = set_i
        for v in set_i:
            node_type[v] = i
        unassigned_nodes = set(unassigned_nodes) - set_i

    if len(unassigned_nodes) > 0:
        print(f'ERROR: Some nodes are still unassigned: {len(unassigned_nodes)}')

    types = []
    nx.set_node_attributes(G, types, "types")
    for v in G.nodes:
        t = node_type[v]
        label = p.player_labels[t]
        nx.set_node_attributes(G, {v: label}, name="types")

    game_info = Game_Info(p.num_of_players, G, p.n, p.m, p.interactive)

    # initial assignment
    game_info.game_initial_assignment = copy.deepcopy(node_type)

    # prepare history data structure
    game_info.history = []

    # Create player objects
    players = dict()
    player_from_type = dict()
    for i, player_runtime in enumerate(player_runtimes.values()):
        # for player_type in player_classes:
        player_runtime.player = player_runtime.player_class()
        player_runtime.id = i
        player_runtime.player_type = p.player_labels[i]
        player_from_type[player_runtime.player_type] = i

    # Initialize players
    for player_runtime in player_runtimes.values():
        player_seed = rng.randint(0, 1000000)
        # player_runtime.player.initialize(G, p, player_runtime.id, player_runtime.player_type)
        player_runtime.player.initialize(game_info, player_runtime.id, player_runtime.player_type, player_seed)

    # types.append("A")
    if p.interactive:
        pos = nx.spring_layout(G)

    step = 0
    while True:
        random_node = get_random_node(G, rng)
        types = nx.get_node_attributes(G, "types")
        node_type = types[random_node][0]

        if node_type in p.player_labels.values():
            id = player_from_type[node_type]
            player_runtime = player_runtimes[id]
            move = player_runtime.player.move(random_node)
            if move not in list(G.neighbors(random_node)) and move != random_node and move is not None:
                raise Exception(f'Invalid move: Node {move} is not a neighbor of node {random_node} in step {step}')
        else:
            traceback.print_exc()
            sys.exit(f'Error: unexpected type: {type}')

        type_from = types.get(move, None)
        nx.set_node_attributes(G, {move: node_type}, name="types")
        game_info.history.append(game_move(step, node_type, random_node, move, type_from))
        counter, num_of_types, distinct_keys, distinct_counts = game_info.get_number_of_active_players()
        step += 1

        if p.interactive:
            draw_graph(G, pos, player_runtimes, counter)
            input("Press Enter to continue...")
            # time.sleep(0.1)

        if num_of_types == 1 or step >= 500:
            print(f'Maximum number of steps reached')
            print(f'Parameters {p}, Fixation {distinct_keys} {distinct_counts} after {step} number of steps!')
            if not p.interactive:
                pos = nx.spring_layout(G)
                draw_graph(G, pos, player_runtimes, counter)
            return list(distinct_keys)[0], step


# run_moran_game(Parameters(2, 20, 2, 123, True))
# run_moran_game(Parameters(2, 20, 2, 123, False))
# run_moran_game(Parameters(3, 20, 2, 123, False))
# run_moran_game(Parameters(3, 20, 2, 123, True))
# run_moran_game(Parameters(4, 20, 2, 123, True))

# run_moran_game(Parameters(2, 30, 2, 123, False))
# run_moran_game(Parameters(2, 50, 2, 123, False))
# run_moran_game(Parameters(2, 150, 2, 123, False))
# run_moran_game(Parameters(2, 200, 2, 123, False))
# run_moran_game(Parameters(2, 500, 2, 123, False))
# run_moran_game(Parameters(2, 1000, 2, 123, False))
# run_moran_game(Parameters(2, 1000, 4, 123, False))
# run_moran_game(Parameters(2, 1000, 5, 123, False))
# run_moran_game(Parameters(2, 1000, 5, 345, False))

run_moran_game(Parameters(num_of_players=4, n=20, m=2, seed=123, interactive=False))
# run_moran_game(Parameters(4, 20, 2, 123, True))
# run_moran_game(Parameters(4, 50, 2, 123, True))
# run_moran_game(Parameters(4, 100, 2, 123, True))
# run_moran_game(Parameters(4, 200, 2, 123, True))
# run_moran_game(Parameters(4, 500, 2, 123, True))
# run_moran_game(Parameters(4, 1000, 2, 123, True))