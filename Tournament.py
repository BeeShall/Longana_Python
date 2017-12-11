from Round import Round
from Human import Human
from Computer import Computer

class Tournament:
	def __init__(self, score=0, players=[], roundCount = 0):
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

	def load(self, data):
		self.score = data['tournamentScore']
		self.roundCount = data['roundNo']
		nextPlayer = None
		for player in data['players']:
			tempPlayer = None
			if player['type'].lower() == 'human':
				tempPlayer = Human(player['name'],player['score'],player['side'])
			else:
				tempPlayer = Computer(player['name'],player['score'],player['side'])
			tempPlayer.setHand(self.parsePips(player['hand']))
			if data['nextPlayer'] == player['name']:
				nextPlayer = tempPlayer
			self.players.append(tempPlayer)
		
		r = Round(self.players, self.roundCount)
		layout = {}
		for side in data['layout']:
			layout[side] = self.parsePips(data['layout'][side])
		r.load(layout, self.parsePips(data['boneyard']), nextPlayer, data['playersPassed'])
		self.start()


	def parsePips(self, pips):
		newDominos = []
		for pip in pips:
			newDominos.append((int(pip[0]), int(pip[2])))
		return newDominos
	
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
