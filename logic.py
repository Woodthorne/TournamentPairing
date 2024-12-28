from player import Player

class Logic:
    def __init__(self):
        self.active_tournament = False
        self.players: list[Player] = []

    def add_player(self, name: str) -> None:
        player = Player(name)
        self.players.append(player)
    
    def create_pairings(self) -> list[tuple[Player, Player]]:
        ranked_players = sorted(self.players, key=lambda x: x.score)
        paired_players: list[Player] = []
        while len(ranked_players) != 0:
            player_1 = ranked_players.pop(0)
            for index, player_2 in enumerate(ranked_players):
                if player_2 not in player_1.opponents:
                    ranked_players.pop(index)
                    paired_players.append((player_1, player_2))
                    break