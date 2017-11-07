#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module for evaluating each object's position
"""

from commonClass import *


# evaluation function for scoring each possible placement
def evaluate(rect, f, obj, rectList):
    # initialize array of weights
    w = [1, 0, 0, 0.03, 0.33, 0]
    return (w[0] * dte(rect, f, obj) + w[2] * spa(f, rect, obj, rectList) +
            w[3] * nob(rect, f, obj) + w[4] * dtt(rect, f, obj))


# distance to an entrance
# preference given to places farther from the entrance
def dte(rect, f, obj):
    # if current floor has an entrance then measure distance from the entrance
    if len(ic.floors[f].entrances) != 0:
        return (ic.floors[f].entrances[0].coordinate.y - rect.bottomLeft.y) / \
               float(ic.floors[f].entrances[0].coordinate.y)
    # if the floor doesn't have an entrance then measure distance from a ramp
    else:
        d = ic.floors[f].ramps[0].coordinate.y + ic.floors[f].ramps[0].length / 2
        if d > rect.bottomLeft.y:
            return (d - rect.bottomLeft.y) / float(ic.floors[f].length)
        else:
            return (rect.bottomLeft.y - d) / float(ic.floors[f].length)


# IS NOT USED!!! (may be is not needed)
# floor number
# lower floors are preferred for bigger objects
# def fln(obj, f):
#     return (len(ic.floors) - f) * obj.getArea()


# remain space
def spa(f, rect, obj, rectList):
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
def nob(rect, f, obj):
    numOfObj = rect.width // (obj.getWidth() + 2 * sideBound)
    if numOfObj > 1:
        return numOfObj / float(ic.floors[f].length // (obj.getWidth() + 2 * sideBound))
    return 0


# distance to the same type of objects
# suppose that better to keep the same type of objects in a limited area
def dtt(rect, f, obj):
    y = obj.type.occupiedArea(f)
    if len(y) == 0:
        return 1
    elif rect.bottomLeft.y >= y[0] and rect.bottomLeft.y + obj.getLength() <= y[1]:
        return 1
    elif rect.bottomLeft.y < y[0]:
        return (y[0] - rect.bottomLeft.y) / float(ic.floors[f].length)
    else:
        return (rect.bottomLeft.y + obj.getLength() - y[1]) / float(ic.floors[f].length)


# use of lifting decks
# in the case of placing an object in area of a lifting deck,
# decide whether to place it on the deck, under it or don't use it at all
def uld():
    return 0
