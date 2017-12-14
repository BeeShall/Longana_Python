from random import shuffle

class Stock:
	def __init__(self, maxPipCount):
		self.stock = [(x, y) for x in range(maxPipCount) for y in range(x, maxPipCount)]
		shuffle(self.stock)

	def isEmpty(self):
		return len(self.stock) <= 0

	def generateHand(self, handSize):
		hand = self.stock[0:handSize]
		self.stock = self.stock[handSize:]
		return hand

	def drawDomino(self):
		if self.isEmpty():
			return None
		domino = self.stock[0]
		del self.stock[0]
		return domino

	def setStock(self, stock):
		self.stock = stock

	def printStock(self):
		print(self.stock)

	def serialize(self):
		stock = []
		for domino in self.stock:
			stock.append(str(domino[0])+"-"+str(domino[2]))
		return stock
