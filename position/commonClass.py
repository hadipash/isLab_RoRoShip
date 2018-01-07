#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
위치 결정에 사용될 전반적인 함수 및 데이터
General functions and data for position determination
"""

from common.InitializationCode import *
import common.InitializationCode as ic
import time

CARGO_INPUT_LIST = "../resources/input_cargo_list%d.json"


# 순서를 받지 못할 때 사용할 임시 순서 리스트를 만들어주는 함수
# Get list of all objects from a json file
def getObjectSampleList():
    objectList = []
    # there are different input files for each floor
    for f in range(len(ic.floors)):
        dataList = Parser.readJSON(CARGO_INPUT_LIST % (f + 1))["data"]

        objectList.append([])
        for data in dataList:
            objectList[f].append(Object(data["cargo_group"], data["cargo_id"], ic.typeList[data["cargo_type"]]))

    return objectList


# 사각형 클래스
class Rectangle:
    # bottomLeft 와 topRight 는 모두 coordinate 정보
    def __init__(self, bottomLeft, topRight):
        self.bottomLeft = bottomLeft
        self.topRight = topRight
        self.width = topRight.x - bottomLeft.x
        self.length = topRight.y - bottomLeft.y

    # 파라미터로 들어온 rect 가 현재 사각형에 포함되는지 확인하는 함수
    def isIncluded(self, rectangle):
        if (rectangle.bottomLeft.x >= self.bottomLeft.x
            and rectangle.bottomLeft.x + rectangle.width <= self.bottomLeft.x + self.width
            and rectangle.bottomLeft.y >= self.bottomLeft.y
            and rectangle.bottomLeft.y + rectangle.length <= self.bottomLeft.y + self.length):
            return True
        return False

    # 겹치는지 확인하는 함수
    def isIntersected(self, rectangle):
        if self.bottomLeft.x > rectangle.topRight.x: return False
        if self.topRight.x < rectangle.bottomLeft.x: return False
        if self.bottomLeft.y > rectangle.topRight.y: return False
        if self.topRight.y < rectangle.bottomLeft.y: return False
        return True

    def equal(self, rectangle):
        if self.bottomLeft.equal(rectangle.bottomLeft) and self.topRight.equal(rectangle.topRight):
            return True
        return False


# 시간을 재어 성능을 측정하는데 쓰는 클래스
class PerformanceTimer:
    def __init__(self, title):
        self.performanceTitle = title
        self.startTime = 0
        self.endTime = 0
        self.result = 0

    def start(self):
        self.startTime = time.time()

    def end(self):
        self.endTime = time.time()
        self.result += self.endTime - self.startTime

    def sPrint(self):
        return self.performanceTitle + " : " + str(self.result)
