class Layout:
    def __init__(self, engine,  playerNames):
        self.engine = engine
        self.engineSet = False
        self.layout = {}
        for player in playerNames:
            self.layout[player] = []

    def getAllSideNames(self):
        return self.layout.keys()

    def setEngine(self):
        self.engineSet = True

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

        return self.verifyDomino(domino, checkDomino)

    def verifyDomino(self, domino, checkDomino):
        if checkDomino[1] == domino[0]:
            return domino
        elif checkDomino[1] == domino[1]:
            return (domino[1], domino[0])
        else:
            return None

    def printLayout(self):
        print(self.layout)

