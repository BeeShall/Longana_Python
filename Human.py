from Player import Player
class Human(Player):
	def __init__(self, name, score, side):
		super().__init__(name,score,side)

	def play(self, layout,playerPassed, domino, side):
		if super().playDomino(domino, side, layout, playerPassed):
			self.drawn = False
			return (side, domino)
		else:
			return None