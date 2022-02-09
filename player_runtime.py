from player import Player


class Player_Runtime:
    player_class: Player
    player: Player
    id: int
    player_type: str

    # constructor
    def __init__(self):
        pass

    def __repr__(self):
        return "Player_Runtime()"

    def __str__(self):
        return f"player_class:{self.player_class}, player:{self.player}, id:{self.id}, player_type:{self.player_type}"