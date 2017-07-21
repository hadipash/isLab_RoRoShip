#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Code for retrieving input data and store it in global variables,
which later used across all modules
"""

from typeInfoReader import *
from LayoutInterface import *

# Extensively used variables across all the program
typeList = None     # List of objects types
parser = None       # Parser of json files


def initialize():
    global parser
    parser = ShipInfoParser()
    global typeList
    typeList = TypeInfoReader().preTypeList
