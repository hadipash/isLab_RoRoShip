#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File for miscellaneous classes and functions
"""

from routing.min_radius import *


# 화물의 종류를 나타내는 클래스
# Class for defining types of objects to be placed on a vessel
class Type:
    def __init__(self, width, length, wheelbase, steeringAngle):
        self.width = width
        self.length = length

        self.L = wheelbase
        self.a = steeringAngle

        if wheelbase <= 0:
            self.min_R = 12000 / 1000  # standard grid size로 나눠야함.
        else:
            self.min_R = cal_radius(wheelbase, steeringAngle)

        self.min_R = int(math.ceil(self.min_R))
        self.radius = pythagoras(self.min_R, self.L)
        self.radius = int(math.ceil(self.radius))

        # # 축거
        # self.wheelbase = wheelbase
        # # 조향각
        # self.steeringAngle = steeringAngle

    def __eq__(self, other):
        return self.width == other.width and self.length == other.length and self.L == other.L and self.a == other.a


# 물체를 표현하는 클래스
# Class for objects to be placed
class Object:
    def __init__(self, groupId, id, type):
        # 해당 물체의 종류를 나타내는 id
        self.groupId = groupId
        # 해당 물체의 고유 id
        self.id = id
        # 물체의 타입
        self.type = type
        self.coordinates = Coordinate(0, 0, 0)

    def setCoordinates(self, f, x, y):
        self.coordinates.setCoordinates(f, x, y)

    def getWidth(self):
        return self.type.width

    def getLength(self):
        return self.type.length


# 좌표를 지칭하는데 사용하는 클래스
# Class for a coordinate system
class Coordinate:
    def __init__(self, floor, x, y):
        self.floor = floor
        self.x = x
        self.y = y

    def setCoordinates(self, floor, x, y):
        self.floor = floor
        self.x = x
        self.y = y

    def printCoordinate(self):
        print ("X : " + str(self.x) + ",   Y : " + str(self.y))

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y


# 선박 클래스
class Floor:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height


# 선박의 공간을 관리하는 클래스
# Class for management free space of a vessel
class Space:
    def __init__(self, floorInfo, entrancesList, obstaclesList):
        self.width = floorInfo.width
        self.length = floorInfo.length
        self.height = floorInfo.height

        self.entrances = entrancesList
        self.obstacles = obstaclesList


# 장애물 클래스
class Obstacle:
    def __init__(self, coordinate, width, length, id):
        self.coordinate = coordinate
        self.width = width
        self.length = length
        self.isEnter = False
        self.id = id


# 입구 클래스
class Enter(Obstacle):
    def __init__(self, coordinate, width, length, id):
        Obstacle.__init__(self, coordinate, width, length, id)
        self.isEnter = True
