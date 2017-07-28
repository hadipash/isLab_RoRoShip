#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Code for retrieving input data and store it in global variables,
which later used across all modules
"""

from typeInfoReader import *

# Extensively used variables across all the program
typeList = None     # List of objects types
space = None        # available free space on a vessel


def initialize():
    global space
    space = Space()
    global typeList
    typeList = TypeInfoReader().preTypeList
    x = 0
