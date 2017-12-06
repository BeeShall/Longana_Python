from Player import Player

class Computer(Player):
	def __init__(self, name, score, side):
		super().__init__(name,score,side)

	def play(self, layout,playerPassed, *_):
		move =  super().getHint(layout, playerPassed)
		if move is not None:
			super().playDomino(move[1],move[0],layout,playerPassed)
		return move