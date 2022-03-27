class Player:
    def __init__(self, playerID, player_name):
        self.player_name = player_name
        self.playerID = playerID
        self.nonerisa = 0
        self.erisa = 0
        self.cafeteria = 0
        self.operating = 0

        # This will be used in the normal gameplay for finding the winner
        self.total_off = 0
        # PlayerID of 0 will be passed through for the winning numbers