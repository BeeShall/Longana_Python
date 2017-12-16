class Layout:
	""" Class to hold the layout """
	def __init__(self, engine,  playerNames):
		#engine for the round
		self.engine = engine
		#if the engine has been set yet or not
		self.engineSet = False
		#to hold the layout for each sie
		self.layout = {}
		#to store the side names for the all the players in the order they were created
		self.sides = playerNames
		for player in playerNames:
			#list to hold the doino for each player
			self.layout[player] = []

	#to get list of all the side names
	def getAllSideNames(self):
		return self.sides

	#to set the engine
	def setEngine(self):
		self.engineSet = True

	def setLayout(self, layout):
		""" to set the layout

			Args:
				layout : the layout to set
		"""
		self.layout = layout
		for side in layout:
			if self.engine in self.layout[side]:
				self.layout[side].remove(self.engine)
				self.setEngine()
		print(self.layout)

	#to get if the engine is set
	def isEngineSet(self):
		return self.engineSet

	def placeDomino(self, domino, side):
		"""to place the domino on the given side

			Args:
				domino : domino to play
				side : side to play the domino in

			Returns:
				True if domino was placed, False if not
		"""

		#if domino is the engine
		if domino == self.engine:
			self.setEngine()
			return True

		#if engine is not set, domino is not placeable
		if not self.engineSet or side not in self.layout:
			return False
		validatedDomino = self.validateMove(domino, side)

		#if domino cannot be placed
		if validatedDomino is None:
			return False

		self.layout[side].append(validatedDomino)
		return True

	#method to remove the domino the given side
	def unPlace(self, side):
		del self.layout[side][-1]


	def validateMove(self, domino, side):
		""" to validate the given move

			Args:
				domino : domino to play
				side : side to play the domino in

			Returns:
				validated domino, None if no domino
		"""
		if side not in self.layout:
			return None

		checkDomino = ()
		dominoes = self.layout[side]

		#if there are no dominoes on the side then the domino has to be placed next to domino
		if len(dominoes) == 0:
			checkDomino = self.engine
		else:
			checkDomino = dominoes[-1]

		return self.verifyDomino(domino, checkDomino, side)

	def verifyDomino(self, domino, checkDomino, side):
		""" to verify if the domino can be placed next to the checkDomino

			Args:
				domino : domino to play
				checkDomino : domino to place the domino against
				side : side to play the domino in

			Returns:
				validated domino, None if no domino
		"""

		#if the side is left or top
		if side is self.sides[0] or ( len(self.sides)>2 and (side == self.sides[2])):
			if checkDomino[0] == domino[1]:
				return domino
			elif checkDomino[0] == domino[1]:
				return (domino[1], domino[0])
			else:
				return None
		#if the side is right or bottom
		else:
			if checkDomino[1] == domino[0]:
				return domino
			elif checkDomino[1] == domino[1]:
				return (domino[1], domino[0])
			else:
				return None

	def printLayout(self):
		""" to print the layout

			Args:
				None

			Returns:
				None
		"""

		leftSideSpaces = 0
		if len(self.sides) > 2:
			leftSideSpaces = (len(self.layout[self.sides[0]])*4)+len(self.sides[0])+1
			print(' '*(leftSideSpaces), self.sides[2])
			for domino in reversed(self.layout[self.sides[2]]):
				self.printTopBottomDomino(domino, leftSideSpaces)

		#print(self.sides[0], end=' ')

		
		lines = self.printLeftRightDomino(reversed(self.layout[self.sides[0]]))
		firstLine = lines[0]
		secondLine = lines[1]


		firstLine += " %d  " % self.engine[0]
		secondLine += " |  "


		#print("%d-%d" % self.engine, end=' ')

		newLines = self.printLeftRightDomino(self.layout[self.sides[1]])

		print(" ",firstLine+newLines[0])
		print(self.sides[0], secondLine+newLines[1], self.sides[1] )
		print(" ",firstLine+newLines[0])

		
		if len(self.sides) >3:
			for domino in self.layout[self.sides[3]]:
				 self.printTopBottomDomino(domino, leftSideSpaces)
			print(' '*(leftSideSpaces), self.sides[3])

	def printTopBottomDomino(self, domino, spaces):
		""" to top and bottom domino

			Args:
				domino : domino to print
				spaces : spaces to print before the domino
		"""
		if domino[0] == domino[1] :
			print(' '*(spaces-1), "%d-%d" % domino )
		else:
			print(' '*spaces, domino[0])
			print(' '*spaces, "|")
			print(' '*spaces, domino[1])

	def printLeftRightDomino(self, dominoes):
		""" to left and right domino

			Args:
				domino : domino to play
		"""
		firstLine = ""
		secondLine =""
		for domino in dominoes:
			if domino[0] == domino[1] :
				firstLine += " %d  " % domino[0]
				secondLine += " |  "
			else:
				firstLine += "    "
				secondLine += "%d-%d " % domino
		return (firstLine,secondLine)
		


	def getSerializedLayout(self):
		""" to get the serialized layout

			Args:
				None

			Returns:
				copy of the layout
		"""
		serialLayout = self.layout.copy()
		serialLayout['l'].insert(0,self.engine)
		return serialLayout



