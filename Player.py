from model.Hand import Hand

class Player:
	def __init__(self, name, score, side):
		self.name = name
		self.score = score
		self.hand = Hand()
		self.side = side

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
	
	def isHandEmpty(self):
		return self.hand.isHandEmpty()

	def hasDomino(self, domino):
		return self.hand.hasDomino(domino)

	def play(self, domino, layout, side, playerPassed):
		if not self.hand.hasDomino(domino):
			return False
		if side != self.side and (not playerPassed) or (domino[0] != domino[1]):
			return False
		if layout.placeDomino(domino, side):
			self.hand.playDomino(domino)
			return True

	def getHint(self, layout, playerPassed):
		pass

	def validateMoveAndAdd(self, side, domino, layout, moves):
		validatedDomino = layout.validateMove(domino, side)
		if not validatedDomino is None:
			moves.append((side, validatedDomino))

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
