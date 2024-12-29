import random

from player import Player


class Logic:
    def __init__(self):
        self.active_tournament = False
        self.players: list[Player] = []
        self.round = 0
        self._buy = Player('BUY')

    def add_player(self, name: str) -> bool:
        if name in [player.name for player in self.players]:
            return False
        if name.upper() == 'BUY':
            return False
        player = Player(name)
        self.players.append(player)
        return True

    def next_round(self) -> None:
        if 2 ** self.round >= len(self.players):
            return False
        
        self.round += 1
        return True
    
    def create_pairings(self) -> list[tuple[Player, Player]]:
        pairings = []
        pairing = []
        for player in self.players:
            pairing.append(player)
            if len(pairing) == 2:
                pairings.append(pairing)
                pairing = []
        return pairings

    def true_create_pairings(self) -> list[tuple[Player, Player]]:
        ranked_players = self.get_rankings()
        pairings: list[Player] = []
        while len(ranked_players) != 0:
            pair = [ranked_players.pop(0)]

            for index, opponent in enumerate(ranked_players):
                if opponent not in pair[0].opponents:
                    ranked_players.pop(index)
                    pair.append(opponent)
                    break
            
            if len(pair) != 2:
                pair.append(self._buy)
            
            pairings.append(tuple(pair))
        return pairings
    
    def get_rankings(self) -> list[Player]:
        players = self.players.copy()
        if self.round == 1:
            random.shuffle(players)
        rankings: list[Player] = []
        scores = {player.score for player in players}
        for score in sorted(scores, reverse=True):
            rankings.extend([player for player 
                             in sorted(players, key=lambda p: p.opponents_score(), reverse=True)
                             if player.score == score])
        return rankings
    
    def end_round(self, results: dict[tuple[Player, Player], tuple[int, int]]) -> None:
        # print([p.score for p in self.players])
        # print([p.opponents_score() for p in self.players])
        
        for pair, wins in results.items():
            player_1, player_2 = pair
            wins_1, wins_2 = wins
            
            if wins_1 > wins_2:
                player_1.score += 3
            elif wins_1 < wins_2:
                player_2.score += 3
            else:
                player_1.score += 1
                player_2.score += 1
            
            player_1.opponents.append(player_2)
            player_2.opponents.append(player_1)
        
        # print([p.score for p in self.players])
        # print([p.opponents_score() for p in self.players])
