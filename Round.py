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
		self.playerPassed = {player.side : False for player in players}
		self.passCount = 0
		self.saveAndQuit = False

	def initialize(self):
		if(self.players[0].isHandEmpty()):
			for player in self.players:
				player.setHand(self.stock.generateHand(8))

	def setNextPlayer(self):
		self.nextPlayer = self.players[(self.players.index(
			self.nextPlayer) + 1) % len(self.players)]
	
	def resetPlayerPassed(self):
		self.passCount = 0
		self.playerPassed = {player.side : False for player in self.players}

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
			print('-' * 44)
			while not self.checkIfAnyPlayerHasEngine(self.layout.engine):
				for player in self.players:
					drawnDomino = self.stock.drawDomino()
					if drawnDomino is not None:
						print(player.name, " drew ", drawnDomino)
						player.addDominoInHand(drawnDomino)
						player.drawn = False
			self.layout.setEngine()
			print('-' * 44)

	def playerDraw(self):
		if isinstance(self.nextPlayer, Human):
			if len(self.nextPlayer.getAllPossibleMoves(self.layout, self.playerPassed)) != 0:
				print(self.nextPlayer.name, " already has valid moves in hand!")
				return False
		if(self.nextPlayer.drawn):
			self.passCount += 1
			self.playerPassed[self.nextPlayer.side] = True
			print(self.nextPlayer.name,
				  " did not have any playable move's in hand. So, the player passed!")
			self.setNextPlayer()
			return True
		else:
			drawnDomino = self.stock.drawDomino()
			if drawnDomino is None:
				print("Stock is empty!")
				self.nextPlayer.drawn = True
			else:
				print(self.nextPlayer.name, " drew ", drawnDomino)
				self.nextPlayer.addDominoInHand(drawnDomino)
			return False

	def play(self, domino=None, side=None):
		print('-' * 44)
		playerMove = self.nextPlayer.play(self.layout, self.playerPassed, domino, side)
		print(playerMove)
		if playerMove is not None:
			print(self.nextPlayer.name, " played ", playerMove)
			self.resetPlayerPassed()
			self.setNextPlayer()
		else:
			if isinstance(self.nextPlayer, Human):
				return False
			else:
				self.playerDraw()
		print('-' * 44)
		return True

	def runRound(self):
		while isinstance(self.nextPlayer, Computer):
			if self.checkIfRoundEnded():
				return False
			self.printGameState()
			self.play()
		return True

	def start(self):
		self.initialize()
		if not self.layout.engineSet:
			self.determineFirstPlayer()
		while not self.checkIfRoundEnded():
			if self.runRound():
				self.getHumanMove()
			else:
				break
		
		#at this point roundEnds or user asked to save and quit
		if(self.saveAndQuit):
			return
		print('-' * 44)
		print("The round has ended! ")
		self.calculateRoundWinner()

	def load(self, layout, stock, nextPlayer, playersPassed):
		self.layout.setLayout(layout)
		self.stock.setStock(stock)
		self.nextPlayer = nextPlayer
		self.passCount = playersPassed
		playerIndex = self.players.index(nextPlayer)-1
		
		while playersPassed > 0:
			self.playerPassed[self.players[playerIndex].side] = True
			playerIndex-=1
			playersPassed-=1

		self.start()


	def calculateRoundWinner(self):
		scores  =[]
		print("Round scores for players: ")
		for player in self.players:
			handSum = player.getHandSum()
			print(player.name,": ", handSum)
			scores.append(handSum)
		
		maxScore = max(scores)
		minScore = min(scores)
		minScoreIndexes = [index for index, value in enumerate(scores) if value == minScore]
		if len(minScoreIndexes) > 1:
			print("Since more than one players have the minimum hand sum, the round ends as a draw!")
			return
		winner = self.players[minScoreIndexes[0]]
		print(winner.name," wins the round with a score of ",maxScore )
		winner.addScore(maxScore)

	def printGameState(self):
		print('-' * 44)
		print("Layout:")
		self.layout.printLayout()
		print("\nStock:")
		self.stock.printStock()
		print('-' * 44)
	
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
		self.printGameState()
		print(self.nextPlayer.name,"Hand: ",self.nextPlayer.getHand())
		while not moveValid:
			choice = self.displayUserMenu()
			if choice == 1:
				print(self.nextPlayer.getHand())
				if len(self.nextPlayer.getAllPossibleMoves(self.layout, self.playerPassed)) == 0:
					print(self.nextPlayer.name, " doesn't have any playable moves in hand!")
					if self.playerDraw():
						moveValid = True
				else:
					valid = False
					while not valid:
						move = input(
							"Please enter the domino you'd like to play e.g. 4-5 ::").strip()
						if(len(move) != 3):
							print("Please follow the correct format and try again! length")
						elif (not move[0].isdigit() or not move[2].isdigit()):
							print("Please follow the correct format and try again! not digit")
						else:
							sides = self.layout.getAllSideNames()
							print('-' * 44)
							print("Please select the side to play:")
							for side in sides:
								print(side)
							side = ''
							while side not in sides:
								side = input("Please select a side: ").lower()
							domino = (int(move[0]), int(move[2]))
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
		#ask for save and quit
		choice = ''
		while choice != 'y' and choice != 'n':
			choice = input("Would you like to save and quit? (y/n)").lower()
		
		if(choice == 'y'):
			self.saveAndQuit = True
			return True

		if self.stock.isEmpty() and self.passCount > len(self.players):
			print("Round ended because stock is empty and all players passed")
			return True

		for player in self.players:
			if player.isHandEmpty():
				print("Round ended because ", player.name,"'s hand is empty!")
				return True
		
		return False

	def serialize(self):
		serialRound = {}
		players = []
		for player in self.players:
			players.append(player.serialize())
		serialRound['players'] = players
		serialRound['layout'] = self.layout.getSerializedLayout()
		serialRound['boneyard'] = self.stock.stock
		serialRound['playersPassed'] = self.passCount
		serialRound['nextPlayer'] = self.nextPlayer.name

		return serialRound

