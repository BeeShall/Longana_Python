from functools import reduce

class Hand:
	def __init__(self):
		self.hand = []

	def setHand(self, hand):
		self.hand = hand
	
	def hasDomino(self, domino):
		return domino in self.hand

	def playDomino(self, domino):
		self.hand.remove(domino)

	def addDomino(self, domino):
		self.hand.append(domino)
	
	def getHandSize(self):
		return len(self.hand)

	def isHandEmpty(self):
		return len(self.hand) == 0

	def getHandSum(self):
		return sum( x+y for x,y in self.hand)

	def getHandDominoes(self):
		return self.hand

	def toString(self):
		print(self.hand)
