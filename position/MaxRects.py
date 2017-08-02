#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
MaximalRectangles 알고리즘을 사용한 배치방법
The Maximal Rectangles algorithm for an object placement
"""

# from llist import dllist, dllistnode
from IPositionAlgorithm import *
from commonClass import *


# algorithm. 삽입 가능 공간을 관리 하는 객체
# 연구사례 중 maximal Rectangle 을 구현한 것
class MaxRects(PositionAlgorithm):
    def __init__(self):
        # super 클래스 초기화
        PositionAlgorithm.__init__(self)

        # 배치 가능 사각형 리스트
        self.rectList = []

        # 맨 초반 장애물들을 탐색하며 선박에 배치 가능한 사각형을 만든다
        self.initializeSpace()

    # 외부에서 사용될 함수
    # 입력받은 화물이 배치될 장소를 찾는다
    def searchPosition(self, obj):
        # search 함수를 사용하여 배치될 위치를 찾는다.
        coordinate = self.search(obj)
        return coordinate

    # 알고리즘을 실행하기 전 space 의 구조를 파악하여 적재 가능 사각형을 정리하는 함수
    def initializeSpace(self):

        # 먼저 선박의 크기 만큼 사각형을 만들어 리스트에 넣는다
        self.rectList.append(Rectangle(Coordinate(0 + self.boundary, 0 + self.boundary),
                                       Coordinate(self.space.width - 1 - self.boundary,
                                                  self.space.height - 1 - self.boundary)))

        # 이미 처리한 장애물, 입구를 저장하는 리스트
        processedObject = []

        # 모든 공간을 뒤지며 장애물을 찾는다
        for j in range(self.space.height):
            for i in range(self.space.width):

                # 지정된 좌표를 가져와서
                coordinate = Coordinate(i, j)
                targetVertex = self.space.getVertex(coordinate.x, coordinate.y)

                # 해당 좌표에 다른 물체가 있는지 확인한다
                if targetVertex.isOccupied():
                    # 이미 처리했던 장애물이라면 처리하지 않는다
                    alreadyProcess = self.alreadyPreProcessed(targetVertex, processedObject)
                    if not alreadyProcess:
                        # 현재 좌표에 있는 화물
                        # 그 사각형을 MaxRects 방법으로 나눈다.
                        targetRect = Rectangle(coordinate, Coordinate(coordinate.x + targetVertex.unit.getWidth() - 1,
                                                                      coordinate.y + targetVertex.unit.getHeight() - 1))

                        # 현재 사각형들을 임시로 저장 할 리스트. 바로 탐색하지 않는 이유는 탐색하는 도중 list가 변경되기 때문이다.
                        searchList = []
                        for rect in self.rectList:
                            searchList.append(rect)

                        # 임시로 저장했던 리스트를 바탕으로 기존 사각형들을 탐색하며, 현재 장애물과 겹치는 사각형들을 분할한다.
                        for rect in searchList:
                            if rect.isInclude(targetRect):
                                self.divide(rect, targetRect)

                        # 처리한 장애물 목록에 현재 장애물을 넣는다
                        processedObject.append(targetVertex.unit)

    # 이미 처리했던 장애물인지 확인하는 함수
    def alreadyPreProcessed(self, targetVertex, processedObject):
        alreadyProcess = False
        for object in processedObject:
            if targetVertex.isSameObject(object):
                alreadyProcess = True
                break
        return alreadyProcess

    # 화물을 집어넣을 사각형을 검색하는 함수
    # 여기서 Best Area Fit, Best Short Side Fit, Best Long Side Fit 사용에 따라 결과가 달라진다
    # 현재는 Best Long Side Fit
    def search(self, obj):
        fitValue = 1000000
        fitRect = None
        fitCoordinate = None

        # 후보 사각형 리스트를 모두 뒤지면서 비교
        for rect in self.rectList:
            # 정방향 배치
            remainWidth = rect.width - obj.getWidth()
            remainHeight = rect.height - obj.getHeight()
            if (remainWidth >= 0 and remainHeight >= 0) and (remainWidth < fitValue or remainHeight < fitValue):
                width = obj.getWidth()
                height = obj.getHeight()
                bottomRight = Coordinate(rect.topLeft.x + width, rect.topLeft.y + height)

                # 라우팅 확인
                if self.isSetEnable(rect.topLeft, bottomRight, obj):
                    obj.isTransformed = False
                    fitValue = min(remainWidth, remainHeight)
                    fitRect = rect
                    fitCoordinate = rect.topLeft

            # 방향 전환
            remainWidth = rect.width - obj.getHeight()
            remainHeight = rect.height - obj.getWidth()
            if (remainWidth >= 0 and remainHeight >= 0) and (remainWidth < fitValue or remainHeight < fitValue):
                width = obj.getHeight()
                height = obj.getWidth()
                bottomRight = Coordinate(rect.topLeft.x + width, rect.topLeft.y + height)

                # 라우팅 확인
                if self.isSetEnable(rect.topLeft, bottomRight, obj):
                    # 배치가 되는지 확인
                    obj.isTransformed = True
                    fitValue = min(remainWidth, remainHeight)
                    fitRect = rect
                    fitCoordinate = rect.topLeft

        # 맞는 사각형이 없는 상황. 알고리즘 종료
        if fitRect is None:
            return None

        # 배치될 사각형의 좌상단 좌표를 리턴
        return fitCoordinate

    # 레이아웃을 업데이트 하는 함수
    # 화물을 배치하여 사각형들을 조절한다
    def updateLayout(self, topLeftCoordinate, obj):

        # 사각형을 배치하는 함수 사용
        # search 함수 실행 후 화물 배치에 적절하다고 판단된 사각형(cacheRect) 에 화물 배치
        self.insert(obj, topLeftCoordinate)

        # 라우팅 모듈쪽 업데이트하기 위한 함수
        PositionAlgorithm.updateLayout(self, topLeftCoordinate, obj)

        # Gui 에 표현하기 위한 코드
        if self.enableEmitter:
            # 이벤트 발생
            self.emitter.emit(topLeftCoordinate, obj, True)

    # 화물(사각형)을 배치하는 함수
    # 화물(사각형)을 배치하고 난 뒤 남은 영역의 사각형을 만들고, 이 때 포함관계를 가진 사각형들을 제거한다
    def insert(self, obj, targetCoordinate):
        width = obj.getWidth()
        height = obj.getHeight()
        if obj.isTransformed:
            width = obj.getHeight()
            height = obj.getWidth()

        # 배치된 화물 사각형
        insertRect = Rectangle(targetCoordinate,
                               Coordinate(targetCoordinate.x + width - 1, targetCoordinate.y + height - 1))

        # 임시로 현재 사각형 리스트를 deep copy 하여 이를 기준으로 사각형들을 조정한다
        tmpRectList = []
        for rect in self.rectList:
            tmpRectList.append(rect)

        # 현재 사각형 리스트들과 추가된 사각형들을 비교하며 사각형을 나누는 작업을 한다
        for rect in tmpRectList:
            if rect.isIntersect(insertRect):
                self.divide(rect, insertRect)

    # 사각형 나누는 함수
    def divide(self, targetRect, insertRect):

        self.delTargetRect(targetRect)

        # 사각형을 4개로 만든 뒤
        topRect = Rectangle(Coordinate(targetRect.topLeft.x, targetRect.topLeft.y),
                            Coordinate(targetRect.bottomRight.x, insertRect.topLeft.y - 1))
        bottomRect = Rectangle(Coordinate(targetRect.topLeft.x, insertRect.bottomRight.y + 1),
                               Coordinate(targetRect.bottomRight.x, targetRect.bottomRight.y))
        leftRect = Rectangle(Coordinate(targetRect.topLeft.x, targetRect.topLeft.y),
                             Coordinate(insertRect.topLeft.x - 1, targetRect.bottomRight.y))
        rightRect = Rectangle(Coordinate(insertRect.bottomRight.x + 1, targetRect.topLeft.y),
                              Coordinate(targetRect.bottomRight.x, targetRect.bottomRight.y))

        # 각 사각형을 추가한다
        self.addRectangle(topRect)
        self.addRectangle(bottomRect)
        self.addRectangle(leftRect)
        self.addRectangle(rightRect)

    # 나누어진 사각형을 사각형 리스트에 추가하는 함수
    def addRectangle(self, rect):
        # 적절한 사각형이 아니라면 추가하지 않는다
        if rect.width > 0 and rect.height > 0 and not self.isAvailableRectMerge(rect):
            self.rectList.append(rect)

    # 넘겨받은 사각형을 rectList 에서 제거
    def delTargetRect(self, targetRect):
        self.rectList.remove(targetRect)

    # 사각형 merge 가능한지 체크하는 함수
    def isAvailableRectMerge(self, newRect):
        for rect in self.rectList:
            if rect.isInclude(newRect):
                return True
        return False
