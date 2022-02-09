import seaborn as sns  # for color palettes

class Parameters:
    num_of_players: int  # the number of distinct players
    n: int  # number of nodes
    m: int  # number of edges per new node (Barabasi-Albert)
    seed: int  # seed of random number generator
    interactive: bool  # flag: interactive execution, else batch execution

    # constructor
    def __init__(self, num_of_players, n, m, seed, interactive):
        self.num_of_players = num_of_players
        self.n = n
        self.m = m
        self.seed = seed
        self.interactive = interactive

        self.player_ids = range(self.num_of_players)
        self.player_labels = {id: chr(65 + id) for id in self.player_ids}
        self.player_colors = sns.color_palette("tab10")

    def __repr__(self):
        return "Parameters()"

    def __str__(self):
        return f"num_of_players:{self.num_of_players}, n:{self.n}, m:{self.m}, seed:{self.seed}, interactive:{self.interactive}"
