from Layout import Layout
from Stock import Stock
from Player import Player


class Round:
	MAX_PIP = 10

	def __init__(self, players, roundNo):
		self.players = players
		enginePip = 0 if (roundNo % self.MAX_PIP == 0) else (self.MAX_PIP - (roundNo) % self.MAX_PIP)
		print("engine is ", enginePip)
		self.layout = Layout((enginePip, enginePip))
		self.stock = Stock(self.MAX_PIP - 1)

	def initialize(self):
		if(self.players[0].isHandEmpty()):
			for player in self.players:
				print(player.name)
				player.setHand(self.stock.generateHand(8))

	def setNextPlayer(self): 
		self.nextPlayer =  self.players[self.players.index(self.nextPlayer) + 1];
		print("Next Player is", self.nextPlayer.name)

	def checkIfAnyPlayerHasEngine(self, engine):
		for player in self.players:
			if player.hasDomino(engine):
				print(player.name," has the engine!")
				self.nextPlayer = player
				self.setNextPlayer()
				return True
		return False


	def determineFirstPlayer(self):
		if not self.layout.engineSet:
			while not self.checkIfAnyPlayerHasEngine(self.layout.engine):
				for player in self.players:
					drawnDomino = self.stock.drawDomino()
					print(player.name," drew ",drawnDomino)
					player.addDominoInHand(drawnDomino)
			self.layout.setEngine()


players = [Player('1',0,'l'), Player('2',0,'r'), Player('3',0,'t'), Player('4',0,'b')]
r = Round(players,3)
r.initialize()
r.determineFirstPlayer()
