# chomp.py - script to investigate the game of chomp.
# the game is played on a 3 row x 4 column bar of chocolate
# players take turns to bite a rectangular region out of the bar, from the
# lower right corner. The upper left corner is poisoned, so the player who
# eats the last square loses.
import numpy as np
import csv
from copy import deepcopy

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
        self.eaten = np.zeros([rows, cols])  # zero = not yet eaten
        self.allPositions = self.enum()
        #self.allPositions = self.getAllPositionsFromCSV()
        self.finished = False  # game over

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
        current = np.zeros([cols,1],dtype=int)
        q = deepcopy(current.T)
        fullList.append(q)
        check = -1 # index of position to first look at
        while current[0] <= rows: # loop until higher number than rows
    #        print('Current = {}'.format(current.T))
    #        print('Check = {}'.format(check))
            if current[check] == current[check-1]: # if the current pair are same
    #            print('Current pair are the same')
                if check-1 != -1*cols: # and this isn't the last pair
    #                print('This isn''t the last pair')
                    check -= 1 # compare a pair higher
                else:
    #                print('This is the last pair')
                    current[0] += 1;
                    current[1:] = 0;
                    check = -1
                    q = deepcopy(current.T)
                    fullList.append(q)
    #                print('After copy Current = {}'.format(current.T))
            else: #current pair are not the same
                if current[check] <= current[check-1]-1: # rollover condition
    #                print('Rollover')
                    current[check] += 1;
                    if check != -1:
                        current[check+1:] = 0
                else:
    #                print('No Rollover')
                    current[check] +=1;
                q = deepcopy(current.T)
                fullList.append(q)
                check = -1
    #            print('After Copy current = {}'.format(current.T))
        check = -1

        f = fullList[:-1]#last element is not valid
        boolRep = np.zeros([rows*cols,len(f)]) # boolean representation
        for j,desc in enumerate(f):
            desc = np.squeeze(desc);
            for i in range(cols):
                boolRep[i::cols,j] = np.concatenate((np.zeros([desc[i]]),np.ones([rows-desc[i]])))

        return boolRep.T.astype('bool')


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
        print('Player {} chose to eat square {}'.format(player,n))
        if n == 0:
            print('square 0 is poisoned so Player {} loses'.format(player))
            self.finished = True
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
                print('That square is already eaten')
            print(self.eaten)

            if len(np.nonzero(self.eaten)) == (self.rows*self.cols)-1:
                print('Player {} wins'.format(player))
                self.finished = True
            print('After eating, my state is {}'
                  .format(self.recognisePosition()))
            print('\n')
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
        return np.random.choice(availableMoves, 1)

    def demo(self):
        '''makes player 1 eat the bottom 2x2 square'''
        self.eaten[1:3, 2:4] = 1


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
# with entirely random play, there seems to be no advantage to going first


    print('\n\n\n')
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

    q = bar(5,4)