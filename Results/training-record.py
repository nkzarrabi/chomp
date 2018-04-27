#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script to Parse Training Record spreadsheet and turn it into a Chomp-format
self.boxes array

Created on Fri Apr 27 09:58:23 2018

@author: dan
"""

import csv
import pickle

b = []

with open('Training Record.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)                    # open file for reading
    next(reader)                                    # skip header row
    for row in reader:
        # each row[0] is the box number
        d = {}
        for [colourID, howMany] in enumerate(row[1:]):  # except label column
            if howMany != '':  # if this colour is present
                d[colourID+1] = int(howMany)
        b.append(d)

savefilename = 'stored-games/RealTraining-76.pkl'
with open(savefilename, 'wb') as f:
            pickle.dump(b, f)
