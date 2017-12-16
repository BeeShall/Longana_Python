from random import shuffle

class Stock:
	""" Class to hold the stock"""
	def __init__(self, maxPipCount):
		self.stock = [(x, y) for x in range(maxPipCount) for y in range(x, maxPipCount)]
		shuffle(self.stock)

	def isEmpty(self):
		""" Runs the round for computer player

		Args:
			None

			Returns:
				True if the stock is empty, False if not
		"""
		return len(self.stock) <= 0

	def generateHand(self, handSize):
		""" generate hand of handsize from the stock

	   Args:
		   handSize : handSize

		Returns:
			a list of dominoes with the given handsize
	"""
		hand = self.stock[0:handSize]
		self.stock = self.stock[handSize:]
		return hand

	def drawDomino(self):
		""" draw a domino from the stock

	   Args:
		   None

		Returns:
			top domino from the stock
	"""
		if self.isEmpty():
			return None
		domino = self.stock[0]
		del self.stock[0]
		return domino

	#method to set the stock
	def setStock(self, stock):
		self.stock = stock

	#method to print the stock
	def printStock(self):
		print(self.stock)


