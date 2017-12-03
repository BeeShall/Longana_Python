from random import shuffle

class Stock:
	def __init__(self, maxPipCount):
		self.stock = [(x, y) for x in range(maxPipCount) for y in range(x, maxPipCount)]
		shuffle(self.stock)
		print(self.stock)
		print(len(self.stock))

	def isEmpty(self):
		return len(self.stock) <= 0

	def generateHand(self, handSize):
		hand = self.stock[0:handSize]
		self.stock = self.stock[handSize:]
		print(hand)
		return hand

	def drawDomino(self):
		domino = self.stock[0]
		del self.stock[0]
		return domino

	def toString(self):
		pass


