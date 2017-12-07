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
			if len(self.nextPlayer.getAllPossibleMoves()) != 0:
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

	def playerHint(self):
		return self.nextPlayer.getHint(self.layout,self.playerPassed)

	def play(self, domino=None, side=None):
		if isinstance(self.nextPlayer, Human):
			if(domino is None):
				return True
			move = self.nextPlayer.play(
				self.layout, self.playerPassed, domino, side)

			'''Illegal human move'''
			if move is None:
				return False

			print(self.nextPlayer.name, " played ", move)
			print("\n Layout:")
			self.layout.printLayout()
			self.setNextPlayer()
		while not isinstance(self.nextPlayer, Human):
			input()
			playerMove = self.nextPlayer.play(self.layout, self.playerPassed)
			if playerMove is not None:
				print(self.nextPlayer.name, " played ", playerMove)
				print("\n Layout:")
				self.layout.printLayout()
				self.setNextPlayer()
			else:
				self.playerDraw()
		return True


def displayUserMenu():
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


def getHumanMove(humanPlayer):
	moveValid = False
	print(humanPlayer.getHand())
	while not moveValid:
		choice = displayUserMenu()
		if choice == 1:
			print(humanPlayer.getHand())
			valid = False
			while not valid:
				move = input(
					"Please enter the domino and side you'd like to play e.g. l 4 5 ::")
				move = move.lower()
				if(len(move) != 5):
					print("Please follow the correct format and try again!")
				elif(move[0] != 'l' and move[0] != 'r'):
					print("Please enter a valid side!")
				elif (not move[2].isdigit() or not move[4].isdigit()):
					print("Please follow the correct format and try again!")
				else:
					side = move[0]
					domino = (int(move[2]), int(move[4]))
					if r.play(domino, side):
						valid = True
					else:
						print("Please enter a valid move!")
		elif choice == 2:
			r.playerDraw()
		elif choice == 3:
			hint = r.playerHint()
			if hint is None:
				print("You don't have any playable moves in hand!")
			else:
				print(hint)


players = [Computer('Computer 1', 0, 'l'), Human('Human 1', 0, 'r'), Computer('Computer 3', 0, 't')]
r = Round(players)
r.initialize()
r.determineFirstPlayer()
r.play()
while True:
	getHumanMove(players[1])
