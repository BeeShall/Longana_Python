from model.Layout import Layout
from model.Stock import Stock
from model.Player import Player


class Round:
	MAX_PIP = 10

	def __init__(self, players=[], roundNo=0):
		self.players = players
		enginePip = 0 if (roundNo % self.MAX_PIP == 0) else (self.MAX_PIP - (roundNo) % self.MAX_PIP)
		print("engine is ", enginePip)
		self.layout = Layout((enginePip, enginePip))
		self.stock = Stock(self.MAX_PIP - 1)
		self.nextPlayer = None

	def initialize(self):
		if(self.players[0].isHandEmpty()):
			for player in self.players:
				print(player.name)
				player.setHand(self.stock.generateHand(8))

	def setNextPlayer(self): 
		self.nextPlayer =  self.players[(self.players.index(self.nextPlayer) + 1) % len(self.players)]
		print("Next Player is", self.nextPlayer.name)

	def getNextPlayer(self):
		print(self.nextPlayer.name)

	def checkIfAnyPlayerHasEngine(self, engine, log):
		for player in self.players:
			if player.hasDomino(engine):
				print(player.name," has the engine!")
				log.append({player.name:True})
				self.nextPlayer = player
				self.setNextPlayer()
				return True
		return False


	def determineFirstPlayer(self):
		log = []
		if not self.layout.engineSet:
			while not self.checkIfAnyPlayerHasEngine(self.layout.engine, log):
				for player in self.players:
					drawnDomino = self.stock.drawDomino()
					log.append({player.name:drawnDomino})
					player.addDominoInHand(drawnDomino)
			self.layout.setEngine()
		return log
