import json

from Round import Round
from Human import Human
from Computer import Computer


class Tournament:
	"""Class to hold the tournamnet"""

	def __init__(self, score=0, players=[], roundCount=0):
		
		#score for the tournament
		self.score = score

		#list of players for the game
		self.players = players

		#round Number
		self.roundCount = roundCount

	def start(self):
		"""Starts the torunament

			Args:
				None
			
			Return:
				None
		"""

		while not self.checkIfTournamentEnded():
			input()
			self.roundCount += 1
			r = Round(self.players, self.roundCount)
			r.start()
			if r.saveAndQuit:
				self.serialize(r.serialize())
				break
			#check for save and quit
			input()

	def load(self, data):
		"""Loads an existing tournamnet

			Args:
				data (dict) : data to load from file
		"""

		self.score = data['tournamentScore']
		self.roundCount = data['roundNo']
		nextPlayer = None
		#creating the game players based on the player type
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
		"""Parses the pips as list to a tuple

			Args:
				pips(list) : pips to parse

			Returns:
				list of parses pips as tuples
		"""

		newDominos = []
		for pip in pips:
			newDominos.append(tuple(pip))
		return newDominos

	def checkIfTournamentEnded(self):
		"""Checks if tournamnet has ended

			Args:
				None

			Returns:
				True if ended, False if not
		"""

		winner = None
		print("Tournament scores for players: ")
		for player in self.players:
			print(player.name, ": ", player.score)
			#if any player's score exceeds the tournament score, the player is the winner
			if player.score >= self.score:
				winner = player
		if winner is not None:
			print(winner.name, " won the torunament with a score of ", winner.score)
			return True
		else:
			return False

	def serialize(self, serial):
		"""Serialized the torunament to a file

			Args:
				serial(dict) : serialized round
			
			Returns:
				None
		"""

		serial["tournamentScore"] = self.score
		serial["roundNo"] = self.roundCount
		with open('./serial/game.json', 'w') as outfile:
			json.dump(serial, outfile)
