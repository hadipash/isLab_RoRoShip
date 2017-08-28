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
    def __init__(self, placedNum, notPlacedNum, totalArea, remainArea):
        # 남은 공간을 저장하는 변수
        self.totalArea = totalArea / 1000000  # convert into m²
        self.remainArea = remainArea / 1000000
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
        notPlacedNumber = 0
        usedSpace = 0

        # variables for simultaneous placing of several objects
        numOfObj = 0
        tempObj = None
        side = ""

        # list 에 있는 모든 object 를 배치
        for obj in ObjectList:
            # place several objects simultaneously
            if numOfObj > 0 and obj.type == tempObj.type:
                tlCoordinate = self.algorithmModule.placeSeveral(tempObj, side)

                placedNumber += 1
                obj.coordinates.setCoordinates(tlCoordinate)
                usedSpace += obj.getWidth() * obj.getLength()
                self.algorithmModule.updateLayout(tlCoordinate, obj)

                numOfObj -= 1
                tempObj = obj

            # place one by one
            else:
                # 배치할 위치 탐색. 탐색에 성공하면 배치할 영역의 좌상단 좌표를 리턴 받는다
                tlCoordinate, numOfObj, side = self.algorithmModule.searchPosition(obj)
                tempObj = obj

                if tlCoordinate is not None:
                    placedNumber += 1
                    # update coordinates of the cargo
                    obj.coordinates.setCoordinates(tlCoordinate)
                    # 배치할 위치가 있다면 사용한 영역 계산
                    usedSpace += obj.getWidth() * obj.getLength()
                    # 레이아웃 업데이트
                    self.algorithmModule.updateLayout(tlCoordinate, obj)
                else:
                    notPlacedNumber += 1

        # 남은 공간 계산 및 결과 만들기
        availSpace = 0
        for floor in ic.floors:
            availSpace += floor.availSpace

        result = PositionResult(placedNumber, notPlacedNumber, availSpace, availSpace - usedSpace)
        return result

    # Gui 프로그램에서 해당 함수를 통해 이벤트를 전달할 수 있는 객체를 준다
    # 프로그램에서는 해당 객체를 통해 특정 시점에 이벤트를 발생 시킴
    def setEventEmitter(self, emitter):
        self.algorithmModule.enableEmitter = True
        self.algorithmModule.emitter = emitter
