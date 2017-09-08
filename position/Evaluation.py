#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for evaluating each object's position
"""

from commonClass import *


# evaluation function for scoring each possible placement
def evaluate(rect, f, obj, sideBound, fbBound, rectList):
    # initialize array of weights
    w = [0.1, 200, 30, 0.1, 1, 1]
    return (w[0] * dte(rect, f) + w[1] * fln(obj, f) + w[2] * spa(f, rect, obj, sideBound, fbBound, rectList) +
            w[3] * nob(rect, obj, sideBound) + w[4] * dtt() + w[5] * uld())


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
# lower floors are preferred for bigger objects
def fln(obj, f):
    return (len(ic.floors) - f) * obj.getArea()


# remain space
def spa(f, rect, obj, sideBound, fbBound, rectList):
    if rect.width // (obj.getWidth() + 2 * sideBound) == 1:
        remain = rect.width - (obj.getWidth() + 2 * sideBound)
        leftRect = Rectangle(Coordinate(f, rect.bottomLeft.x, rect.bottomLeft.y),
                             Coordinate(f, rect.topRight.x - remain, rect.bottomLeft.y))
        rightRect = Rectangle(Coordinate(f, rect.bottomLeft.x + remain, rect.bottomLeft.y),
                              Coordinate(f, rect.topRight.x, rect.bottomLeft.y))
        tempRect = Rectangle(Coordinate(f, rect.bottomLeft.x, rect.bottomLeft.y),
                             Coordinate(f, rect.topRight.x, rect.bottomLeft.y + obj.getLength() + 2 * fbBound))

        for rl in rectList:
            if rl.isIntersected(tempRect):
                spaceOnLeft = True
                spaceOnRight = True

                if rightRect.bottomLeft.x - rl.bottomLeft.x < ic.minWidth:
                    spaceOnLeft = False
                if rl.topRight.x - leftRect.topRight.x < ic.minWidth:
                    spaceOnRight = False

                if not (spaceOnLeft or spaceOnRight):
                    return -1

    return 1


# number of objects which can be placed in one row
# preference given to an area where several objects can be placed
def nob(rect, obj, sideBound):
    numOfObj = rect.width // (obj.getWidth() + 2 * sideBound)
    if rect.width % (obj.getWidth() + 2 * sideBound) >= ic.minWidth:
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
