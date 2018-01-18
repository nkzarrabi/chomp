"""Investigative Script on the game of Chomp"""
import csv
import pickle
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.filedialog import askopenfilename


class Bar(object):
    """ A bar of chocolate is the playing surface for the game of chomp.
    Players take turns to bite a rectangular region out of the bar, from the
    lower right corner. The upper left corner is poisoned, so the player who
    eats the last square loses.

    Data Structures:
        The internal data structure used to represent the Bar is a
        rectangular numpy array. Squares are numbered from zero in
        reading-order (left to right then down). In the self.eaten array,
        a zero indicates a square is not yet eaten, and other numbers
        indicate the player who ate the square.

        Finitely many game states exist. These are represented in two
        different ways - a 'description', which is a 1D array containing
        the number of uneaten squares per column, e.g. [3,2,2,0] - this
        uniquely describes the bar due to the game mechanic. The second
        method is a 'boolean representation' - this is a 1D array of
        boolean variables, of length rows*columns. The value is False if
        the corresponding square (when read out in reading order) is
        available to eat.

        The probability of eating to a particular square is governed by
        'boxes' representing each potential board state.

    Methods:
        resetEaten() : Resets array of eaten squares
        enumerateStates() : Creates a list of possible board states
        convertDescriptionToBoolean(desc) : Converts a shorthand
                                            description to a boolean
                                            representation
        convertBooleanToDescription(boolRep) : Converts from boolean
                                               representation to shorthand
                                               description
        show() : Displays a graphical bar with numbered cells.
        getallStatesFromCSV() : DEPRECATED - receive all states of 3x4
                                bar from a CSV file
        recogniseState() : Find the index of self.allStates which
                              corresponds with the current bar state
        show() : Prints a graphical bar with numbered cells to the screen.
        eat(n, player) : Eats square n and all squares lower and to the right.
                         player argument is to tag squares (for further
                         graphics enhancements)
        positionNumberToCoords(n) : Returns the coordinates (row, col) from
                                    square number n.
        pickRandomAvailableSquareToEat() : Returns the number of an available
                                           square to eat.
        getBoxes() : Generate a list of Box objects for the bar
        record() : Print the number of games won and played and return the
                   percentage.
        save(filename) : Saves the current box array to a file 'filename'
        load(filename) : Loads a box array from the file 'filename'
        play(opponent) : Play chomp - opponent = 'human'|'random'|'intelligent'


    Example: Generate a 3x4 bar, Let Players 1 and 2 eat a bit, then show the
             different representations

        In: bar = Bar(3,4)

        In: bar.show()
            | 0| 1| 2| 3|
            | 4| 5| 6| 7|
            | 8| 9|10|11|

        In: bar.eat(n=3, player=1)
        Out: array([[0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 0, 0, 1]])

        In: bar.eat(9, 2)
        Out: array([[0, 0, 0, 1],
                    [0, 0, 0, 1],
                    [0, 2, 2, 1]])

        In: bar.recogniseState()
        Out: 22

        In: b.allStates[22]
        Out: array([False, False, False,  True,
                    False, False, False,  True,
                    False, True,  True,   True], dtype=bool)

        In: b.convertBooleanToDescription(b.allStates[22])
        Out: array([3, 2, 2, 0])

    """
    def __init__(self, rows=3, cols=4, bounty=3, maxBeads=2, minBeads=1):
        self.rows = rows
        self.cols = cols
        self.eaten = np.zeros([rows, cols], dtype=int)
        self.allStates = self.enumerateStates()
        self.finished = False  # game over if this is True
        self.boxes = self.getBoxes(bounty, maxBeads, minBeads)
        self.gamesPlayed = 0
        self.gamesWon = 0
        self.nextStateList = self.produceListNextState()

    def resetEaten(self):
        """Resets the self.eaten array to all zeros"""
        self.eaten = np.zeros([self.rows, self.cols], dtype=int)

    def enumerateStates(self):
        """ Enumerates all possible bar states

        Internally represents bars as a list with self.cols elements
        where the maximum value of each element is self.rows.
        Example: on this bar, X's are uneaten squares
        -sum the X's to get the bar ID.

            X X X 0
            X X 0 0
            0 0 0 0
            - - - -
            2 2 1 0

        Returns the list of possible bars in a boolean representation
        """
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
        """Converts a description of a bar, like [3,3,2,0] to a boolean
        representation, [0,0,0,1,0,0,0,1,0,0,1,1]
        """
        cols = self.cols
        rows = self.rows
        boolRep = np.zeros([rows*cols])  # boolean representation
        desc = np.squeeze(desc)
        for i in range(cols):
            boolRep[i::cols] = np.concatenate(
                (np.zeros(desc[i]), np.ones([rows-desc[i]])))
        return boolRep.astype('bool')

    def convertBooleanToDescription(self, boolRep):
        """Converts a boolean representation like [0,0,0,1,0,0,0,1,0,0,1,1]
        into a description like [3,3,2,0]
        """
        return np.sum(np.invert(boolRep.reshape(
            self.rows, self.cols)).astype('int'), 0)

    def getallStatesFromCSV(self):
        """Returns a boolean array of bar states -
        elements true if eaten
        """
        raise DeprecationWarning('This only works for bar 3x4')
        with open('chomp.csv', 'r') as csvfile:
            myreader = csv.reader(csvfile, delimiter=',')
            barStates = np.zeros([len(self.allStates), 12])
            next(myreader)
            for i, row in enumerate(myreader):
                try:
                    barStates[i, :] = row[2:-1]
                except ValueError:
                    pass
        return barStates.astype('bool')

    def recogniseState(self):
        """Returns the index of the state which the current bar is in"""

        boolRepeat = (np.reshape(self.eaten, [1, self.cols*self.rows]) *
                      np.ones([len(self.allStates), 1])).astype('bool')
        barPositionID = np.argwhere(np.all
                                    (self.allStates == boolRepeat, 1))
        return int(barPositionID)

    def show(self):
        """Prints a visual representation of the bar with numbers on squares"""
        print('Square Numbers')
        for i in range(self.rows):
            print('|', end='')
            for j in range(self.cols):
                print('{:2}|'.format(j+i*self.cols), end='')
            print('')
        print('')

    def showUnicode(self):
        """Draws a bar on the screen using unicode block elements"""
        print('Current squares which have been eaten')
        for i in range(self.rows):
            for j in range(self.cols):
                if self.eaten[i, j] == 0:
                    print('██', end='')
                else:
                    print('░░', end='')
            print('')
        print('')

    def showEaten(self):
        """Prints a representation of which parts of the bar have been eaten"""
        print('Current squares which have been eaten')
        for i in range(self.rows):
            print('|', end='')
            for j in range(self.cols):
                print('{:2}|'.format(self.eaten[i, j]), end='')
            print('')
        print('')

    def eat(self, n, player):
        """"Sets the eaten property of the bar, from some coordinate position
        specified by n
        """
        # print('Player {} chose to eat square {}'.format(player, n))
        if n == 0:
            # print('square 0 is poisoned so Player {} loses'.format(player))
            self.eaten = np.zeros(self.rows, self.cols)
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
                # .format(self.recogniseState()))
                #  print('\n')
        return self.eaten

    def positionNumberToCoords(self, n):
        """Converts between a position number as reported by self.show()
        and row and column identifiers
        """
        rowID = n//self.cols
        colID = n % self.cols
        return (rowID, colID)

    def pickRandomAvailableSquareToEat(self):
        """Gets all available squares and chooses one at random
        choosing a square eats from the lower right corner up to and
        including that square
        """
        allMoves = np.arange(0, self.rows*self.cols)
        barID = self.recogniseState()
        availableMoves = allMoves[np.invert(self.allStates[barID, :])]
        availableMoves = availableMoves[availableMoves != 0]
        # remove the chance of zeroing
        if len(availableMoves) == 0:
            move = -1  # resign
        else:
            move = int(np.random.choice(availableMoves, 1))
        return move

    def getBoxes(self, bounty, maxBeads, minBeads):
        """Returns a list of Box objects which help select the probability of
        choosing a square to eat
        """
        listOfBoxes = []
        for boolean in self.allStates:
            description = self.convertBooleanToDescription(boolean)
            listOfBoxes.append(Box(description, self.rows, self.cols,
                                   bounty, maxBeads, minBeads))
        return listOfBoxes

    def record(self):
        """Prints the game-win record and returns the win percentage"""
        try:
            per = (self.gamesWon/self.gamesPlayed)*100
        except ZeroDivisionError:
            per = 0
        print('PC has won {} of {} games - {:.0f} percent'.format(
            self.gamesWon,
            self.gamesPlayed,
            per))
        return per

    def save(self, filename):
        """Pickles the current array of box objects"""
        with open(filename, 'wb') as f:
            pickle.dump(self.boxes, f)

    def load(self, filename):
        """Retrieves an array of box objects"""
        with open(filename, 'rb') as f:
            boxData = pickle.load(f)
            self.boxes = boxData

    def showBoxChoices(self):
        """Graphically represents the chance of choosing a particular move
        based on the current state of self.boxes"""

        def dict2Grid(d, rows, cols):
            grid = np.zeros([rows*cols])
            for i in range(rows*cols):
                try:
                    grid[i] = d.moveDict[i]
                except KeyError:
                    grid[i] = np.nan
            grid = np.reshape(grid, [rows, cols])
            return grid

        nStates = len(self.allStates)
        sz = np.ceil(np.sqrt(nStates))
        plt.figure()
        plt.suptitle('Probability of choosing a square')
        for i in range(nStates):
            plt.subplot(sz, sz, i+1)
            g = dict2Grid(self.boxes[i], self.rows, self.cols)
            plt.imshow(g/(np.nansum(g)),
                       cmap='viridis', vmin=0, vmax=1)
            plt.ylabel('State {}'.format(i))
            plt.colorbar()

    def setState(self, n):
        """Sets the bar into a defined state n"""
        boolRep = self.enumerateStates()[n]
        eatenArray = np.reshape(boolRep, (self.rows, self.cols)).astype('int')
        self.eaten = eatenArray

    def produceListNextState(self):
        """Returns a list of 3-element tuples: (from state, move, to State)
        to help us with picking up boxes"""
        outList = []
        # first loop - starting positions
        for pos in range(1, len(self.boxes)):
            # pos is the starting position
            self.setState(pos)
#            print('Current state is {}'.format(pos))
#            self.showUnicode()
            for move in range(1, self.rows*self.cols):
                self.setState(pos)
#                print('Trying Move {}'.format(move))
                self.eat(move, 1)
                newPos = self.recogniseState()
                if pos != newPos:
                    outList.append((pos, move, newPos))
        return outList

    def play(self, opponent, display=False):
        """Play the game of Chomp against an opponent
        Generalised - takes argument 'opponent' to face either
            'human'
            'random'
            'intelligent'
        """

        def humanMove():
            """Ask the human for input, returns a valid move or -1"""
            loop = True
            self.show()
            self.showEaten()
            while loop:
                move = input(
                        'Which square would you like to go in? '
                        '(-1 to resign), blank for random ')
                try:
                    move = int(move)  # convert all good inputs to int from str
                except ValueError:
                    move = self.pickRandomAvailableSquareToEat()
                    print('Machine Randomly chose {}'.format(move))
                if (move in self.boxes[self.recogniseState()].moveDict.keys()):
                    return move
                elif move == 0:
                    print('It\'s all too much - resigned by eating poison')
                    return -1
                elif move == -1:
                    print('Human Resigns')
                    return -1
                else:
                    print('Invalid Input')

        def randomMove():
            """Select a random move from those available"""
            move = self.pickRandomAvailableSquareToEat()  # positive int or -1
            return move

        def drawMove():
            """Draw a move from the distribution"""
            move = self.boxes[current].draw()
            return move

        # initialise constants
        pcMoveList = []
        opponentMoveList = []
        positionList = []
        self.resetEaten()  # reset which boxes have been eaten
        self.gamesPlayed += 1
        self.finished = False
        winner = -1   # don't know the winner yet

        # select opponent
        if opponent.lower() == 'human':
            moveFcn = humanMove
        elif opponent.lower() == 'random':
            moveFcn = randomMove
        elif opponent.lower() == 'intelligent':
            moveFcn = drawMove
        else:
            raise NameError('Unknown Opponent')

        while self.finished is False:
            # PC part
            current = self.recogniseState()  # get current state
            positionList.append(current)  # add this to list
            move = drawMove()
            if move == -1:  # Computer resigns
                self.finished = True
                winner = 2  # other player wins
                break
            else:  # Computer plays
                self.eat(move, 1)
                pcMoveList.append(move)

            # Opponent part
            current = self.recogniseState()
            positionList.append(current)
            move = moveFcn()
            if move == -1:  # Opponent resigns
                self.finished = True
                winner = 1  # other player wins
                break
            else:  # Opponent plays
                self.eat(move, 2)
                opponentMoveList.append(move)
        if display:
            print('Position List = {}'.format(positionList))
            print('PC Moves = {}'.format(pcMoveList))
            print('Opponent Moves = {}'.format(opponentMoveList))
        if winner == 1:  # the computer wins
            if display:
                print('THE COMPUTER WINS'.format(winner))
            winPositionList = positionList[::2]
            winMoveList = pcMoveList
            self.gamesWon += 1
        else:  # the opponent wins
            if display:
                print('OPPONENT WINS -'
                      'But Chomp learns from its mistakes!')
            winPositionList = positionList[1::2]
#            winPositionList = []
            winMoveList = opponentMoveList
#            winMoveList = []
        for move, position in zip(winMoveList, winPositionList):
            if display:
                print('Boosting move {} in box {}'.format(move, position))
            self.boxes[position].replenish(move)
        return winner


class Box(object):
    '''Each bar has as many boxes as possible game states - possible moves are
    represented as beads, which are drawn from the box.

    Box methods:
        init - initialise contents depending on description
        repr - prints the dictionary
        populate - initialise internal dictionary with the right number moves
        distribution - calculates the number of beads to start in each box
        draw - return a move or -1 for resignnerate a list of Box objects
        replenish - add beads to winning moves
    '''

    def __init__(self, desc, rows, cols, bounty, maxBeads, minBeads):
        self.desc = np.squeeze(desc)  # to ensure a single dimensional array
        self.cols = cols
        self.rows = rows
        self.bounty = bounty
        self.maxBeads = maxBeads
        self.minBeads = minBeads
        self.moveDict = {}  # create an empty dictionary to store move/beads
        self.populate()  # populate this dictionary with moves

    def __repr__(self):
        return repr(self.moveDict)

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
        except KeyError:  # this occurs when trying to populate the empty bar
            pass

    def distribution(self):
        '''Controls how many initial beads get placed in each box,
        depending on how far into the game they are

        This is governed by the sum of the description (how many squares are
        left over and maxBeads and minBeads)
        '''
        maxSum = self.rows * self.cols
        totalSquaresLeft = np.sum(self.desc)
        return np.round(np.interp(
            totalSquaresLeft, [0, maxSum],
            [self.minBeads, self.maxBeads])).astype(int)

    def draw(self):
        '''Draws a move from all possible moves available from this box'''
        moveList = []
        for k in self.moveDict:
            for i in range(self.moveDict[k]):
                moveList.append(k)  # add the move this many times
        try:  # choose one from the dictionary
            selected = int(np.random.choice(moveList, 1))
            self.moveDict[selected] -= 1  # decrement
        except ValueError:  # there are no possible moves which result in a win
            selected = -1  # resign as no possible move
            # print('RAN OUT OF BEANS IN {}'.format(self.desc))
            self.populate()  # reset to original
        return selected

    def replenish(self, winningMove):
        '''Adds to the dictionary the list of moves which won the game'''
        self.moveDict[winningMove] += self.bounty


def menu():
    playChoice = input('What would you like to do: \n'
                       '1: Play Chomp against the machine \n'
                       '2: Train the machine against itself \n'
                       '3: Save the machine\'s state \n'
                       '4: Load a state from a file \n'
                       '5: View the machine\'s stats \n'
                       '0: Quit \n'
                       '> ')
    try:
        playChoice = int(playChoice)
        if playChoice in [1, 2, 3, 4, 5, 0]:
            return playChoice
        else:
            return -1
    except ValueError:
        print('Unknown menu Choice')
        return -1


if __name__ == '__main__':
    w = []  # win log
    b = Bar()  # create bar
    loop = True
    while loop:
        choice = menu()
        if choice == 1:
            playLoop = True  # keep playing
            while playLoop:
                w.append(b.play('human', display=True))
                q = input('Play Again? ([y]/n) ')
                if q == 'n':
                    playLoop = False
        elif choice == 2:
            for i in range(10000):
                b.play('random', display=False)
            print('Trained')
        elif choice == 3:
            fname = input('Type the filename to save')
            b.save(fname)
        elif choice == 4:
            filename = askopenfilename()  # show an "Open" dialog box
            b.load(filename)
        elif choice == 5:
            b.show()
            b.record()
            b.showBoxChoices()
            plt.show()
        elif choice == 0:
            loop = False  # exit
        else:
            pass


# q.load('50GamesHuman.pkl')  #


#  Auto games  # uncomment for automation
#    e = Bar(rows=3,
#            cols=4,
#            bounty=3,
#            maxBeads=2,
#            minBeads=2)  # this is default
#    gameIdx = 0
#    gameList = []
#    recordList = []
#    w = []
#    for i in range(2000):  # simulate games against random opposition
#        w.append(e.play('random', display=False))
#        gameList.append(gameIdx)
#        recordList.append(e.record())
#        gameIdx += 1
#
#    plt.figure(4)
#    plt.plot(gameList, recordList, '-')
#    plt.xlabel('Time')
#    plt.ylabel('Probability of win')
#    plt.title('Training against Random opposition')
#    # e.save('2000GamesRandom.pkl')
#    e.showBoxChoices()
#
#    f = Bar(maxBeads=6)
#    gameIdx = 0
#    gameList = []
#    recordList = []
#    w = []
#    for i in range(2000):  # simulate against intelligent opposition
#        w.append(f.play('intelligent', display=False))
#        gameList.append(gameIdx)
#        recordList.append(f.record())
#        gameIdx += 1
#
#    plt.figure(5)
#    plt.plot(gameList, recordList, '-')
#    plt.xlabel('Time')
#    plt.ylabel('Probability of win')
#    plt.title('Dual Phase Training')
#    # f.save('2000GamesIntelligent.pkl')
#    f.showBoxChoices()
