from Layout import Layout
from Stock import Stock
from Player import Player
from Human import Human
from Computer import Computer

class Round:
	""" Class to hold the round """

	def __init__(self, players=[], roundNo=1):
		#list of players in the game
		self.players = players

		#if 2 players max number of pip is 7 else max number of pip is 10
		self.MAX_PIP = 10 if len(players) > 2 else 7

		#calculating the engine pip
		enginePip = 0 if (roundNo % self.MAX_PIP == 0) else (
			self.MAX_PIP - (roundNo) % self.MAX_PIP)
		
		#layout for the round
		self.layout = Layout((enginePip, enginePip), [player.side for player in players])

		#stock for the round
		self.stock = Stock(self.MAX_PIP)

		#to track the next player for the round
		self.nextPlayer = None

		#to keep track of which players passed
		self.playerPassed = {player.side : False for player in players}

		#to keep track of how many players passed consecutively
		self.passCount = 0

		#to keep track if the player decided to save and quit
		self.saveAndQuit = False

	def initialize(self):
		"""To initialize the round

			Args:
				None
			"""
		if(self.players[0].isHandEmpty()):
			for player in self.players:
				player.setHand(self.stock.generateHand(8))

	def setNextPlayer(self):
		"""To set the next player

       Args:
           None
    """

		#get the index of the current player, add 1 to it and the fetch the next player
		self.nextPlayer = self.players[(self.players.index(
			self.nextPlayer) + 1) % len(self.players)]
	
	def resetPlayerPassed(self):
		"""Rest all the player passed state

       Args:
           None
    """
		#reset the pass count
		self.passCount = 0
		#reset passed for each player
		self.playerPassed = {player.side : False for player in self.players}

	def checkIfAnyPlayerHasEngine(self, engine):
		"""To check if any player has engine in hand

       Args:
           engine to look for

		Returns:
			True if any player has engine else False
    """

		for player in self.players:
			if player.hasDomino(engine):
				print(player.name, " has the engine!")
				player.playDomino(engine, 'e')
				self.nextPlayer = player
				self.setNextPlayer()
				return True
		return False

	def determineFirstPlayer(self):
		""" determines the first player for the round

       Args:
           None
    """

		if not self.layout.engineSet:
			print('-' * 44)

			#until the engine has been found check for all players hand
			while not self.checkIfAnyPlayerHasEngine(self.layout.engine):

				#if not in hand, draw dominos from stock for all the players
				for player in self.players:
					drawnDomino = self.stock.drawDomino()
					if drawnDomino is not None:
						print(player.name, " drew ", drawnDomino)
						player.addDominoInHand(drawnDomino)
						player.drawn = False
			self.layout.setEngine()
			print('-' * 44)

	def playerDraw(self):
		""" draw a tile for the player

       Args:
          None
		Returns:
			True if valid, False if invalid
    """

		#if player is human, check that drawing is allowed
		if isinstance(self.nextPlayer, Human):
			if len(self.nextPlayer.getAllPossibleMoves(self.layout, self.playerPassed)) != 0:
				print(self.nextPlayer.name, " already has valid moves in hand!")
				return False
		
		# if player has already drawn, automatically pass and set next player
		if self.nextPlayer.drawn:
			self.passCount += 1
			self.playerPassed[self.nextPlayer.side] = True
			print(self.nextPlayer.name,
				  " did not have any playable move's in hand. So, the player passed!")
			self.setNextPlayer()
			return True
		else:
			#else draw from the stock
			drawnDomino = self.stock.drawDomino()
			if drawnDomino is None:
				#if stock is empty, set drawn to true so that it will automatically be passed on the next iteration
				print("Stock is empty!")
				self.nextPlayer.drawn = True
			else:
				print(self.nextPlayer.name, " drew ", drawnDomino)
				self.nextPlayer.addDominoInHand(drawnDomino)
			return False

	def play(self, domino=None, side=None):
		""" Make a move for the respective player in the round

       Args:
           domino  (tuple) : domino to play default value is None
		   side (string): side to play, default value is None
		Returns:
			True is move was played, False if error
    """

		print('-' * 44)
		playerMove = self.nextPlayer.play(self.layout, self.playerPassed, domino, side)
		print(playerMove)

		#if move was valid reset passed and set next player
		if playerMove is not None:
			print(self.nextPlayer.name, " played ", playerMove)
			self.resetPlayerPassed()
			self.setNextPlayer()
		else:
			#else, if player is human, set move as invalid, if computer draw from stock
			if isinstance(self.nextPlayer, Human):
				return False
			else:
				self.playerDraw()
		print('-' * 44)
		return True

	def runRound(self):
		""" Runs the round for computer player

       Args:
           None
    """

		#until the next player is human, keep playing
		while isinstance(self.nextPlayer, Computer):
			if self.checkIfRoundEnded():
				return False
			self.printGameState()
			self.play()
		return True

	def start(self):
		"""starts the round

       Args:
           None
    """

		self.initialize()
		if not self.layout.engineSet:
			self.determineFirstPlayer()
		while not self.checkIfRoundEnded():
			#getting computer moves
			if self.runRound():
				#getting human moves
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
		""" Loads a round

       Args:
           layout : layout to load
		   stock : stock to load
		   nextPlayer : nextPlayer int he saved game
		   playersPassed : numebrs of player passed in the saved game
    """

		self.layout.setLayout(layout)
		self.stock.setStock(stock)
		self.nextPlayer = nextPlayer

		#setting the playerPassed and passCounts
		if playersPassed is not None:
			self.passCount = playersPassed
			playerIndex = self.players.index(nextPlayer)-1
			
			#if any players have passed, tract back to the respective previous players and set
			#their player passed to true
			while playersPassed > 0:
				self.playerPassed[self.players[playerIndex].side] = True
				playerIndex-=1
				playersPassed-=1
		#if the player passed value if empty, it means the first player has not been determined yet
		else:
			self.determineFirstPlayer()

		self.start()

	def printGameState(self):
		"""Prints the game state

       Args:
           NOne
    """

		print('-' * 44)
		print("Layout:")
		self.layout.printLayout()
		print("\nStock:")
		self.stock.printStock()
		print('-' * 44)
	
	def displayUserMenu(self):
		"""Displays the user menu

       Args:
           None
    """

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
		""" To get and play the human move

       Args:
           None

		Returns:
			None
    """

		moveValid = False
		self.printGameState()
		print(self.nextPlayer.name,"Hand: ",self.nextPlayer.getHand())
		while not moveValid:
			choice = self.displayUserMenu()
			if choice == 1:
				print(self.nextPlayer.getHand())
				#check if player has any valid hands
				if len(self.nextPlayer.getAllPossibleMoves(self.layout, self.playerPassed)) == 0:
					print(self.nextPlayer.name, " doesn't have any playable moves in hand!")

					#if not automatically draw or pass
					if self.playerDraw():
						moveValid = True
				else:
					#get the move from user, validate it and play it
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
				#if player chose to draw
				self.playerDraw()
			elif choice == 3:
				#if player chose to ask for a hint
				hint = self.nextPlayer.getHint(self.layout,self.playerPassed)
				if hint is None:
					print("You don't have any playable moves in hand!")
				else:
					print(hint)

	def checkIfRoundEnded(self):
		"""to check if round ended

       Args:
           None

		Returns:
			True id round ended else False
    """

		#ask for save and quit
		choice = ''
		while choice != 'y' and choice != 'n':
			choice = input("Would you like to save and quit? (y/n)").lower()
		
		if(choice == 'y'):
			self.saveAndQuit = True
			return True

		#if stock is empty and all players passed
		if self.stock.isEmpty() and self.passCount > len(self.players):
			print("Round ended because stock is empty and all players passed")
			return True

		#if any of the hands are empty
		for player in self.players:
			if player.isHandEmpty():
				print("Round ended because ", player.name,"'s hand is empty!")
				return True
		
		return False


	def calculateRoundWinner(self):
		""" calculates the round scores and winner

       Args:
           value (str): the value to add.
    """

		scores  =[]
		print("Round scores for players: ")
		for player in self.players:
			handSum = player.getHandSum()
			print(player.name,": ", handSum)
			scores.append(handSum)
		
		maxScore = max(scores)
		minScore = min(scores)

		#checking for all the minimun scores to see if its a draw
		minScoreIndexes = [index for index, value in enumerate(scores) if value == minScore]

		#if there are more than one people with minimun scores, its a draw
		if len(minScoreIndexes) > 1:
			print("Since more than one players have the minimum hand sum, the round ends as a draw!")
			return

		#else the person with the minimum score gets the maximum score
		winner = self.players[minScoreIndexes[0]]
		print(winner.name," wins the round with a score of ",maxScore )
		winner.addScore(maxScore)

	def serialize(self):
		"""To serialize the current round

       Args:
           None

		Returns:
			dict containing all the round details
    """

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