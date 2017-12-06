from Layout import Layout
from Stock import Stock
from Player import Player
from Human import Human
from Computer import Computer


class Round:

	def __init__(self, players=[], roundNo=1):
		self.players = players
		self.MAX_PIP = 10 if len(players) >2 else 7
		enginePip = 0 if (roundNo % self.MAX_PIP == 0) else (
			self.MAX_PIP - (roundNo) % self.MAX_PIP)
		self.layout = Layout((enginePip, enginePip), len(players))
		self.stock = Stock(self.MAX_PIP)
		self.nextPlayer = None
		self.playerPassed = False
		self.passCount = 0

	def initialize(self):
		if(self.players[0].isHandEmpty()):
			for player in self.players:
				player.setHand(self.stock.generateHand(8))

	def setNextPlayer(self):
		self.nextPlayer = self.players[(self.players.index(
			self.nextPlayer) + 1) % len(self.players)]

	def checkIfAnyPlayerHasEngine(self, engine):
		for player in self.players:
			if player.hasDomino(engine):
				print(player.name, " has the engine!")
				player.playDomino(engine,'e')
				self.nextPlayer = player
				self.setNextPlayer()
				return True
		return False

	def determineFirstPlayer(self):
		if not self.layout.engineSet:
			while not self.checkIfAnyPlayerHasEngine(self.layout.engine):
				for player in self.players:
					drawnDomino = self.stock.drawDomino()
					print(player.name, " drew ", drawnDomino)
					player.addDominoInHand(drawnDomino)
					player.drawn = False
			self.layout.setEngine()

	def play(self, domino=None, side=None):
		move = self.nextPlayer.play(self.layout, self.playerPassed, domino, side)

		'''Illegal human move'''
		if move is None:
			return None

		print(self.nextPlayer.name, " played ",move)
		self.setNextPlayer()
		while not isinstance(self.nextPlayer, Human):
			self.layout.printLayout()
			input()
			playerMove = self.nextPlayer.play(self.layout, self.playerPassed)
			if playerMove is not None:
				print(self.nextPlayer.name, " played ",playerMove)
			else:
				if(self.nextPlayer.drawn):
					self.passCount += 1
					self.playerPassed = True
					print(self.nextPlayer.name, " did not have any playable move's in hand. So, the player passed!")
				else:
					drawnDomino = self.stock.drawDomino()
					print(self.nextPlayer.name, " drew ",drawnDomino)
					self.nextPlayer.addDominoInHand(drawnDomino)
					continue
			self.setNextPlayer()


players = [Computer('c1',0,'l'), Computer('c2',0,'r')]
r = Round(players)
r.initialize()
r.determineFirstPlayer()
r.play()
