#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Code for retrieving input data and store it in global variables,
which later used across all modules
"""

from Parser import *

# Extensively used variables across all the program
typeList = None     # List of objects types
floors = None       # available free space on each floor
minWidth = 0        # minimum width among all cargoes
minLength = 0       # minimum length among all cargoes


def initialize():
    parser = Parser()
    global floors
    floors = parser.floors
    global typeList
    typeList = parser.typeList
    global minWidth
    minWidth = parser.minWidth + 2 * sideBound
    global minLength
    minLength = parser.minLength + 2 * fbBound
