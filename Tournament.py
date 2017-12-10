from Round import Round
from Human import Human
from Computer import Computer

class Tournament:
	def __init__(self, score, players, roundCount = 0):
		self.score = score
		self.players = players
		self.roundCount = roundCount
	
	def start(self):
		while(not self.checkIfTournamentEnded()):
			input()
			self.roundCount+=1
			r = Round(self.players, self.roundCount)
			r.start()
			input()
	
	def checkIfTournamentEnded(self):
		winner = None
		print("Tournament scores for players: ")
		for player in self.players:
			print(player.name, ": ", player.score)
			if player.score > self.score:
				winner = player
		if winner is not None:
			print(winner.name, " won the torunament with a score of ",winner.score)
			return True
		else:
			return False
