# chomp.py - script to investigate the game of chomp.
# the game is played on a 3 row x 4 column bar of chocolate
# players take turns to bite a rectangular region out of the bar, from the
# lower right corner. The upper left corner is poisoned, so the player who
# eats the last square loses.
import numpy as np
import csv


class bar(object):
    def __init__(self, rows=3, cols=4):
        self.rows = rows
        self.cols = cols
        self.eaten = np.zeros([rows, cols])  # zero = not yet eaten
        self.allPositions = self.getAllPositionsFromCSV()
        self.finished = False  # game over

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
                filt = np.zeros([3, 4], dtype=bool)
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
        rowID = n//self.cols
        colID = n % self.cols
        return (rowID, colID)

    def pickRandomAvailableSquareToEat(self):
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
    for i in range(1000):
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