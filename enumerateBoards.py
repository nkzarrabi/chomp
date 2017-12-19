#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to enumerate all possible boards of chomp
Created on Mon Dec 18 11:28:09 2017

@author: dan
djw1g12@soton.ac.ul
"""
import numpy as np
from copy import deepcopy

def showBoard(rows, cols):
    '''Draws the board with corresponding cell numbers'''
    pad = np.ceil(np.log10(rows*cols))
    for i in range(rows):
        print('|', end='')
        for j in range(cols):
            print('{num:''{pad}}|'.format(num=int(j+i*cols),pad=int(pad)), end='')
        print('')

def enum(rows,cols):
    '''Enumerates all possible CHOMP positions
    First, the algorithm fills in rows in reading order (left to right, then
    down ), then does the same with columns'''
    uBound = 36
    boards = np.zeros([uBound,rows,cols])
    i = 1
    for r in range(rows):
        for c in range(cols):
            boards[i,:,:] = boards[i-1,:,:] # set to previous board
            boards[i,r,c] = 1; # place a 1 in the new position
            i += 1
    i += 1
    boards[i,:,:] = np.zeros([rows,cols])
    for c in range(cols):
        for r in range(rows):
            boards[i,:,:] = boards[i-1,:,:]
            boards[i,r,c] = 1;
            i += 1
    return boards

    for i in range(rows):
        for j in range(cols):
            pass

def enum2(rows,cols):
    """Represent boards as a list with cols elements and maximum value rows
    on this board, X's are uneaten squares - add the X's to get the board ID
        X X X 0
        X X 0 0
        0 0 0 0
        - - - -
        2 2 1 0"""
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

    return boolRep

rows = 3
cols = 4
showBoard(rows, cols)

f = enum2(rows,cols)

# form an array of boolean values corresponding to taken or not



#
#
#boardPositions2 = np.zeros([len(f),rows*cols])
#
#for i,desc in enumerate(f): # for each descriptor
#    print(desc)
#    boardDescriptor = np.squeeze(desc)
#    for j,nRowsAvail in enumerate(boardDescriptor): # for each element
#        print(nRowsAvail)
#        for k in range(cols):
#            boardPositions2[i,k*rows] = 1
#        print(boardPositions2[i,:])
#



rows = 3
cols = 4
papa = np.ones([12,3])
desc = np.array([2,1,1,0])
j = 2
for i in range(cols):
    papa[i::cols,j] = np.concatenate((np.zeros([desc[i]]),np.ones([rows-desc[i]])))
papa
