#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File for miscellaneous classes and functions
"""

from routing.min_radius import *


# 화물의 종류를 나타내는 클래스
# Class for defining types of objects to be placed on a vessel
class Type:
    def __init__(self, width, height, wheelbase, steeringAngle):
        self.width = width
        self.height = height

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
        return self.width == other.width and self.height == other.height and self.L == other.L and self.a == other.a


# 물체를 표현하는 클래스
# Class for objects to be placed
class Object:
    def __init__(self, groupId, id, type):
        # 해당 물체의 종류를 나타내는 id
        self.groupId = groupId
        # 해당 물체의 고유 id
        self.id = id
        # 물체의 방향전환 결과
        # Whether an object is rotated or not (default value false)
        self.isTransformed = False
        # 물체의 타입
        self.type = type

    def getWidth(self):
        return self.type.width

    def getHeight(self):
        return self.type.height


# 좌표를 지칭하는데 사용하는 클래스
# Class for a coordinate system
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setCoordinate(self, x, y):
        self.x = x
        self.y = y

    def printCoordinate(self):
        print ("X : " + str(self.x) + ",   Y : " + str(self.y))

    def equal(self, coordinate):
        if (self.x == coordinate.x and self.y == coordinate.y):
            return True
        return False

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y


# gird의 cell에 들어 갈 클래스
# Class for cells
class Cell:
    def __init__(self):
        # 해당 좌표에 어떤 Obejct 가 있는지 저장하는 변수
        # Saves object located at certain vertex
        self.unit = None

    # 해당 좌표가 이미 선점 되었는지 확인하는 변수
    def isOccupied(self):
        if self.unit != None:
            return True
        else:
            return False

    # 해당 좌표에 존재하는 Object의 Id 를 리턴
    # Return object's id located at certain coordinates
    def getObjectId(self):
        if self.unit != None:
            return self.unit.id
        else:
            return 0

    # 같은 Obejct 인지 확인
    def isSameObject(self, Object):
        if self.unit.id == Object.id:
            return True
        else:
            return False


# 선박 클래스
class Floor:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height


# 장애물 클래스
class Obstacle:
    def __init__(self, coordinate, width, length, id):
        self.coordinate = coordinate
        self.width = width
        self.height = length
        self.isEnter = False
        self.id = id


# 입구 클래스
class Enter(Obstacle):
    def __init__(self, coordinate, width, length, id):
        Obstacle.__init__(self, coordinate, width, length, id)
        self.isEnter = True
