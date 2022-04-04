
class Scores:
    def __init__(self):
        self.players = {}

    def add_players(self, players_list):
        points = 0
        self.players = self.players.fromkeys(players_list, points)

    def get_scores(self):
        sorted_dict = {k: v for k, v in sorted(self.players.items(), reverse=True, key=lambda item: item[1])}
        return sorted_dict

    def add_point(self, player_name):
        players_score = self.players.get(player_name)
        self.players.update({player_name: players_score + 1})