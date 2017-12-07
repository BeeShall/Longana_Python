from Hand import Hand
import functools

class Player:
	def __init__(self, name, score, side):
		self.name = name
		self.score = score
		self.hand = Hand()
		self.side = side
		self.drawn = False

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
	
	def isHandEmpty(self):
		return self.hand.isHandEmpty()

	def hasDomino(self, domino):
		return self.hand.hasDomino(domino)

	def playDomino(self, domino, side, layout=None, playerPassed=None):
		if side == 'e':
			self.hand.playDomino(domino)
			self.drawn = False
			return True
		if not self.hand.hasDomino(domino):
			print(self.name, " doesn't have the domino in hand")
			return False
		if side != self.side and (not playerPassed) and (domino[0] != domino[1]):
			print(self.name, " cannot play the domino on this side")
			return False
		if layout.placeDomino(domino, side):
			self.hand.playDomino(domino)
			self.drawn = False
			return True

	def play(self):
		pass

	def getBestValidMoves(self, layout, playerPassed):
		validMoves = self.getAllPossibleMoves(layout, playerPassed)
		if len(validMoves) == 0:
			return []
		validMoves.sort(key=functools.cmp_to_key(lambda a,b: 1 if (a[1][0]+a[1][1]) > (b[1][0]+b[1][1]) else -1 if (a[1][0]+a[1][1]) < (b[1][0]+b[1][1]) else 0), reverse=True)
		bestDomino = validMoves[0][1]
		validMoves = list(filter(lambda x: x[1] == bestDomino, validMoves))
		return validMoves

	def getNextBestScoreAfterPlacement(self, layout, move):
		bestScore = 0
		layout.placeDomino(move[1],move[0])
		bestValidMoves= self.getBestValidMoves(layout, False )
		if len(bestValidMoves) != 0:
			bestValidDomino = bestValidMoves[0][1]
			bestScore = bestValidDomino[0]+bestValidDomino[1]
		layout.unPlace(move[0])
		return bestScore
	

	def getHint(self, layout, playerPassed):
		validMoves = self.getBestValidMoves(layout, playerPassed)
		if len(validMoves) == 0:
			return None
		elif len(validMoves) < 2:
			return validMoves[0]
		else:
			scores = [self.getNextBestScoreAfterPlacement(layout, move) for move in validMoves]
			maxIndex = scores.index(max(scores))
			return validMoves[maxIndex]

	def validateMoveAndAdd(self, side, domino, layout, moves):
		validatedDomino = layout.validateMove(domino, side)
		if not validatedDomino is None:
			moves.append((side, domino))

	def getAllPossibleMoves(self, layout, playerPassed):
		validMoves = []
		dominoes = self.hand.getHandDominoes()
		for domino in dominoes:
			if playerPassed or (domino[0] == domino[1]):
				sides = layout.getAllSideNames()
				for side in sides:
					self.validateMoveAndAdd(side, domino, layout, validMoves)
					self.validateMoveAndAdd(side, domino, layout, validMoves)
					self.validateMoveAndAdd(side, domino, layout, validMoves)
					self.validateMoveAndAdd(side, domino, layout, validMoves)
			else:
				self.validateMoveAndAdd(self.side, domino, layout, validMoves)
		return validMoves

	def getHand(self):
		return self.hand.toString()

