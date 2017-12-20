#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:13:02 2017

Creates art for the chomp game

@author: dan
"""
import scipy as sp
import numpy as np
from chomp import Bar

a = Bar()
states = a.allStates
r = a.rows
c = a.cols
sqr = sp.misc.imread('Art/square.jpg')
bad = sp.misc.imread('Art/badSquare.jpg')
pixSize = sqr.shape[0]

for i, state in enumerate(states):
    state = np.reshape(state, [r, c])
    imageArray = np.ones([r*pixSize, c*pixSize, sqr.shape[2]])
    for j in range(r):
        for k in range(c):
            if (j == 0 and k == 0):
                img = bad
            else:
                img = sqr
            if not state[j, k]:
                imageArray[j*pixSize:(j+1)*pixSize,
                           k*pixSize:(k+1)*pixSize, :] = img
                sp.misc.imsave('Art/{}.jpg'.format(i), imageArray)
