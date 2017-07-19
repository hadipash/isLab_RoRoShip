#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
위치 결정에 사용될 전반적인 함수 및 데이터
General functions and data for position determination
"""

from common.LayoutInterface import *
from common.typeInfoReader import *
import time
typeList = TypeInfoReader().preTypeList
# 순서를 받지 못할 때 사용할 임시 순서 리스트를 만들어주는 함수
def getObjectSampleList():
    f = open("../common/cargo_input.json", 'r')
    js = json.loads(f.read())
    f.close()

    dataList = js["data"]

    objectList = []

    for data in dataList:
        object = Object(data["groupId"], data["cargoId"], typeList[int(data["cargoType"])-1])
        objectList.append(object)

    return objectList

# 임시로 만들어 둔 라우팅 모듈 클래스
class RoutingModule:
    def __init__(self):
        self.test = 1


# 사각형 클래스
class Rectangle:
    # topLeft 와 bottomRight 는 모두 coordinate 정보
    def __init__(self, topLeft, bottomRight):
        self.topLeft = topLeft
        self.bottomRight = bottomRight
        self.width = bottomRight.x - topLeft.x + 1
        self.height = bottomRight.y - topLeft.y + 1
        # self.width = bottomRight.x - topLeft.x
        # self.height = bottomRight.y - topLeft.y

    # 파라미터로 들어온 rect 가 현재 사각형에 포함되는지 확인하는 함수
    def isInclude(self, rectangle):
        if (rectangle.topLeft.x >= self.topLeft.x and rectangle.topLeft.x + rectangle.width <= self.topLeft.x + self.width and
            rectangle.topLeft.y >= self.topLeft.y and rectangle.topLeft.y + rectangle.height <= self.topLeft.y + self.height):
            return True
        return False

    # 겹치는지 확인하는 함수
    def isIntersect(self, rectangle):
        if(self.topLeft.x > rectangle.bottomRight.x): return False
        if(self.bottomRight.x < rectangle.topLeft.x): return False
        if(self.topLeft.y > rectangle.bottomRight.y): return False
        if(self.bottomRight.y < rectangle.topLeft.y): return False
        return True

    # 겹치는지 좌상단 좌표와 너비, 높이를 받아서 확인하는 함수
    def isIntersectArea(self, topLeftX, topLeftY, width, height):
        if(self.topLeft.x > topLeftX + width -1): return False
        # if(self.topLeft.x > topLeftX + width): return False
        if(self.bottomRight.x < topLeftX): return False
        if(self.topLeft.y > topLeftY + height -1): return False
        # if(self.topLeft.y > topLeftY + height): return False
        if(self.bottomRight.y < topLeftY): return False
        return True

    def equal(self, rectangle):
        if(self.topLeft.equal(rectangle.topLeft) and self.bottomRight.equal(rectangle.bottomRight)):
            return True
        return False

# GridSearcher 에서 사용할 클래스
class Candidate:
    def __init__(self, coordinate, isTransformed):
        self.coordinate = coordinate
        self.isTransformed = isTransformed

    def __hash__(self):
        return hash(self.coordinate) ^ hash(self.isTransformed)

    def __eq__(self, another):
        return self.coordinate == another.coordinate and self.isTransformed == another.isTransformed

# heap 에서 사용하는 클래스
class ScoreResult:
    def __init__(self, candidate, targetCoordinate, distScore, effScore):
        # 평가요소2(간섭도)
        self.effScore = effScore
        # 평가요소1(입구와의 거리)
        self.distScore = distScore

        # 배치할 좌상단 좌표
        self.coordinate = targetCoordinate
        # 후보해
        self.candidate = candidate

        # 점수 계산
        self.score = self.getScore()


    def getScore(self):
        score = 0
        # if(self.candidate.isTransformed == False):
        #     score += 5

        # 점수는 클수록 좋게 설계함
        # score += self.distScore - self.effScore

        # self.score = -1 * effScore
        # self.score = distScore - effScore * 2
        score +=  (self.distScore*30 - self.effScore)
        # score = self.distScore*1000000 - self.effScore
        # score += self.distScore
        return score
        # self.score += -1 * effScore


    # 점수가 높을수록 좋도록 설계
    def __cmp__(self, other):
        if(self.score > other.score):
            return -1
        elif(self.score == other.score):
            if(self.candidate.isTransformed):
                return 1
            else:
                return -1
        else:
            return 1

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

# 연산 횟수를 측정하는데 쓰는 클래스
class PerformanceCounter:
    def __init__(self, title):
        self.performanceTitle = title
        self.count = 0

    def add(self):
        self.count = self.count + 1

    def sPrint(self):
        return self.performanceTitle + " : " + str(self.count)
