#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Code for retrieving input data and store it in global variables,
which later used across all modules
"""

from typeInfoReader import *
from Parser import *

# Extensively used variables across all the program
typeList = None     # List of objects types
floors = None       # available free space on each floor


def initialize():
    parser = Parser()
    global floors
    floors = parser.floors()
    global typeList
    typeList = TypeInfoReader(parser).preTypeList
