from math import log

class Team:
	
	def __init__(self, name, startingElo):
		self.name = name
		self.elo = startingElo
		self.peakElo = (startingElo, "Start")
		self.biggestJump = (0, startingElo, "Start")
		self.biggestFall = (0, startingElo, "Start")
		
    def lose(oppName, oppElo, scoreDiff):
		# if(abs(elo - ))
		elo -= oppElo
		
	def win(oppName, oppElo, scoreDiff):
		elo += oppElo
		
		
		# log(abs(scoreDiff) + 1) * (2.2 / ((ELOW-ELOL) * .001 + 2.2))