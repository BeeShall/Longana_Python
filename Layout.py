class Layout:
    def __init__(self, engine):
        self.engine = engine
        self.engineSet = False
        self.layout = {
            'l': [],
            'r': [],
            't': [],
            'b': []
        }
		
    def setEngine(self):
        self.engineSet = True

    def isEngineSet(self):
        return self.engineSet

    def placeDomino(self, domino, side):
        if domino == self.engine:
            self.setEngine()
            return True
        if not self.engineSet:
            return False
        validatedDomino = self.validateMove(domino, side)

        if validatedDomino is None:
            return False
        self.layout[side].append(validatedDomino)
        print(self.layout[side])
        return True

    def validateMove(self, domino, side):
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

