#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
위치결정모듈을 사용하기 위한 interface
Interface for position determination module
"""

from MaxRects import *
import common.InitializationCode as ic


# 외부에서 알고리즘 결과를 받을 클래스
class PositionResult:
    def __init__(self, placedNum, totalArea, remainArea):
        # 남은 공간을 저장하는 변수
        self.totalArea = totalArea / 1000000  # convert into m²
        self.remainArea = remainArea / 1000000
        self.percent = self.remainArea / (self.totalArea / 100.0)
        self.placedNum = placedNum


# 외부에서 사용하는 인터페이스
class PositionModule:
    def __init__(self):
        # Algorithm for placing cargoes
        self.algorithmModule = MaxRects()

    # 화물의 리스트를 받아 화물 배치
    def setPosition(self, ObjectList):
        """
        :param ObjectList: 순서가 결정 된 화물 리스트
        :return: 화물 배치 결과를 리턴. PositionResult 라는 객체를 리턴할 계획
        """

        placedNumber = 0
        usedSpace = 0

        # list 에 있는 모든 object 를 배치
        for f in range(len(ObjectList)):
            notPlaced = len(ObjectList[f])
            # place object till all are placed
            while notPlaced > 0:
                # iterate through each object
                for i in range(len(ObjectList[f])):
                    # check if an object has been placed
                    if ObjectList[f][i].coordinates.floor == -1:
                        rect = self.algorithmModule.getNextRect(f)

                        # check how many objects can be placed in the rectangle
                        numOfObj = rect.width // (ObjectList[f][i].getWidth() + 2 * sideBound) - 1

                        # if it is possible to place an object into the rectangle
                        if numOfObj >= 0 and rect.length - (ObjectList[f][i].getLength() + 2 * fbBound) >= 0:
                            j = i + 1
                            place = []

                            # scan through object list and find the same objects in the list
                            while j < len(ObjectList[f]) and numOfObj > 0:
                                if ObjectList[f][j] == ObjectList[f][i]:
                                    place.append(j)
                                    numOfObj -= 1
                                j += 1

                            if numOfObj == 0:
                                placedNumber += len(place) + 1
                                usedSpace += (len(place) + 1) * (ObjectList[f][i].getWidth() + 2 * sideBound) \
                                             * (ObjectList[f][i].getLength() + 2 * fbBound)

                                ObjectList[f][i].coordinates.setCoordinates(f, rect.bottomLeft.x + sideBound,
                                                                            rect.bottomLeft.y + fbBound)
                                self.algorithmModule.updateLayout(ObjectList[f][i])

                                if len(place) > 0:
                                    ObjectList[f][place[0]].coordinates.\
                                        setCoordinates(self.algorithmModule.placeNext(ObjectList[f][i]))
                                    self.algorithmModule.updateLayout(ObjectList[f][place[0]])

                                    for p in range(1, len(place)):
                                        ObjectList[f][place[p]].coordinates. \
                                            setCoordinates(self.algorithmModule.placeNext(ObjectList[f][place[p-1]]))
                                        self.algorithmModule.updateLayout(ObjectList[f][place[p]])

                            else:
                                notPlaced += 1
                        else:
                            notPlaced += 1

        # 남은 공간 계산 및 결과 만들기
        availSpace = 0
        for floor in ic.floors:
            availSpace += floor.availSpace

        result = PositionResult(placedNumber, availSpace, availSpace - usedSpace)
        return result
