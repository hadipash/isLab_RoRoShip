#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
위치결정모듈을 사용하기 위한 interface
Position determination module
"""

from MaxRects import *
import common.InitializationCode as ic


# 외부에서 알고리즘 결과를 받을 클래스
class PositionResult:
    def __init__(self, placedNum, notPlacedNum, totalArea, remainArea):
        # 남은 공간을 저장하는 변수
        self.totalArea = totalArea / 1000000  # convert into m²
        self.remainArea = remainArea / 1000000
        self.percent = self.remainArea / (self.totalArea / 100.0)
        self.placedNum = placedNum
        self.notPlacedNum = notPlacedNum


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
        failedNumber = 0
        usedSpace = 0

        # list 에 있는 모든 object 를 배치
        for f in range(len(ObjectList)):
            # variable for determining algorithm
            previous = 0    # number of previously not placed cargoes
            notPlaced = len(ObjectList[f])

            # place objects till all are placed
            while notPlaced > 0:
                # if objects can be placed line by line
                if previous != notPlaced:
                    # initialize variables
                    previous = notPlaced
                    notPlaced = 0

                    # iterate through each object
                    for i in range(len(ObjectList[f])):
                        if f == 1 and i == 25:
                            x = ObjectList[f][i]
                        # check if an object has not been placed
                        if ObjectList[f][i].coordinates.floor == -1:
                            if ObjectList[f][i].id == 'cargo359' or ObjectList[f][i].id == 'cargo417':
                                x = 0

                            rect, numOfObj = self.algorithmModule.getNextRect(ObjectList[f][i], f)

                            if rect is not None:
                                # if it is possible to place an object into the rectangle
                                if numOfObj >= 0 and rect.length - (ObjectList[f][i].getLength() + 2 * fbBound) >= 0:
                                    j = i + 1   # pointer to the next object on the list
                                    place = []  # list of objects to be placed

                                    # scan through the object list and find the same objects in the list to place
                                    while j < len(ObjectList[f]) and numOfObj > 0:
                                        if ObjectList[f][j].type == ObjectList[f][i].type:
                                            place.append(j)
                                            numOfObj -= 1
                                        j += 1

                                    if numOfObj == 0:
                                        placedNumber += len(place) + 1
                                        usedSpace += (len(place) + 1) * (ObjectList[f][i].getWidth() + 2 * sideBound) \
                                                     * (ObjectList[f][i].getLength() + 2 * fbBound)

                                        ObjectList[f][i].coordinates.setCoordinates(
                                            Coordinate(f, rect.bottomLeft.x + sideBound, rect.bottomLeft.y + fbBound))
                                        self.algorithmModule.updateLayout(ObjectList[f][i])

                                        if len(place) > 0:
                                            ObjectList[f][place[0]].coordinates.setCoordinates(
                                                self.algorithmModule.placeNext(ObjectList[f][i]))
                                            self.algorithmModule.updateLayout(ObjectList[f][place[0]])

                                            for p in range(1, len(place)):
                                                ObjectList[f][place[p]].coordinates.setCoordinates(
                                                    self.algorithmModule.placeNext(ObjectList[f][place[p - 1]]))
                                                self.algorithmModule.updateLayout(ObjectList[f][place[p]])
                                    else:
                                        notPlaced += 1
                                else:
                                    notPlaced += 1
                            else:
                                notPlaced += 1
                # if objects cannot be placed line by line anymore => use another algorithm
                else:
                    notPlaced = 0
                    # iterate through each object
                    for i in range(len(ObjectList[f])):
                        # check if an object has not been placed
                        if ObjectList[f][i].coordinates.floor == -1:
                            ObjectList[f][i].coordinates.setCoordinates(
                                self.algorithmModule.searchPosition(ObjectList[f][i], f))
                            if ObjectList[f][i].coordinates.floor != -1:
                                placedNumber += 1
                                self.algorithmModule.updateLayout(ObjectList[f][i])
                                usedSpace += (ObjectList[f][i].getWidth() + 2 * sideBound) \
                                             * (ObjectList[f][i].getLength() + 2 * fbBound)
                            else:
                                failedNumber += 1

        # 남은 공간 계산 및 결과 만들기
        availSpace = 0
        for floor in ic.floors:
            availSpace += floor.availSpace

        result = PositionResult(placedNumber, failedNumber, availSpace, availSpace - usedSpace)
        return result
