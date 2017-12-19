# chomp.py - script to investigate the game of chomp.
# the game is played on a 3 row x 4 column bar of chocolate
# players take turns to bite a rectangular region out of the bar, from the
# lower right corner. The upper left corner is poisoned, so the player who
# eats the last square loses.
import numpy as np
import csv
from copy import deepcopy
import matplotlib.pyplot as plt


class bar(object):
    ''' A bar of chocolate is the playing surface for chomp.

        The internal data structure used is a numpy array with rows and columns
        as in the bar. Cells are numbered from zero in reading-order
        (left to right then down). The show() method displays a graphical
        version of the board with numbered cells.

        The eat() method is the primary gameplay function. You select a single
        cell and all the cells to the right and below are removed.
        Corresponding cells which are eaten are labelled in the allPosition
        array.

        All possible positions can be enumerated by the enum() method.

    '''
    def __init__(self, rows=3, cols=4):
        self.rows = rows
        self.cols = cols
        self.eaten = np.zeros([rows, cols], dtype=int)  # zero = not yet eaten
        self.allPositions = self.enum()
        # self.allPositions = self.getAllPositionsFromCSV()
        self.finished = False  # game over
        self.boxes = self.getBoxes()
        self.gamesPlayed = 0
        self.gamesWon = 0

    def resetEaten(self):
        self.eaten = np.zeros([self.rows, self.cols], dtype=int)
        # zero = not yet eaten

    def enum(self):
        """ Enumerates all possible board positions

        Internally represents boards as a list with cols elements
        and maximum value rows.
        Example: on this board, X's are uneaten squares
        -sum the X's to get the board ID.

            X X X 0
            X X 0 0
            0 0 0 0
            - - - -
            2 2 1 0

        Returns the list of possible boards using the data structure
        used in the remainder of the program"""
#        raise DeprecationWarning('Function is Deprecated, use self.enum')
        rows = self.rows
        cols = self.cols
        fullList = []
        current = np.zeros([cols, 1], dtype=int)
        q = deepcopy(current.T)
        fullList.append(q)
        check = -1  # index of position to first look at
        while current[0] <= rows:  # loop until higher number than rows
            if current[check] == current[check-1]:  # if pair are the same
                if check-1 != -1*cols:  # and this isn't the last pair
                    check -= 1  # compare a pair higher
                else:
                    current[0] += 1
                    current[1:] = 0
                    check = -1
                    q = deepcopy(current.T)
                    fullList.append(q)
            else:  # current pair are not the same
                if current[check] <= current[check-1]-1:  # rollover condition
                    current[check] += 1
                    if check != -1:
                        current[check+1:] = 0  # set end digits to zero
                else:  # no rollover of digits
                    current[check] += 1
                q = deepcopy(current.T)
                fullList.append(q)
                check = -1
        check = -1

        f = fullList[:-1]  # last element is not valid
        boolRep = np.zeros([rows*cols, len(f)])  # boolean representation
        for j, desc in enumerate(f):
            desc = np.squeeze(desc)
            for i in range(cols):
                boolRep[i::cols, j] = np.concatenate(
                        (np.zeros([desc[i]]), np.ones([rows-desc[i]])))
        return boolRep.T.astype('bool')

    def convertDescriptionToBoolean(self, desc):
        '''Converts a description of a board, like [3,3,2,0] to a boolean
        representation, [0,0,0,1,0,0,0,1,0,0,1,1]'''
        cols = self.cols
        rows = self.rows
        boolRep = np.zeros([rows*cols])  # boolean representation
        desc = np.squeeze(desc)
        for i in range(cols):
            boolRep[i::cols] = np.concatenate(
                (np.zeros(desc[i]), np.ones([rows-desc[i]])))
        return boolRep.astype('bool')

    def convertBooleanToDescription(self, boolRep):
        '''Converts a boolean representation like [0,0,0,1,0,0,0,1,0,0,1,1]
        into a description like [3,3,2,0]'''
        return np.sum(np.invert(boolRep.reshape(3, 4)).astype('int'), 0)

    def getAllPositionsFromCSV(self):
        '''Returns a boolean array of board positions -
        elements true if eaten'''
        with open('chomp.csv', 'r') as csvfile:
            myreader = csv.reader(csvfile, delimiter=',')
            boardPositions = np.zeros([35, 12])
            next(myreader)
            for i, row in enumerate(myreader):
                try:
                    boardPositions[i, :] = row[2:-1]
                except ValueError:
                    pass
        return boardPositions.astype('bool')

    def recognisePosition(self):
        '''Returns the index of the position which the current board is in'''
        boolRepeat = (np.reshape(self.eaten, [1, 12]) *
                      np.ones([35, 1])).astype('bool')
        boardPositionID = np.argwhere(np.all
                                      (self.allPositions == boolRepeat, 1))
        return int(boardPositionID)

    def show(self):
        """Prints the number positions"""
        for i in range(self.rows):
            print('|', end='')
            for j in range(self.cols):
                print('{:2}|'.format(j+i*self.cols), end='')
            print('')

    def eat(self, n, player):
        """"Sets the eaten property of the bar, from some coordinate position
        specified by n"""
       # print('Player {} chose to eat square {}'.format(player, n))
        if n == 0:
           # print('square 0 is poisoned so Player {} loses'.format(player))
            self.eaten = np.zeros(self.rows,self.cols)
        else:
            topLeftPosition = self.positionNumberToCoords(n)
            if self.eaten[topLeftPosition] == 0:
                # now eat that square and all other
                # nonzero squares to the right and below
                filt = np.zeros([self.rows, self.cols], dtype=bool)
                filt[topLeftPosition[0]:, topLeftPosition[1]:] = True
                squaresAlreadyEatenFilter = self.eaten == 0
                squaresToEat = np.logical_and(squaresAlreadyEatenFilter, filt)
                self.eaten[squaresToEat] = player
            else:
                pass
            if len(np.nonzero(self.eaten)) == (self.rows*self.cols)-1:
                #   print('Player {} wins'.format(player))
                self.finished = True
                #  print('After eating, my state is {}'
                # .format(self.recognisePosition()))
                #  print('\n')
        return self.eaten

    def positionNumberToCoords(self, n):
        '''Converts between a position number as reported by self.show()
        and row and column identifiers'''
        rowID = n//self.cols
        colID = n % self.cols
        return (rowID, colID)

    def pickRandomAvailableSquareToEat(self):
        '''Gets all available squares and chooses one at random
        choosing a square eats from the lower right corner up to and
        including that square'''
        allMoves = np.arange(0, 12)
        boardID = self.recognisePosition()
        availableMoves = allMoves[np.invert(self.allPositions[boardID, :])]
        availableMoves = availableMoves[availableMoves != 0]
        # remove the chance of zeroing
        if len(availableMoves) == 0:
            move = -1  # resign
        else:
            move = int(np.random.choice(availableMoves, 1))
        return move

    def demo(self):
        '''makes player 1 eat the bottom 2x2 square'''
        self.eaten[1:3, 2:4] = 1

    def getBoxes(self):
        listOfBoxes = []
        for boolean in self.allPositions:
            description = self.convertBooleanToDescription(boolean)
            listOfBoxes.append(Box(description, self.rows, self.cols))
        return listOfBoxes

    def record(self):
        print('PC has won {} of {} games - {:.0f} percent'.format(
            self.gamesWon,
            self.gamesPlayed,
            (self.gamesWon/self.gamesPlayed)*100))
        return self.gamesWon/self.gamesPlayed

    def playHuman(self):
        '''Play the game of Chomp against the human - PC starts (player 1)

        Strategy: Starts with a random move, then draw moves thereafter.
        Log moves and boxes as we go
        If we win, replenish the boxes we used
        If we lose, replenish the boxes the human used

        '''
        pcMoveList = []
        humanMoveList = []
        positionList = []
        self.resetEaten()  # reset which boxes have been eaten
        self.gamesPlayed += 1

        current = self.recognisePosition()
        positionList.append(current)
        move = self.boxes[current].draw()
        self.eat(move, 1)
        print('After eating, my state is {}'
              .format(self.recognisePosition()))
        print(self.eaten)
        pcMoveList.append(move)
        player1In = False  # in the loop, it's the human's turn
        winner = -1  # don't know the winner yet
        self.finished = False
        while self.finished is False:
            if player1In:
                current = self.recognisePosition()
                positionList.append(current)
                move = self.boxes[current].draw()
                move = int(move)
                if move == -1:
                    self.finished = True
                    winner = 2  # player 1 resigned
                    print('Player 1 Resigned')
                else:
                    self.eat(move, 1)
                    pcMoveList.append(move)
                    player1In = False
            else:
                current = self.recognisePosition()
                positionList.append(current)
                self.show()
                print(self.eaten)
                move = input(
                        'Which square would you like to go in? '
                        '(-1 to resign), blank for random ')
                try:
                    move = int(move)
                except ValueError:
                    move = -2  # set to -2 if left blank
                if move == -1:
                    move = int(move)
                    self.finished = True
                    winner = 1  # player 2 resigned
                    print('Player 2 Resigned')
                    player1In = True  # do I need this?
                elif move == -2:
                    move = self.pickRandomAvailableSquareToEat()
                    print('Player 2 Randomly chose {}'.format(move))
                    if move != -1:  # any move but resignation
                        self.eat(move, 2)
                        humanMoveList.append(move)
                        player1In = True
                    else:  # resignation
                        self.finished = True
                        winner = 1  # player 2 resigned
                        print('Player 2 Resigned')
                        player1In = True  # not sure if I need this
                else:
                    move = int(move)
                    if move == 0:
                        print('Player 2 ate the poison')
                        self.finished = True
                        winner = 1
                        player1In = True
                    else:
                        self.eat(move, 2)
                        humanMoveList.append(move)
                        player1In = True
        print('Player {} won'.format(winner))
        print('Position List = {}'.format(positionList))
        print('PC Moves = {}'.format(pcMoveList))
        print('Human Moves = {}'.format(humanMoveList))
        if winner == 1:  # the computer wins
            winPositionList = positionList[::2]
            winMoveList = pcMoveList
            self.gamesWon += 1
        else:
            winPositionList = positionList[1::2]
            winMoveList = humanMoveList
        for move, position in zip(winMoveList, winPositionList):
                print('Boosting move {} in box {}'.format(move, position))
                self.boxes[position].replenish(move)
        return winner

    def playRandomOpponent(self):
        '''Play the game of Chomp against a random opponent

        Strategy: draws moves from the distribution
        Log moves and boxes as we go
        If we win, replenish the boxes we used
        If we lose, replenish the boxes the human used

        '''
        pcMoveList = []
        humanMoveList = []
        positionList = []
        self.resetEaten()  # reset which boxes have been eaten
        self.gamesPlayed += 1

        current = self.recognisePosition()
        positionList.append(current)
        move = self.boxes[current].draw()
        self.eat(move, 1)
        pcMoveList.append(move)
        player1In = False  # in the loop, it's the human's turn
        winner = -1  # don't know the winner yet
        self.finished = False
        while self.finished is False:
            if player1In:
                current = self.recognisePosition()
                positionList.append(current)
                move = self.boxes[current].draw()
                move = int(move)
                if move == -1:
                    self.finished = True
                    winner = 2  # player 1 resigned
                else:
                    self.eat(move, 1)
                    pcMoveList.append(move)
                    player1In = False
            else:
                current = self.recognisePosition()
                positionList.append(current)
                move = self.pickRandomAvailableSquareToEat()
                if move != -1:  # any move but resignation
                    self.eat(move, 2)
                    humanMoveList.append(move)
                    player1In = True
                else:  # resignation
                    self.finished = True
                    winner = 1  # player 2 resigned
                    player1In = True  # not sure if I need this
        if winner == 1:  # the computer wins
            winPositionList = positionList[::2]
            winMoveList = pcMoveList
            self.gamesWon += 1
        else:
            winPositionList = positionList[1::2]
            winMoveList = humanMoveList
        for move, position in zip(winMoveList, winPositionList):
                self.boxes[position].replenish(move)
        return winner


class Box(object):
    '''Each bar has as many boxes as possible game states - possible moves are
    drawn from the box

    Box methods:
        init - initialise contents depending on description
        repr - prints the dictionary
        populate - initialise internal dictionary with the right number moves
        distribution - calculates the number of beads to start in each box
        draw - return a move or -1 for resign
        replenish - add beads to winning moves
    '''

    def __init__(self, desc, rows, cols):
        self.desc = np.squeeze(desc)  # to ensure a single dimensional array
        self.cols = cols
        self.rows = rows
        self.moveDict = {}  # create an empty dictionary to store move/beads
        self.populate()  # populate this dictionary with moves

    def __repr__(self):
        return(repr(self.moveDict))

    def populate(self):
        '''Populates the dictionary of available moves'''
        desc = np.squeeze(self.desc)
        boolRep = np.zeros([self.rows*self.cols])  # 1 for eaten, 0 for not
        for i in range(self.cols):
            boolRep[i::self.cols] = np.concatenate(
                    (np.zeros([desc[i]]), np.ones([self.rows-desc[i]])))
        boolRep = (1-boolRep).astype('bool')
        allMoves = np.arange(self.rows*self.cols)
        availableMoves = allMoves[boolRep]
        numberOfBeadsEach = self.distribution()
        for move in availableMoves:
            self.moveDict[move] = numberOfBeadsEach
        try:
            self.moveDict.pop(0)  # force remove the 0 move which loses
        except KeyError:  # this occurs when trying to populate the empty board
            pass

    def distribution(self):
        '''Controls how many initial beads get placed in each box,
        depending on how far into the game they are

        This is governed by the sum of the description (how many squares are
        left over and maxBeads and minBeads)
        '''
        maxBeads = 6
        minBeads = 2
        maxSum = self.rows * self.cols
        totalSquaresLeft = np.sum(self.desc)
        return np.ceil(np.interp(
                totalSquaresLeft, [0, maxSum],
                [minBeads, maxBeads])).astype(int)

    def draw(self):
        '''Draws a move from all possible moves available from this box'''
        moveList = []
        for k in self.moveDict:
            for i in range(self.moveDict[k]):
                moveList.append(k)  # add the move this many times
        try:  # choose one from the dictionary
            selected = int(np.random.choice(moveList, 1))
            self.moveDict[selected] -= 1  # decrement
        except ValueError:  # there are no possible moves
            selected = -1  # resign as no possible moves
            self.populate()  # reset to original
        return selected

    def replenish(self,winningMove):
        '''Adds to the dictionary the list of moves which won the game'''
        bounty = 3;  # add this to each winning position
        self.moveDict[winningMove] += bounty


if __name__ == '__main__':
#    b = bar()
#    b.show()
#    for i in range(12):
#        print('i= {} '.format(i), end='')
#        print(b.positionNumberToCoords(i))
#
#    print('\n\n\n')
#
#    b.eat(2, player=1)
#    b.eat(5, 2)
#    b.eat(1, 1)


    # enough demos, let's play some games
    if False:
        p1Wins = 0;
        nGames = 100;
        for i in range(nGames):
            d = bar()
            player = 1
            player1In=True
            while d.finished == False:
                if player1In:
                    player = 1
                else:
                    player = 2
                sq2Eat = int(d.pickRandomAvailableSquareToEat())
                d.eat(sq2Eat,player)
                player1In = not(player1In)
            p1Wins += player-1
        print('Player 1 won {} times out of {} games'.format(p1Wins,nGames))
## with entirely random play, there seems to be no advantage to going first
#
#
#    print('\n\n\n')
#    # game against a human opponent
#    d = bar()
#    player = 1
#    player1In=True
#    while d.finished == False:
#        if player1In: # PC always goes first
#            sq2Eat = int(d.pickRandomAvailableSquareToEat())
#            d.eat(sq2Eat, 1)
#            player1In = False
#        else:
#            player = 2
#            d.show()
#            print(d.eaten)
#            q = input('Which square would you like to go in?')
#            q = int(q)
#            d.eat(q, 2)
#            player1In = True

#    if False:
#        d = bar()
#        go = True
#        gameIdx = 0
#        gameList = []
#        recordList = []
#        while go:
#            d.playHuman()
#            gameList.append(gameIdx)
#            recordList.append(d.record())
#            gameIdx += 1
#            raw = input('Hit Enter to go again, type anything to quit: ')
#            if len(raw) != 0:
#                go = False
#        plt.figure(1)
#        plt.plot(gameList, recordList, 'k-')
#        plt.show()

    e = bar()
    gameIdx = 0
    gameList = []
    recordList = []
    for i in range(10000):  # simulate 10000 games against random opposition
        e.playRandomOpponent()
        gameList.append(gameIdx)
        recordList.append(e.record())
        gameIdx += 1
    plt.figure(2)
    plt.plot(gameList, recordList, 'k-')
    plt.show()


