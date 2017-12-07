from Layout import Layout
from Stock import Stock
from Player import Player
from Human import Human
from Computer import Computer


class Round:

	def __init__(self, players=[], roundNo=1):
		self.players = players
		self.MAX_PIP = 10 if len(players) > 2 else 7
		enginePip = 0 if (roundNo % self.MAX_PIP == 0) else (
			self.MAX_PIP - (roundNo) % self.MAX_PIP)
		self.layout = Layout((enginePip, enginePip), [player.side for player in players])
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
				player.playDomino(engine, 'e')
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

	def playerDraw(self):
		if isinstance(self.nextPlayer, Human):
			if len(self.nextPlayer.getAllPossibleMoves(self.layout, self.playerPassed)) != 0:
				print(self.nextPlayer.name, " already has valid moves in hand!")
				return False
		if(self.nextPlayer.drawn):
			self.passCount += 1
			self.playerPassed = True
			print(self.nextPlayer.name,
				  " did not have any playable move's in hand. So, the player passed!")
			self.setNextPlayer()
		else:
			drawnDomino = self.stock.drawDomino()
			print(self.nextPlayer.name, " drew ", drawnDomino)
			self.nextPlayer.addDominoInHand(drawnDomino)
		return True

	def play(self, domino=None, side=None):
		playerMove = self.nextPlayer.play(self.layout, self.playerPassed, domino, side)
		if playerMove is not None:
			print(self.nextPlayer.name, " played ", playerMove)
			print("\n Layout:")
			self.layout.printLayout()
			self.setNextPlayer()
		else:
			if isinstance(self.nextPlayer, Human):
				return False
			else:
				self.playerDraw()
		return True

	def runRound(self):
		while isinstance(self.nextPlayer, Computer):
			if self.checkIfRoundEnded():
				return False
			self.play()
		return True

	def start(self):
		self.initialize()
		self.determineFirstPlayer()
		while not self.checkIfRoundEnded():
			if self.runRound():
				self.getHumanMove()
	
	def displayUserMenu(self):
		choice = -1
		while choice < 0 or choice > 3:
			print('-' * 44)
			print("Please select one of the following options: ")
			print("1. Make a move ")
			print("2. Draw from stock/ Pass")
			print("3. Can I get a hint?")
			print('-' * 44)
			choice = int(input("Plese select a menu choice: "))
			print()
		return choice


	def getHumanMove(self):
		moveValid = False
		print(self.nextPlayer.getHand())
		while not moveValid:
			choice = self.displayUserMenu()
			if choice == 1:
				print(self.nextPlayer.getHand())
				if len(self.nextPlayer.getAllPossibleMoves(self.layout, self.playerPassed)) == 0:
					print(self.nextPlayer.name, " doesn't have any playable moves in hand!")
					self.playerDraw()
				else:
					valid = False
					while not valid:
						move = input(
							"Please enter the domino you'd like to play e.g. 4-5 ::").strip()
						if(len(move) != 3):
							print("Please follow the correct format and try again!")
						elif (not move[1].isdigit() or not move[3].isdigit()):
							print("Please follow the correct format and try again!")
						else:
							sides = self.layout.getAllSideNames()
							print("Please select the side to play in using the respective index")
							for x in range(0,len(sides)):
								print(x+1, sides[x])
							side = -1
							while side< 0 or side >len(sides):
								side = int(input("Please enter the index"))
							domino = (int(move[2]), int(move[4]))
							if self.play(domino, side):
								return
							else:
								print("Please enter a valid move!")
			elif choice == 2:
				self.playerDraw()
			elif choice == 3:
				hint = self.nextPlayer.getHint(self.layout,self.playerPassed)
				if hint is None:
					print("You don't have any playable moves in hand!")
				else:
					print(hint)

	def checkIfRoundEnded(self):
		if self.stock.isEmpty() and self.passCount > 2:
			return True

		for player in self.players:
			if player.isHandEmpty():
				return True
		
		return False
		

players = [Computer('C1', 0, 'l'), Human('H1', 0, 'r'), Computer('C3', 0, 't')]
r = Round(players)
r.start()

		
	

