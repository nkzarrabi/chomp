# script to draw chomp win diagram

import numpy as np
import matplotlib.pyplot as plt

plt.close('all')

winstr = 'lwlllll\
          lwlllll\
          wlwllll\
          wlwlwlw\
          lwlwlwl\
          lwlwlwl\
          wlwlwlw\
          wlwlwlw\
          wlwlwww\
          lwlwlwl\S
          wwwllw'

          # this string of wins is not exact! taken from graph

for j in range(4,10):

    setSize = j # games per set

    winstr = winstr.replace(' ', '')  # get rid of spaces

    losses = winstr.count('l')
    wins = winstr.count('w')
    tot = len(winstr)

    sets = tot//setSize+1

    d = np.zeros([setSize, sets])

    for i in range(sets):
        substr = winstr[i*setSize:(i+1)*setSize]
        #    print(substr)
        d[:, i] = 0.5  # initialise to nan
        subwins = substr.count('w')
        subloss = substr.count('l')
        print('{} = {}w + {}l'.format(substr, subwins, subloss))
        if subwins != 0:
            d[:subwins,i] = 1;
        if subloss != 0:
            d[-subloss:,i] = 0;


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.pcolor(d)
    ax.xaxis.set_ticks(np.arange(0,sets))
    ax.grid(True)