class Player:

    def __init__(self, name, passwd, games_played = 0, score = 0):
        self.id = 0
        self.name = name
        self.passwd = passwd
        self.games_played = games_played
        self.score = score

    def validation(self):
        # implement this method
        # return 0 for valid player
        # return 1 for invalid user name
        # return 2 for invalid password
        if len(self.name) < 4 or len(self.name) > 14:
            return 1
        if len(self.passwd) < 10 or len(self.passwd) > 20:
            return 2
        
        return 0

    def to_dict(self):
        return {"username": self.name, "password": self.passwd, "games_played": self.games_played, "total_score": self.score}
