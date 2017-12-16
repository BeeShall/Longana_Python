from Hand import Hand
import functools

class Player:
	""" Class to hold the player data
	"""

	def __init__(self, name, score, side):
		#name for the player
		self.name = name
		#score for the player
		self.score = score
		#hand of the player
		self.hand = Hand()
		#name of the side in the layout for the player
		self.side = side
		#to hold if the player has drawn a tile yet or not
		self.drawn = False

	"""				Getter and Setters and small utility functions						"""
	def getScore(self):
		return self.score

	def setHand(self, hand):
		self.hand.setHand(hand)

	def setScore(self, score):
		self.score = score

	def addScore(self, score):
		self.score += score

	def addDominoInHand(self, domino):
		self.hand.addDomino(domino)
		self.drawn = True

	def getHandSum(self):
		return self.hand.getHandSum()

	def isHandEmpty(self):
		return self.hand.isHandEmpty()

	def hasDomino(self, domino):
		return self.hand.hasDomino(domino)

	def getHand(self):
		return self.hand.getHandDominoes()

	"""					"""

	def playDomino(self, domino, side, layout=None, playerPassed={}):
		""" plays the given domino after layout validation

	   Args:
		   domino : domino to play
		   side : side to play the domino in
		   layout: layout to play the domino in
		   playerpassed: list of all the players passed
	"""

		#if side is the engine
		if side == 'e':
			self.hand.playDomino(domino)
			self.drawn = False
			return True
		#if the domino is not in hand
		if not self.hand.hasDomino(domino):
			print(self.name, " doesn't have the domino in hand")
			return False
		#if the domino is tried to place on the other side
		if side != self.side and (not playerPassed[side]) and (domino[0] != domino[1]):
			print(self.name, " cannot play the domino on this side")
			return False
		#finally place th domino, if all the othe condition fail
		if layout.placeDomino(domino, side):
			self.hand.playDomino(domino)
			self.drawn = False
			return True

	def play(self):
		#to make the player move
		pass

	def getBestValidMoves(self, layout, playerPassed):
		"""To get all the valid moves with the best scored

	   Args:
		   layout: layout to play the domino in
		   playerpassed: list of all the players passed
	"""

		#get all the valid moves
		validMoves = self.getAllPossibleMoves(layout, playerPassed)

		#if there are no valid moves
		if len(validMoves) == 0:
			return []

		#sort the moves based on the score
		validMoves.sort(key=functools.cmp_to_key(lambda a,b: 1 if (a[1][0]+a[1][1]) > (b[1][0]+b[1][1]) else -1 if (a[1][0]+a[1][1]) < (b[1][0]+b[1][1]) else 0), reverse=True)
		bestDomino = validMoves[0][1]

		#get all the moves that yield the same score
		validMoves = list(filter(lambda x: x[1] == bestDomino, validMoves))
		return validMoves

	def getNextBestScoreAfterPlacement(self, layout, move):
		""" To get the next best score after makig the move

	   Args:
		   layout: layout to play the domino in
		   move : move to play
	"""

		#place the domino
		#get all the valid moves after placing the domino
		#return the best score yielded from the moves
		bestScore = 0
		layout.placeDomino(move[1],move[0])
		bestValidMoves= self.getBestValidMoves(layout, {} )
		if len(bestValidMoves) != 0:
			bestValidDomino = bestValidMoves[0][1]
			bestScore = bestValidDomino[0]+bestValidDomino[1]
		layout.unPlace(move[0])
		return bestScore


	def getHint(self, layout, playerPassed):
		"""get the hint fo the player given the layout

	   Args:
		   layout: layout to play the domino in
		   playerpassed: list of all the players passed
	"""

		print("Strategy: ")
		#get all the valid moves
		validMoves = self.getBestValidMoves(layout, playerPassed)

		#if no valid moves
		if len(validMoves) == 0:
			print("Player doesn't have any valid moves in hand!")
			return None
		#if valid moves is only one, then it can be placed on only one side so return it
		elif len(validMoves) < 2:
			print("The best move that yields the highest score in hand is ",validMoves[0])
			return validMoves[0]
		#if there are more than one valid moves, then it can be placed on multiple side
		else:
			print("The best move that yields the highest score in hand is ",validMoves[0])
			print("However, this move can also be placed on other player's locations!")

			#fetch the next best score after placing on each side
			scores = [self.getNextBestScoreAfterPlacement(layout, move) for move in validMoves]

			#return the moves with the max next best score
			maxIndex = scores.index(max(scores))
			print("This domino will yield the best score if placed ", validMoves[maxIndex])
			return validMoves[maxIndex]

	def validateMoveAndAdd(self, side, domino, layout, moves):
		"""validate all the move and add to the best moves list

	   Args:
		   side : side to play the domino in
		   domino : domino to play
		   layout : layout to play the domino in
		   moves : list of valid moves
	"""

		validatedDomino = layout.validateMove(domino, side)
		if not validatedDomino is None:
			moves.append((side, domino))

	def getAllPossibleMoves(self, layout, playerPassed):
		""" get all possible moves

	   Args:
		   layout: layout to play the domino in
		   playerpassed: list of all the players passed
	"""

		validMoves = []
		dominoes = self.hand.getHandDominoes()
		for domino in dominoes:
			self.validateMoveAndAdd(self.side, domino, layout, validMoves)
			sides = layout.getAllSideNames()
			for side in sides:
				if (side in playerPassed and playerPassed[side]) or (domino[0] == domino[1]):
					self.validateMoveAndAdd(side, domino, layout, validMoves)
		return validMoves


	def serialize(self):
		"""serialize the player class

			Args:
				None

			Returns:
				Dictionary including the serialized player
		"""

		return {
			"name": self.name,
			"type": type(self).__name__,
			"hand": self.hand.getHandDominoes(),
			"side": self.side,
			"score": self.score
		}


