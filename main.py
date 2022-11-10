from copy import deepcopy
from queue import PriorityQueue


class stateSpace:
    # gameState =[["." for x in range(6)] for y in range(6)]
    # costs={}
    # currentCost=0
    def __init__(self, gameboard, fuelOfCars, costOfMove, carMovedWithDirection, parent):
        self.gameboard = gameboard
        self.fuelOfCars = fuelOfCars
        self.costOfMove = costOfMove
        self.carMovedWithDirection = carMovedWithDirection
        self.stringRep = ''.join([item for innerlist in gameboard for item in innerlist])
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


class gamePlayer:
    def __init__(self, gameString, initalFuel):
        gameState = [["." for x in range(6)] for y in range(6)]
        for i in range(0, 6):
            for j in range(0, 6):
                gameState[i][j] = gameString[j + (6 * i)]
        init = stateSpace(gameState, initalFuel, 0, "none", None)
        self.openList = PriorityQueue()
        self.openList.put(init)
        self.openListTracker = {init.stringRep: init.costOfMove}
        self.closedList = {}

    def play(self):
        while not self.openList.empty():
            currentState = self.openList.get()
            if currentState.solution():
                return currentState
            marked = {}
            reOrder = False
            getRidOf = {}
            self.closedList[currentState.stringRep] = currentState
            if currentState.stringRep in self.openListTracker:
                del self.openListTracker[currentState.stringRep]
            newStates = []
            for i in range(0, 6):
                for j in range(0, 6):
                    if currentState.gameboard[i][j] not in marked:

                        marked[currentState.gameboard[i][j]] = True
                        coordinates = locateFrontAndBack(currentState.gameboard, i, j)
                        axis = coordinates[3][1]
                        steps = coordinates[3][0]

                        if (axis == 'right' or axis == 'down') and steps != 0:
                            start = 1
                            temp = deepcopy(currentState.gameboard)
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
                                    message = currentState.gameboard[i][j] + ' ' + 'down' + ' ' + str(start)
                                fuelCopy = currentState.fuelOfCars.copy()
                                fuelCopy[currentState.gameboard[i][j]] -= start
                                newState = stateSpace(temp, fuelCopy, 1 + currentState.costOfMove, message,
                                                      currentState)
                                start += 1
                                if newState.stringRep not in self.closedList:
                                    if newState.stringRep in self.openListTracker and self.openListTracker[
                                        newState.stringRep] > newState.costOfMove:
                                        newStates.append(newState)
                                        reOrder = True
                                        getRidOf[newState.stringRep] = True
                                    elif newState.stringRep not in self.openListTracker:
                                        newStates.append(newState)
                        coordinates = locateFrontAndBack(currentState.gameboard, i, j)
                        axis = coordinates[2][1]
                        steps = coordinates[2][0]

                        if (axis == 'left' or axis == 'up') and steps != 0:
                            start = 1
                            temp = deepcopy(currentState.gameboard)
                            while start <= currentState.fuelOfCars[currentState.gameboard[i][j]] and start <= steps:
                                message = ''
                                if axis == 'left':
                                    if temp[i][j - (start - 1)] == '.':
                                        break
                                    coordinates = locateFrontAndBack(temp, i, j - (start - 1))
                                    temp = moveLeft(temp, coordinates[0], coordinates[1])
                                    message = currentState.gameboard[i][j] + ' ' + 'left' + ' ' + str(start)
                                else:
                                    if temp[i - (start - 1)][j] == '.':
                                        break
                                    coordinates = locateFrontAndBack(temp, i - (start - 1), j)
                                    temp = moveUp(temp, coordinates[0], coordinates[1])
                                    message = currentState.gameboard[i][j] + ' ' + 'up' + ' ' + str(start)
                                fuelCopy = currentState.fuelOfCars.copy()
                                fuelCopy[currentState.gameboard[i][j]] -= start
                                newState = stateSpace(temp, fuelCopy, 1 + currentState.costOfMove, message,
                                                      currentState)
                                start += 1
                                if newState.stringRep not in self.closedList:
                                    if newState.stringRep in self.openListTracker and self.openListTracker[
                                        newState.stringRep] > newState.costOfMove:
                                        newStates.append(newState)
                                        prettyPrint(newState.gameboard)
                                        reOrder = True
                                        getRidOf[newState.stringRep] = True
                                    elif newState.stringRep not in self.openListTracker:
                                        newStates.append(newState)

            oldStates = []
            if reOrder:
                while not self.openList.empty():
                    oldState = self.openList.get()
                    if oldState.stringRep in getRidOf:
                        del self.openListTracker[oldState.stringRep]
                    else:
                        oldStates.append(oldState)
            for state in oldStates:
                self.openList.put(state)
            for state in newStates:
                self.openList.put(state)
                self.openListTracker[state.stringRep] = state.costOfMove
        return None


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


# def move(container,index,count,direction):

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


def writeToSearch(totalCost, searchCost, heurisitcCost, board, fuels):
    res = str(totalCost) + ' ' + ' ' + str(searchCost) + ' ' + str(heurisitcCost) + ' ' + board + fuels + '\n'
    with open("search-path.txt", "a") as myfile:
        myfile.write(res)


def prettyPrint(container):
    for row in container:
        print(row)
        print()


def printFuel(fuels):
    strRep = ''
    for car in fuels:
        if not (fuels[car] == 100):
            strRep += ' ' + car + str(fuels[car])
    return strRep


if __name__ == '__main__':
    game = "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH..."
    # "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH..."
    # game="IIB...C.BHHHC.AAD.....D.EEGGGF.....F"
    # game ="C.B...C.BHHHAADD........EEGGGF.....F"
    # game  ="...GF...BGF.AABCF....CDD...C....EE.."
    newGame = gamePlayer(game, initalFuel=getFuel(game))
    win = newGame.play()
    for k,value in newGame.closedList.items():
        writeToSearch(value.costOfMove, value.costOfMove, 0, value.stringRep,
                  printFuel(value.fuelOfCars))
    # fuel = 0
    # count = 0
    # while not win == None:
    #     # prettyPrint(win.gameboard)
    #     print('-------------')
    #     print(win.carMovedWithDirection)
    #     win = win.parent
    #     count += 1
    # count -= 1
    # print(count)
    # print(fuel)
