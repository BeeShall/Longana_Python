from Player import Player

class Computer(Player):
	def __init__(self, name, score, side):
		super().__init__(name,score,side)

	def play(self, layout,playerPassed, *_):
		""" play method for the computer player

			Args:
				layout : layout for the player to play on
				playerPassed : list of the players passed
		"""
		print(self.name,"Hand: ", self.hand.getHandDominoes())
		move =  super().getHint(layout, playerPassed)
		if move is not None:
			super().playDomino(move[1],move[0],layout,playerPassed)
			self.drawn = False
		return move