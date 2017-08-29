#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for evaluating each object's position
"""

import common.InitializationCode as ic


# evaluation function for scoring each possible placement
def evaluate(rect, f, obj, dbo):
    # initialize array of weights
    w = [0.1, 200, 30, 1, 1]
    return (w[0] * dte(rect, f) + w[1] * fon(obj, f) + w[2] * nob(rect, obj, dbo) +
            w[3] * dtt() + w[4] * uld())


# distance to an entrance
# preference given to places farther from the entrance
def dte(rect, f):
    # if current floor has an entrance then measure distance from the entrance
    if len(ic.floors[f].entrances) != 0:
        return ic.floors[f].entrances[0].coordinate.y - rect.bottomLeft.y
    # if the floor doesn't have an entrance then measure distance from a ramp
    else:
        return ic.floors[f].ramps[0].coordinate.y - rect.bottomLeft.y


# floor number
# lower floors preferred for bigger objects
def fon(obj, f):
    return (len(ic.floors) - f) * obj.getArea()


# number of objects which can be placed in one row
# preference given to an area where several objects can be placed
def nob(rect, obj, dbo):
    numOfObj = rect.width // (obj.getWidth() + 2 * dbo)
    if rect.width % (obj.getWidth() + 2 * dbo) >= ic.minWidth:
        numOfObj += 0.5
    return numOfObj


# distance to the same type of objects
# suppose that better to keep the same type of objects in a limited area
def dtt():
    return 0


# use of lifting decks
# in the case of placing an object in area of a lifting deck,
# decide whether to place it on the deck, under it or don't use it at all
def uld():
    return 0
