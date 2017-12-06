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
			return False
		if side != self.side and (not playerPassed) and (domino[0] != domino[1]):
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
		layout.placeDomino(move[1],move[0])
		print(move)
		bestValidDomino = self.getBestValidMoves(layout, False )[0][1]
		if bestValidDomino is None:
			return 0
		layout.unPlace(move[0])
		return bestValidDomino[0]+bestValidDomino[1]
	

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
				self.validateMoveAndAdd('l', domino, layout, validMoves)
				self.validateMoveAndAdd('r', domino, layout, validMoves)
				self.validateMoveAndAdd('t', domino, layout, validMoves)
				self.validateMoveAndAdd('b', domino, layout, validMoves)
			else:
				self.validateMoveAndAdd(self.side, domino, layout, validMoves)
		return validMoves

