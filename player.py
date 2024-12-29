class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.opponents: list[Player] = []
    
    def opponents_score(self) -> int:
        return sum([player.score for player in self.opponents])
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f'Player({self.name})'