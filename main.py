import datetime
from copy import deepcopy
from queue import PriorityQueue


# for ucs h(n)
def noHeuristic(x):
    return 0


# for gbfs g(n)
def noCostFromParent(x):
    return 0


# def numberOfBlockingVehiclesHeuristic(state):
#     been = {}
#     count = 0
#     x = 0
#     for i in range(0, 6):
#         if state[2][i] == 'A':
#          for j in range(i,6):
#              if state[2][j] != 'A':


# for ucs g(n)
def pathFromPatent(node):
    return 1 + node.costOfMove


class stateSpace:
    def __init__(self, gameboard, fuelOfCars, costOfMove, heuristicCost, carMovedWithDirection, parent, carMoved):
        self.gameboard = gameboard
        self.fuelOfCars = fuelOfCars
        self.costOfMove = costOfMove
        self.heuristicCost = heuristicCost
        self.combinedCost = costOfMove + heuristicCost
        self.carMovedWithDirection = carMovedWithDirection
        self.stringRep = ''.join([item for innerlist in gameboard for item in innerlist])
        self.moved = carMoved
        self.parent = parent

    def __eq__(self, other):
        if other == None:
            return False
        return ((self.costOfMove) == (other.costOfMove))

    def __ne__(self, other):
        return not (self.costOfMove == other.costOfMove)

    def __lt__(self, other):
        return (self.costOfMove) < (other.costOfMove)

    def solution(self):
        if self.gameboard[2][5] == 'A':
            return True
        else:
            return False


def writeToSearch(totalCost, searchCost, heurisitcCost, board, fuels, name, number):
    res = str(totalCost) + ' ' + ' ' + str(searchCost) + ' ' + str(heurisitcCost) + ' ' + board + fuels + '\n'
    with open(name + "-search-" + str(number) + ".txt", "a+") as myfile:
        myfile.write(res)


class gamePlayer:
    def __init__(self, dataStructure, gameString, initalFuel, heuristic, pathCostFunction, ucs, gbfs, algoA):
        gameState = [["." for x in range(6)] for y in range(6)]
        for i in range(0, 6):
            for j in range(0, 6):
                gameState[i][j] = gameString[j + (6 * i)]
        init = stateSpace(gameState, initalFuel, 0, 0, "none", None, ' ')
        self.openList = dataStructure
        self.openList.put(init)
        self.heuristic = heuristic
        self.openListTracker = {init.stringRep: init.costOfMove}
        self.closedList = {}
        self.pathCostFunction = pathCostFunction
        self.timing = 0
        self.isAlgoA = algoA
        self.isGBFS = gbfs
        self.isUCS = ucs
        self.getRidOf = {}
        self.newStates = []
        self.reOrder = False
        strRep = 'Car fuel available: '
        for car in initalFuel:
            strRep += car + ':' + str(initalFuel[car]) + ", "

        self.startingFuel = strRep
        self.winner = None

    def buildStatesUCS(self, currentState, i, j, start, temp, costFromRoot, heuristicCost, message):
        fuelCopy = currentState.fuelOfCars.copy()
        fuelCopy[currentState.gameboard[i][j]] -= start
        newState = stateSpace(temp, fuelCopy, costFromRoot, heuristicCost,
                              message,
                              currentState, currentState.gameboard[i][j])
        if newState.stringRep not in self.closedList:
            if newState.stringRep in self.openListTracker and self.openListTracker[
                newState.stringRep] > newState.combinedCost:
                self.newStates.append(newState)
                self.reOrder = True
                self.getRidOf[newState.stringRep] = True
            elif newState.stringRep not in self.openListTracker:
                self.newStates.append(newState)

    def buildStatesGBFS(self, currentState, i, j, start, temp, costFromRoot, heuristicCost, message):
        fuelCopy = currentState.fuelOfCars.copy()
        fuelCopy[currentState.gameboard[i][j]] -= start
        newState = stateSpace(temp, fuelCopy, costFromRoot, heuristicCost,
                              message,
                              currentState, currentState.gameboard[i][j])
        if newState.stringRep not in self.closedList and newState.stringRep not in self.openListTracker:
            self.newStates.append(newState)

    def buildStatesAlgoA(self, currentState, i, j, start, temp, costFromRoot, heuristicCost, message):
        fuelCopy = currentState.fuelOfCars.copy()
        fuelCopy[currentState.gameboard[i][j]] -= start
        newState = stateSpace(temp, fuelCopy, costFromRoot, heuristicCost,
                              message,
                              currentState, currentState.gameboard[i][j])
        if newState.stringRep in self.closedList:
            if self.closedList[newState.stringRep] <= newState.combinedCost:
                return
            else:
                del self.closedList[newState.stringRep]
                self.newStates.append(newState)
                return
        if newState.stringRep in self.openListTracker:
            if self.openListTracker[newState.stringRep] <= newState.combinedCost:
                return
            else:
                self.newStates.append(newState)
                self.reOrder = True
                self.getRidOf[newState.stringRep] = True
                return
        self.newStates.append(newState)

    def checkAlgoAndBuildStates(self, currentState, i, j, start, temp, costFromRoot, heuristicCost, message):
        if self.isUCS:
            self.buildStatesUCS(currentState, i, j, start, temp, costFromRoot, heuristicCost,
                                message)
        elif self.isGBFS:
            self.buildStatesGBFS(currentState, i, j, start, temp, costFromRoot, heuristicCost,
                                 message)
        elif self.isAlgoA:
            self.buildStatesAlgoA(currentState, i, j, start, temp, costFromRoot, heuristicCost,
                                  message)

    def writeToSolution(self, name, number):
        if self.winner is None:
            with open(name + "-search-" + str(number) + ".txt", "a+") as myFile:
                myFile.write("no solution")
        else:
            searchPath = []
            win = self.winner
            count = 0
            while win is not None:
                searchPath.append(win)
                win = win.parent

            searchPath.reverse()
            with open(name + "-SOL-" + str(number) + ".txt", "a+") as myFile:
                myFile.write("--------------------------------------------------------------------------------")
                myFile.write('\n')
                myFile.write("Initial board configuration: " + searchPath[0].stringRep)
                myFile.write('\n')
                myFile.write('\n')
                myFile.write(prettyPrint(searchPath[0].gameboard))
                myFile.write('Car fuel available: ' + self.startingFuel)
                myFile.write('\n')
                myFile.write('\n')
                myFile.write('Runtime:' + str(self.timing) + 'seconds')
                myFile.write('\n')
                myFile.write('\n')
                myFile.write('Search path length:' + str(len(self.closedList)))
                myFile.write('\n')
                myFile.write('\n')
                myFile.write('Solution path length:' + str(len(searchPath) - 1) + 'moves')
                myFile.write('\n')
                myFile.write('\n')
                solutionString = ''
                searchPath = searchPath[1:]
                for state in searchPath:
                    solutionString += ' ' + state.carMovedWithDirection + '; '
                myFile.write('Solution path:' + solutionString)
                myFile.write('\n')
                myFile.write('\n')

                for state in searchPath:
                    myFile.write(state.carMovedWithDirection + '       ' + str(
                        state.fuelOfCars[state.moved]) + ' ' + state.stringRep + ' ' + getFormattedFuel(
                        state.fuelOfCars))
                    myFile.write('\n')
                myFile.write('\n')
                myFile.write('\n')
                myFile.write(prettyPrint(searchPath[len(searchPath) - 1].gameboard))

    def writeSearchFile(self, searchAlgo, number):
        for k, value in self.closedList.items():
            writeToSearch(value.combinedCost, value.costOfMove, value.heuristicCost, value.stringRep,
                          getFormattedFuel(value.fuelOfCars), searchAlgo, number)

    def play(self):
        a = datetime.datetime.now()
        while not self.openList.empty():
            currentState = self.openList.get()
            if currentState.solution():
                b = datetime.datetime.now()
                self.timing = (b - a).microseconds / 1000000
                self.winner = currentState
                return
            marked = {}
            self.reOrder = False
            self.getRidOf = {}
            self.closedList[currentState.stringRep] = currentState
            if currentState.stringRep in self.openListTracker:
                del self.openListTracker[currentState.stringRep]
            self.newStates = []
            for i in range(0, 6):
                for j in range(0, 6):
                    if currentState.gameboard[i][j] not in marked:

                        marked[currentState.gameboard[i][j]] = True
                        coordinates = locateFrontAndBack(currentState.gameboard, i, j)
                        axis = coordinates[3][1]
                        steps = coordinates[3][0]
                        start = 1

                        if (axis == 'right' or axis == 'down') and steps != 0:
                            temp = deepcopy(currentState.gameboard)
                            heuristicCost = self.heuristic(temp)
                            costFromRoot = self.pathCostFunction(currentState)
                            while start <= currentState.fuelOfCars[currentState.gameboard[i][j]] and start <= steps:
                                message = ''
                                if axis == 'right':
                                    if temp[i][j + (start - 1)] == '.':
                                        break
                                    coordinates = locateFrontAndBack(temp, i, j + (start - 1))
                                    temp = moveRight(temp, coordinates[0], coordinates[1])
                                    message = currentState.gameboard[i][j] + ' ' + 'right' + ' ' + str(start)
                                else:
                                    if temp[i + (start - 1)][j] == '.':
                                        break
                                    coordinates = locateFrontAndBack(temp, i + (start - 1), j)
                                    temp = moveDown(temp, coordinates[0], coordinates[1])
                                    message = currentState.gameboard[i][j] + ' ' + 'down ' + ' ' + str(start)
                                self.checkAlgoAndBuildStates(currentState, i, j, start, temp, costFromRoot, heuristicCost,message)
                                start += 1
                        coordinates = locateFrontAndBack(currentState.gameboard, i, j)
                        axis = coordinates[2][1]
                        steps = coordinates[2][0]
                        start = 1
                        if (axis == 'left' or axis == 'up') and steps != 0:
                            temp = deepcopy(currentState.gameboard)
                            heuristicCost = self.heuristic(temp)
                            costFromRoot = self.pathCostFunction(currentState)
                            while start <= currentState.fuelOfCars[currentState.gameboard[i][j]] and start <= steps:
                                message = ''
                                if axis == 'left':
                                    if temp[i][j - (start - 1)] == '.':
                                        break
                                    coordinates = locateFrontAndBack(temp, i, j - (start - 1))
                                    temp = moveLeft(temp, coordinates[0], coordinates[1])
                                    message = currentState.gameboard[i][j] + ' ' + 'left ' + ' ' + str(start)
                                else:
                                    if temp[i - (start - 1)][j] == '.':
                                        break
                                    coordinates = locateFrontAndBack(temp, i - (start - 1), j)
                                    temp = moveUp(temp, coordinates[0], coordinates[1])
                                    message = currentState.gameboard[i][j] + ' ' + 'up   ' + ' ' + str(start)
                                self.checkAlgoAndBuildStates(currentState, i, j, start, temp, costFromRoot, heuristicCost,
                                                       message)

                                start += 1

            oldStates = []
            if self.reOrder:
                while not self.openList.empty():
                    oldState = self.openList.get()
                    if oldState.stringRep in self.getRidOf:
                        del self.openListTracker[oldState.stringRep]
                    else:
                        oldStates.append(oldState)
            for state in oldStates:
                self.openList.put(state)
            for state in self.newStates:
                self.openList.put(state)
                self.openListTracker[state.stringRep] = state.combinedCost
        b = datetime.datetime.now()
        self.timing = (b - a).seconds


def getFuel(gamestring):
    fuels = {}
    for car in range(0, 36):
        if gamestring[car] != '.' and gamestring[car] != ' ':
            if gamestring[car] not in fuels:
                fuels[gamestring[car]] = 100
    pos = 36
    while pos < len(gamestring):
        if gamestring[pos].isdigit():
            digitStart = pos
            x = digitStart
            while x < len(gamestring):
                if not gamestring[x].isdigit():
                    break
                x += 1
            currCar = gamestring[digitStart - 1]
            fuel = int(gamestring[digitStart:x])
            fuels[currCar] = fuel
            pos = x
        else:
            pos += 1
    return fuels


def locateFrontAndBack(container, yIndex, xIndex):
    car = container[yIndex][xIndex]
    orientation = ""
    if yIndex + 1 < len(container):
        currCar = container[yIndex + 1][xIndex]
        if currCar == car:
            orientation = 'vertical'

    if yIndex - 1 >= 0:
        currCar = container[yIndex - 1][xIndex]
        if currCar == car:
            orientation = 'vertical'

    if xIndex + 1 < len(container[yIndex]):
        currCar = container[yIndex][xIndex + 1]
        if currCar == car:
            orientation = 'horizontal'

    if xIndex - 1 >= 0:
        currCar = container[yIndex][xIndex - 1]
        if currCar == car:
            orientation = 'horizontal'
    head = (0, 0)
    tail = (0, 0)
    if orientation == 'vertical':
        start = yIndex
        while start < len(container) and container[start][xIndex] == car:
            start += 1
        tail = (start - 1, xIndex)
        start = yIndex
        while start >= 0 and container[start][xIndex] == car:
            start -= 1
        head = (start + 1, xIndex)
    else:
        start = xIndex
        while start < len(container[yIndex]) and container[yIndex][start] == car:
            start += 1
        tail = (yIndex, start - 1)
        start = xIndex
        while start >= 0 and container[yIndex][start] == car:
            start -= 1
        head = (yIndex, start + 1)
    length = 0
    directionA = ()
    directionB = ()
    if orientation == 'vertical':
        length = abs(head[0] - tail[0])
        startCar = head[0] - 1
        countMoves = 0
        while startCar >= 0 and container[startCar][xIndex] == '.':
            countMoves += 1
            startCar -= 1
        directionA = (countMoves, 'up')
        startCar = tail[0] + 1
        countMoves = 0
        while startCar < len(container) and container[startCar][xIndex] == '.':
            countMoves += 1
            startCar += 1
        directionB = (countMoves, 'down')

    else:
        length = abs(head[1] - tail[1])
        startCar = head[1] - 1
        countMoves = 0
        while startCar >= 0 and container[yIndex][startCar] == '.':
            countMoves += 1
            startCar -= 1
        directionA = (countMoves, 'left')
        startCar = tail[1] + 1
        countMoves = 0
        while startCar < len(container[yIndex]) and container[yIndex][startCar] == '.':
            countMoves += 1
            startCar += 1
        directionB = (countMoves, 'right')

    return head, tail, directionA, directionB


def moveRight(container, head, tail):
    state = deepcopy(container)
    state[tail[0]][tail[1] + 1] = state[tail[0]][tail[1]]
    state[head[0]][head[1]] = '.'
    if tail[0] == 2 and (tail[1] + 1) == 5 and state[tail[0]][tail[1] + 1] != 'A':
        for x in range(head[1], 6):
            state[tail[0]][x] = '.'
    return state


def moveLeft(container, head, tail):
    state = deepcopy(container)
    state[head[0]][head[1] - 1] = state[head[0]][head[1]]
    state[tail[0]][tail[1]] = '.'
    return state


# increases y
def moveDown(container, head, tail):
    state = deepcopy(container)
    state[tail[0] + 1][tail[1]] = state[tail[0]][tail[1]]
    state[head[0]][head[1]] = '.'
    return state


# decreases y
def moveUp(container, head, tail):
    state = deepcopy(container)
    state[head[0] - 1][head[1]] = state[head[0]][head[1]]
    state[tail[0]][tail[1]] = '.'
    return state


def prettyPrint(container):
    game = ""
    for row in container:
        game += "".join(row)
        game += '\n'
    return game


def getFormattedFuel(fuels):
    strRep = ''
    for car in fuels:
        if not (fuels[car] == 100):
            strRep += ' ' + car + str(fuels[car])
    return strRep


if __name__ == '__main__':
    game = ".BBCCC..EEKLAAIJKLH.IJFFHGGG.M.....M K6 M0"
    newGame = gamePlayer(PriorityQueue(), game, getFuel(game), noHeuristic, pathFromPatent, ucs=True, gbfs=False,
                         algoA=False)
    newGame.play()
    newGame.writeSearchFile('ucs', 3)
    newGame.writeToSolution('ucs', 3)
