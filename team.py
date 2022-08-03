class Team:
    def __init__(self) -> None:
        self.minimalTeamSize = 3
        self.normalTeamSize = 4
        self.maxTeamSize = 8
        self.defaultTeamSize = 6
        self.players = ["Player " + str(k) for k in range(1, self.defaultTeamSize + 1)]
        self.probabilityOfUseForPlayer = dict(zip(self.players, [0.5 for k in range(1, self.defaultTeamSize + 1)])) # self.probabilityOfUseForAllPlayers))
        self.probabilityOfUseForAllPlayers #= [0.5 for k in range(1, self.defaultTeamSize + 1)]
        self.probabilityOfUseForKPlayers = []
        self.distributionMoreOrEqualKPlayers = []
        self.expectedValue = 0
        self.probabilityForMinTeamSize = 0
        self.probabilityForNormalTeamSize = 0
        
        

    @property
    def probabilityOfUseForAllPlayers(self):
        return self.probabilityOfUseForPlayer.values()

if __name__ == "__main__":
  pass