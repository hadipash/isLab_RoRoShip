#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
MaximalRectangles 알고리즘을 사용한 배치방법
The Maximal Rectangles algorithm for an object placement
"""

from IPositionAlgorithm import *
from commonClass import *
import common.InitializationCode as ic
from Evaluation import evaluate


# algorithm. 삽입 가능 공간을 관리 하는 객체
# 연구사례 중 maximal Rectangle 을 구현한 것
class MaxRects(PositionAlgorithm):
    def __init__(self):
        # super 클래스 초기화
        PositionAlgorithm.__init__(self)

        # 배치 가능 사각형 리스트
        # List of empty rectangles where cargoes can be placed
        self.rectList = []

        # 맨 초반 장애물들을 탐색하며 선박에 배치 가능한 사각형을 만든다
        self.initializeSpace()

    # 알고리즘을 실행하기 전 space 의 구조를 파악하여 적재 가능 사각형을 정리하는 함수
    # Divide available space into rectangles in accordance with entrances and obstacles
    def initializeSpace(self):
        # 모든 공간을 뒤지며 장애물을 찾는다
        for f in range(len(ic.floors)):
            self.rectList.append([])
            # first, represent all floors as single rectangles
            self.rectList[f].append(Rectangle(Coordinate(f, sideBound, fbBound),
                                              Coordinate(f, ic.floors[f].width - sideBound,
                                                         ic.floors[f].length - fbBound)))

            # Then split floor rectangles into smaller rectangles in accordance with entrances, obstacles, etc.
            for elem in ic.floors[f].entrances:
                entrance = Rectangle(Coordinate(f, elem.coordinate.x - sideBound,
                                                elem.coordinate.y - fbBound),
                                     Coordinate(f, elem.coordinate.x + elem.width + sideBound,
                                                elem.coordinate.y + elem.length + fbBound))
                # Find rectangle(s) in which an entrance is located
                # But before doing it, make a copy of the rectangles list,
                # because the original one will be modified
                tempList = list(self.rectList[f])
                for rect in tempList:
                    if rect.isIntersected(entrance):
                        self.divide(f, rect, entrance)

            # obstacles
            for elem in ic.floors[f].obstacles:
                obstacle = Rectangle(Coordinate(f, elem.coordinate.x - sideBound,
                                                elem.coordinate.y - fbBound),
                                     Coordinate(f, elem.coordinate.x + elem.width + sideBound,
                                                elem.coordinate.y + elem.length + fbBound))
                # Find rectangle(s) in which an obstacle is located
                tempList = list(self.rectList[f])
                for rect in tempList:
                    if rect.isIntersected(obstacle):
                        self.divide(f, rect, obstacle)

            # not loadable space
            for elem in ic.floors[f].notLoadable:
                notLoad = Rectangle(Coordinate(f, elem.coordinate.x - sideBound,
                                               elem.coordinate.y - fbBound),
                                    Coordinate(f, elem.coordinate.x + elem.width + sideBound,
                                               elem.coordinate.y + elem.length + fbBound))

                tempList = list(self.rectList[f])
                for rect in tempList:
                    if rect.isIntersected(notLoad):
                        self.divide(f, rect, notLoad)

            # ramps between floors
            for elem in ic.floors[f].ramps:
                ramp = Rectangle(Coordinate(f, elem.coordinate.x - sideBound,
                                            elem.coordinate.y - fbBound),
                                 Coordinate(f, elem.coordinate.x + elem.width + sideBound,
                                            elem.coordinate.y + elem.length + fbBound))

                tempList = list(self.rectList[f])
                for rect in tempList:
                    if rect.isIntersected(ramp):
                        self.divide(f, rect, ramp)

            # slopes
            for elem in ic.floors[f].slopes:
                slope = Rectangle(Coordinate(f, elem.coordinate.x - sideBound,
                                             elem.coordinate.y - fbBound),
                                  Coordinate(f, elem.coordinate.x + elem.width + sideBound,
                                             elem.coordinate.y + elem.length + fbBound))

                tempList = list(self.rectList[f])
                for rect in tempList:
                    if rect.isIntersected(slope):
                        self.divide(f, rect, slope)

            # TODO: add lifting decks

    # 화물을 집어넣을 사각형을 검색하는 함수
    def searchPosition(self, obj):
        maxVal = -1000000
        coord = None
        numOfObj = 0
        placeRect = None
        floor = 0

        # 후보 사각형 리스트를 모두 뒤지면서 비교
        for f in range(len(ic.floors)):
            for rect in self.rectList[f]:
                # 정방향 배치
                # check whether it is possible to place an object in a rectangle
                remainWidth = rect.width - (obj.getWidth() + 2 * sideBound)
                remainLength = rect.length - (obj.getLength() + 2 * fbBound)
                if remainWidth >= 0 and remainLength >= 0:
                    score = evaluate(rect, f, obj, self.rectList[f])
                    if score > maxVal:
                        maxVal = score
                        placeRect = rect
                        floor = f

        if placeRect is not None:
            side = self.sideToPlace(floor, placeRect)
            numOfObj = placeRect.width // (obj.getWidth() + 2 * sideBound) - 1
            if side == "Left":
                coord = Coordinate(floor, placeRect.bottomLeft.x + sideBound,
                                   placeRect.bottomLeft.y + fbBound)
            elif side == "Right":
                coord = Coordinate(floor, placeRect.bottomLeft.x + sideBound +
                                   (placeRect.width % (obj.getWidth() + 2 * sideBound)),
                                   placeRect.bottomLeft.y + fbBound)
            elif side == "Middle":
                coord = Coordinate(floor, placeRect.bottomLeft.x + sideBound +
                                   (placeRect.width % (obj.getWidth() + 2 * sideBound)) / 2,
                                   placeRect.bottomLeft.y + fbBound)

        # 배치될 사각형의 좌상단 좌표를 리턴
        return coord, numOfObj

    def sideToPlace(self, f, rect):
        # if no available space between left wall and rectangle
        if rect.bottomLeft.x == sideBound:
            return "Left"
        # if no available space between right wall and rectangle
        if rect.topRight.x == ic.floors[f].width - sideBound:
            return "Right"

        return "Middle"

    def placeNext(self, obj):
        return Coordinate(obj.coordinates.floor,
                          obj.coordinates.x + obj.getWidth() + 2 * sideBound,
                          obj.coordinates.y)

    # 레이아웃을 업데이트 하는 함수
    # 화물을 배치하여 사각형들을 조절한다
    def updateLayout(self, bottomLeftCoordinate, obj):
        # 사각형을 배치하는 함수 사용
        # search 함수 실행 후 화물 배치에 적절하다고 판단된 사각형(cacheRect) 에 화물 배치
        self.insert(obj, bottomLeftCoordinate)

        # 라우팅 모듈쪽 업데이트하기 위한 함수
        PositionAlgorithm.updateLayout(self, bottomLeftCoordinate, obj)

        # Gui 에 표현하기 위한 코드
        if self.enableEmitter:
            # 이벤트 발생
            self.emitter.emit(bottomLeftCoordinate, obj, True)

    # 화물(사각형)을 배치하는 함수
    # 화물(사각형)을 배치하고 난 뒤 남은 영역의 사각형을 만들고, 이 때 포함관계를 가진 사각형들을 제거한다
    def insert(self, obj, targetCoordinate):
        f = targetCoordinate.floor
        # 배치된 화물 사각형
        insertRect = Rectangle(Coordinate(f, targetCoordinate.x - sideBound, targetCoordinate.y - fbBound),
                               Coordinate(f, targetCoordinate.x + obj.getWidth() + sideBound,
                                          targetCoordinate.y + obj.getLength() + fbBound))

        # 현재 사각형 리스트들과 추가된 사각형들을 비교하며 사각형을 나누는 작업을 한다
        # Find rectangle(s) in which a cargo will be placed
        # But before doing it, make a copy of the rectangles list,
        # because the original one will be modified
        tempList = list(self.rectList[f])
        for rect in tempList:
            if rect.isIntersected(insertRect):
                self.divide(f, rect, insertRect)

    # 사각형 나누는 함수
    def divide(self, f, targetRect, insertRect):
        self.rectList[f].remove(targetRect)
        # 사각형을 4개로 만든 뒤
        newRects = [Rectangle(Coordinate(f, targetRect.bottomLeft.x, targetRect.bottomLeft.y),
                              Coordinate(f, targetRect.topRight.x, insertRect.bottomLeft.y)),
                    Rectangle(Coordinate(f, targetRect.bottomLeft.x, insertRect.topRight.y),
                              Coordinate(f, targetRect.topRight.x, targetRect.topRight.y)),
                    Rectangle(Coordinate(f, targetRect.bottomLeft.x, targetRect.bottomLeft.y),
                              Coordinate(f, insertRect.bottomLeft.x, targetRect.topRight.y)),
                    Rectangle(Coordinate(f, insertRect.topRight.x, targetRect.bottomLeft.y),
                              Coordinate(f, targetRect.topRight.x, targetRect.topRight.y))]
        # 각 사각형을 추가한다
        self.addRectangle(f, newRects)

    # 나누어진 사각형을 사각형 리스트에 추가하는 함수
    def addRectangle(self, f, newRects):
        # 적절한 사각형이 아니라면 추가하지 않는다
        for newRect in newRects:
            if newRect.width >= ic.minWidth and newRect.length >= ic.minLength \
                    and not self.isAvailableRectMerge(f, newRect):
                self.rectList[f].append(newRect)

    # 사각형 merge 가능한지 체크하는 함수
    def isAvailableRectMerge(self, f, newRect):
        for rect in self.rectList[f]:
            if rect.isIncluded(newRect):
                return True
        return False
