#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
위치결정모듈을 사용하기 위한 interface
Interface for position determination module
"""

from GridSearcher import *
from MaxRects import *


# 외부에서 알고리즘 결과를 받을 클래스
class PositionResult:
    def __init__(self, isAllSet, remainArea):
        # 모두 배치되었는지를 저장하는 변수
        self.isAllSet = isAllSet
        # 남은 공간을 저장하는 변수
        self.remainArea = remainArea

    # 해당 클래스에 담겨있는 정보를 출력하는 함수
    def getInfo(self):
        print "isAllSet : " + str(self.isAllSet) + ", remainArea : " + str(self.remainArea)


# 외부에서 사용하는 인터페이스
class PositionModule:
    def __init__(self, algoType):
        # 상황에 따라 아래 알고리즘 수행
        # Algorithm for placing cargoes
        if algoType == 'MaxRects':
            self.algorithmModule = MaxRects()
        else:
            self.algorithmModule = GridSearcher()

    # 화물의 리스트를 받아 화물 배치
    def setPosition(self, ObjectList):
        """
        :param ObjectList: 순서가 결정 된 화물 리스트
        :return: 화물 배치 결과를 리턴. PositionResult 라는 객체를 리턴할 계획
        """
        isSuccess = True

        processedDataCnt = 0
        usingVertex = 0

        # list 에 있는 모든 object 를 배치
        for obj in ObjectList:

            # 배치할 위치 탐색. 탐색에 성공하면 배치할 영역의 좌상단 좌표를 리턴 받는다
            tlCoordinate = self.setObjectPosition(obj)

            if tlCoordinate is not None:
                # 배치할 위치가 있다면 사용한 영역 계산
                usingVertex += obj.getWidth() * obj.getHeight()
                # 레이아웃 업데이트
                self.updateLayout(tlCoordinate, obj)
            else:
                # 배치 실패. 원래 코드.
                isSuccess = False
                break

            processedDataCnt += 1

        # 남은 공간 계산 및 결과 만들기
        result = PositionResult(isSuccess, self.space.width * self.space.height - usingVertex)
        return result

    # 개별 화물을 받아 화물을 배치 시도
    def setObjectPosition(self, Object):
        """
        :param Object: 개별 화물
        :return: 화물 배치 결과로써 단순히 배치된 좌표를 리턴. 배치를 못 할 경우 좌표가 None.
        """

        coordinate = self.algorithmModule.searchPosition(Object)
        return coordinate

    # 라우팅 모듈에 화물이 배치되어 레이아웃이 갱신되었음을 알리는 함수
    def updateLayout(self, coordinate, object):
        self.space.setObject(object, coordinate)
        self.algorithmModule.updateLayout(coordinate, object)

    # Gui 프로그램에서 해당 함수를 통해 이벤트를 전달할 수 있는 객체를 준다
    # 프로그램에서는 해당 객체를 통해 특정 시점에 이벤트를 발생 시킴
    def setEventEmitter(self, emitter):
        self.algorithmModule.enableEmitter = True
        self.algorithmModule.emitter = emitter
