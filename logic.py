from player import Player

class Logic:
    def __init__(self):
        self.active_tournament = False
        self.players: list[Player] = []

    def add_player(self, name: str) -> bool:
        if name in [player.name for player in self.players]:
            return False
        if name.upper() == 'BUY':
            return False
        player = Player(name)
        self.players.append(player)
        return True

    def setup_tournament(self) -> None:
        if len(self.players) % 2 != 0:
            self.players.append(Player('BUY'))
        self.round = 1
    
    def create_pairings(self) -> list[tuple[Player, Player]]:
        pairings = []
        pairing = []
        for player in self.players:
            pairing.append(player)
            if len(pairing) == 2:
                pairings.append(pairing)
                pairing = []
        return pairings


        ranked_players = sorted(self.players, key=lambda x: x.score)
        paired_players: list[Player] = []
        while len(ranked_players) != 0:
            player_1 = ranked_players.pop(0)
            for index, player_2 in enumerate(ranked_players):
                if player_2 not in player_1.opponents:
                    ranked_players.pop(index)
                    paired_players.append((player_1, player_2))
                    break