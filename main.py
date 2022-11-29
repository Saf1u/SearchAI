import datetime
import os
from copy import deepcopy
from queue import PriorityQueue


# for ucs h(n)
def noHeuristic(x, **kwargs):
    return 0


# for gbfs g(n)
def noCostFromParent(x):
    return 0


def numberOfPositionsToGoal(state, **kwargs):
    fuels = kwargs.get('fuel', None)
    ambulanceFuel = fuels['A']
    x = 0
    for i in range(0, 6):
        if state[2][i] == 'A':
            x = i + 1
            break

    count = 5 - x
    if count == 0:
        return 0
    if ambulanceFuel >= count:
        return 1
    else:
        return float('-inf')


def yCanLeave(state, **kwargs):
    horizontalBlocks = numberOfBlockingVehiclesHeuristic(state)
    if horizontalBlocks == 0:
        return 0
    if state[2][5] == state[1][5] or state[2][5] == state[3][5]:
        return horizontalBlocks - 1
    else:
        return horizontalBlocks


def numberOfBlockingVehiclesHeuristic(state, **kwargs):
    been = {}
    count = 0
    x = 0
    for i in range(0, 6):
        if state[2][i] == 'A':
            x = i + 2
            break
    for i in range(x, 6):
        if state[2][i] != '.':
            if state[2][i] not in been:
                count += 1
                been[state[2][i]] = True
    return count


def numberOfBlockingVehiclesHeuristicScaled(state, **kwargs):
    # change this to probably mess with admissibility(higher constant less optimism)
    return 5 * numberOfBlockingVehiclesHeuristic(state)


def numberOfBlockingPositions(state, **kwargs):
    count = 0
    x = 0
    for i in range(0, 6):
        if state[2][i] == 'A':
            x = i + 2
            break
    for i in range(x, 6):
        if state[2][i] != '.':
            # if state[2][i]:
            count += 1
    return count


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
    with open("./output/" + name + "-search-" + str(number) + ".txt", "a+") as myfile:
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
        self.initialConfig = init
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
            if self.closedList[newState.stringRep].combinedCost <= newState.combinedCost:
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
            with open("./output/" + name + "-SOL-" + str(number) + ".txt", "a+") as myFile:
                myFile.write("no solution")
                myFile.write("--------------------------------------------------------------------------------")
                myFile.write('\n')
                myFile.write("Initial board configuration: " + self.initialConfig.stringRep)
                myFile.write('\n')
                myFile.write('\n')
                myFile.write(prettyPrint(self.initialConfig.gameboard))
                myFile.write('Car fuel available: ' + self.startingFuel)
                myFile.write('\n')
                myFile.write('\n')
                myFile.write('no solution found')
                myFile.write('\n')
                myFile.write('\n')
                myFile.write('Runtime:' + str(self.timing) + 'seconds')
                myFile.write('\n')
                myFile.write('\n')
        else:
            searchPath = []
            win = self.winner
            count = 0
            while win is not None:
                searchPath.append(win)
                win = win.parent

            searchPath.reverse()
            with open("./output/" + name + "-SOL-" + str(number) + ".txt", "a+") as myFile:
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
                if len(searchPath) > 1:
                    myFile.write(prettyPrint(searchPath[len(searchPath) - 1].gameboard))
                else:
                    if len(searchPath) == 1:
                        myFile.write(prettyPrint(searchPath[0].gameboard))
                if not os.path.exists('./output/analysis.csv'):
                    with open("./output/" + "analysis" + ".csv", "a+") as analysisFile:
                        analysisFile.write(
                            "Puzzle Number,Algorithm,Heuristic,Length of the solution,Length of The search path,Execution Time (in seconds)")
                        analysisFile.write('\n')
                with open("./output/" + "analysis" + ".csv", "a+") as analysisFile:
                    algo = name
                    parts = name.split('-')
                    if len(parts) < 2:
                        analysisFile.write(str(i) + ",UCS" + ",N/A," + str(len(searchPath) - 1) + "," + str(
                            len(self.closedList)) + ',' + str(self.timing))
                    else:
                        analysisFile.write(
                            str(i) + "," + parts[0] + "," + parts[1] + "," + str(len(searchPath) - 1) + "," + str(
                                len(self.closedList)) + ',' + str(self.timing))
                    analysisFile.write('\n')

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
                            heuristicCost = self.heuristic(temp, fuel=currentState.fuelOfCars)
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
                                self.checkAlgoAndBuildStates(currentState, i, j, start, temp, costFromRoot,
                                                             heuristicCost, message)
                                start += 1
                        coordinates = locateFrontAndBack(currentState.gameboard, i, j)
                        axis = coordinates[2][1]
                        steps = coordinates[2][0]
                        start = 1
                        if (axis == 'left' or axis == 'up') and steps != 0:
                            temp = deepcopy(currentState.gameboard)
                            heuristicCost = self.heuristic(temp, fuel=currentState.fuelOfCars)
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
                                self.checkAlgoAndBuildStates(currentState, i, j, start, temp, costFromRoot,
                                                             heuristicCost,
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
        self.timing = (b - a).microseconds / 1000000


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


def readInput(filename):
    puzzles = []
    with open(filename) as myfile:
        for line in myfile:
            if line.strip():
                # print(line)
                if line[0] != '#':
                    puzzles.append(line.strip())
    return puzzles


if __name__ == '__main__':
    games = readInput('sample-input.txt')
    heurestics = {"h1": numberOfBlockingVehiclesHeuristic, "h2": numberOfBlockingVehiclesHeuristicScaled,
                  "h3": numberOfBlockingPositions, "h4": yCanLeave}

    i = 1
    for game in games:
        # ucs
        newGame = gamePlayer(PriorityQueue(), game, getFuel(game), noHeuristic, pathFromPatent,
                             ucs=True, gbfs=False,
                             algoA=False)
        newGame.play()
        newGame.writeSearchFile('ucs', i)
        newGame.writeToSolution('ucs', i)
        for heurestic in heurestics:
            # gbfs and algoA
            newGame = gamePlayer(PriorityQueue(), game, getFuel(game), heurestics[heurestic], noCostFromParent,
                                 ucs=False, gbfs=True,
                                 algoA=False)
            newGame.play()
            newGame.writeSearchFile('gbfs-' + str(heurestic), i)
            newGame.writeToSolution('gbfs-' + str(heurestic), i)

            newGame = gamePlayer(PriorityQueue(), game, getFuel(game), heurestics[heurestic], pathFromPatent,
                                 ucs=False, gbfs=False,
                                 algoA=True)
            newGame.play()
            newGame.writeSearchFile('AlgoA|AlgoA*-' + str(heurestic), i)
            newGame.writeToSolution('AlgoA|AlgoA*-' + str(heurestic), i)
        i += 1
        print('puzzle:' + str(i) + ' done')
