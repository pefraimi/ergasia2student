import seaborn as sns  # for color palettes


class Parameters:
    num_of_players: int  # the number of distinct players
    n: int  # number of nodes
    m: int  # number of edges per new node (Barabasi-Albert)
    seed: int  # seed of random number generator
    steps: int  # maximum number of steps
    assignment: list  # the assignment of strategies to the players (or else, the order of the players)
    interactive: bool  # flag: interactive execution, else batch execution

    # constructor
    def __init__(self, num_of_players, n, m, steps, seed, assignment, interactive):
        self.num_of_players = num_of_players
        self.n = n
        self.m = m
        self.steps = steps
        self.seed = seed
        self.interactive = interactive
        self.assignment = assignment

        self.player_ids = range(self.num_of_players)
        self.player_labels = {player_id: chr(65 + player_id) for player_id in self.player_ids}
        self.player_colors = sns.color_palette("tab10")

    def __repr__(self):
        return "Parameters()"

    def __str__(self):
        return f"num_of_players:{self.num_of_players}, n:{self.n}, m:{self.m}, assignment:{self.assignment}, seed:{self.seed}, " \
               f"interactive:{self.interactive} "
