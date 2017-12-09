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
        if side is self.sides[0] or side is self.sides[2]:
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
        leftSideSpaces=0
        if len(self.sides) > 2:
            leftSideSpaces = (len(self.layout[self.sides[0]])*4)+1
            print(' '*(leftSideSpaces+1), self.sides[2])
            for domino in reversed(self.layout[self.sides[2]]):
                print(' '*leftSideSpaces, self.getDominoString(domino))
         
        print(self.sides[0], end=' ')
        for domino in reversed(self.layout[self.sides[0]]):
            print(self.getDominoString(domino), end=' ')
             
        print(self.getDominoString(self.engine), end=' ')

        for domino in self.layout[self.sides[1]]:
            print(self.getDominoString(domino), end=' ')
        print(self.sides[1])

        if len(self.sides) >3:
            for domino in self.layout[self.sides[3]]:
                print(''*leftSideSpaces, self.getDominoString(domino))
            print(''*leftSideSpaces, self.sides[3])
        
    def getDominoString(self, domino):
        return "%d-%d" % domino


