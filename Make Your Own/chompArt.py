#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:13:02 2017

Creates box lid designs for CHOMP

@author: dan
"""
import scipy as sp
import numpy as np
from chomp import Bar

pathGoodSquare = 'path/to/good/square.png'
pathBadSquare = 'path/to/bad/square.png'
savePath = 'path/to/save'

a = Bar()
states = a.allStates
r = a.rows
c = a.cols
sqr = sp.misc.imread(pathGoodSquare)
bad = sp.misc.imread(pathBadSquare)
pixh = sqr.shape[0]
pixv = sqr.shape[1]
imageArray = np.ones([r*pixh, c*pixv, sqr.shape[2]])
sp.misc.imsave('{}/out0.png'.format(savePath), imageArray)
for i, state in enumerate(states):
    state = np.reshape(state, [r, c])
    imageArray = np.ones([r*pixh, c*pixv, sqr.shape[2]])
    for j in range(r):
        for k in range(c):
            if (j == 0 and k == 0):
                img = bad
            else:
                img = sqr
            if not state[j, k]:
                imageArray[j*pixh:(j+1)*pixh,
                           k*pixv:(k+1)*pixv, :] = img
                sp.misc.imsave('{}/out{}.png'.format(savePath,i), imageArray)
