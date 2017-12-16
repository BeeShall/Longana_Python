from Player import Player
class Human(Player):
	""" Class to hold the human player """
	def __init__(self, name, score, side):
		super().__init__(name,score,side)

	def play(self, layout,playerPassed, domino, side):
		""" play method for the human player

			Args:
				layout : layout for the player to play on
				playerPassed : list of the players passed
				domino : domino to play
				side : side to play the domino 
		"""
		if super().playDomino(domino, side, layout, playerPassed):
			self.drawn = False
			return (side, domino)
		else:
			return None