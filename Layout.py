class Layout:
	def __init__(self, engine,  playerNames):
		self.engine = engine
		self.engineSet = False
		self.layout = {}
		self.sides = playerNames
		for player in playerNames:
			self.layout[player] = []

	def getAllSideNames(self):
		return self.sides

	def setEngine(self):
		self.engineSet = True

	def setLayout(self, layout):
		self.layout = layout
		for side in layout:
			if self.engine in self.layout[side]:
				self.layout[side].remove(self.engine)
				self.setEngine()
		print(self.layout)

	def isEngineSet(self):
		return self.engineSet

	def placeDomino(self, domino, side):
		if domino == self.engine:
			self.setEngine()
			return True
		if not self.engineSet or side not in self.layout:
			return False
		validatedDomino = self.validateMove(domino, side)

		if validatedDomino is None:
			return False
		self.layout[side].append(validatedDomino)
		return True

	def unPlace(self, side):
		del self.layout[side][-1]

	def validateMove(self, domino, side):
		if side not in self.layout:
			return None
		checkDomino = ()
		dominoes = self.layout[side]
		if len(dominoes) == 0:
			checkDomino = self.engine
		else:
			checkDomino = dominoes[-1]

		return self.verifyDomino(domino, checkDomino, side)

	def verifyDomino(self, domino, checkDomino, side):
		if side is self.sides[0] or ( len(self.sides)>2 and (side == self.sides[2])):
			if checkDomino[0] == domino[1]:
				return domino
			elif checkDomino[0] == domino[1]:
				return (domino[1], domino[0])
			else:
				return None
		else:
			if checkDomino[1] == domino[0]:
				return domino
			elif checkDomino[1] == domino[1]:
				return (domino[1], domino[0])
			else:
				return None

	def printLayout(self):
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
		if domino[0] == domino[1] :
			print(' '*(spaces-1), "%d-%d" % domino )
		else:
			print(' '*spaces, domino[0])
			print(' '*spaces, "|")
			print(' '*spaces, domino[1])

	def printLeftRightDomino(self, dominoes):
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
		serialLayout = self.layout.copy()
		serialLayout['l'].insert(0,self.engine)
		return serialLayout



