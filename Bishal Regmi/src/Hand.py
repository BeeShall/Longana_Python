from functools import reduce

class Hand:
	""" Class to hold the Hand """
	def __init__(self):
		self.hand = []

	#method to set the hand
	def setHand(self, hand):
		self.hand = hand
	
	#checks if the domino is in hand
	def hasDomino(self, domino):
		return domino in self.hand

	#plays the domino from hand
	def playDomino(self, domino):
		self.hand.remove(domino)

	#add the domino to hand
	def addDomino(self, domino):
		self.hand.append(domino)
	
	#get the no of dominos in hand
	def getHandSize(self):
		return len(self.hand)

	#check if the hand is empty
	def isHandEmpty(self):
		return len(self.hand) == 0

	#get the sum of all the dominoes in hand
	def getHandSum(self):
		return sum( x+y for x,y in self.hand)

	#get list of dominoes in hand
	def getHandDominoes(self):
		return self.hand[:]

