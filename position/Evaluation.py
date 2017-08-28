#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for evaluating each object's position
"""


# evaluation function for scoring each possible placement
def evaluate(self):
    # initialize array of weights
    w = [1, 1, 1, 1]
    return w[0] * dte() + w[1] * nob() + w[2] * dtt() + w[3] * uld()


# distance to an entrance
# suppose that bigger objects must be farther from the entrance
# than smaller one for smooth routing
def dte():
    return 0


# number of objects which can be placed in one row
# preference given to an area where several objects can be placed
def nob():
    return 0


# distance to the same type of objects
# suppose that better to keep the same type of objects in a limited area
def dtt():
    return 0


# use of lifting decks
# in the case of placing an object in area of a lifting deck,
# decide whether to place it on the deck, under it or don't use it at all
def uld():
    return 0
