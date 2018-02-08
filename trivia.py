#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:35:42 2018

script to calculate the size of the flat panel
or sphere required to play certain games

@author: dan
"""

import math

def sphereRadius(nstates,wb=0.085,lb=0.120,hb=0.045):
    # volume of box in m^3
    vbox = wb*lb*hb
    vtot = nstates*vbox
    r = (vtot * 0.75 / math.pi)**(1/3)
    return r

def flatArea(nstates,wb=0.085,lb=0.120):
    abox = wb*lb
    atot = nstates*abox
    return atot

# useful numbers
nchomp = 35
ncon4 = 4531985219092
nchess = 7.7e45

m2AU = 6.6846e-12  # metres per astronomical unit
m2LD = 3.8607e-14   # metres per light day

