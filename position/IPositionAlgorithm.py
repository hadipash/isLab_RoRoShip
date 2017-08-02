#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
MaxRects GridSearcher의 Interface
Interface for GridSearcher and MaxRects classes
"""

from routing.graph import *
from common.InitializationCode import *


# 내부 알고리즘 인터페이스 클래스
# 내부 알고리즘들이 필요한 함수들을 정의하고
class PositionAlgorithm:
    def __init__(self):
        # 선박 주변에 배치하지 못하도록 하는 경계선의 크기
        # Boundary line to avoid placing cargoes close to a vessel's walls
        self.boundary = 0

        # ------------------------------------------------------------
        # Routing module 생성 && 라우팅 검사를 위해 입구 정보를 가져온다
        self.RM = []
        for _type in typeList:
            Graph = graph(_type)
            Graph.graph_initt()
            self.RM.append(Graph)

        # enterList 에 메인 입구(입구 2개 중 )
        self.enterList = []
        for enter in reversed(parser.parseEnterInfo()):
            self.enterList.append(enter)

        # 이벤트 emitter 를 사용하는지 체크
        self.enableEmitter = False
        self.emitter = None

        # 라우팅 모듈에 라우팅 확인하는 수를 센다
        self.checkCnt = 0
        # 라우팅 모듈 업데이트 횟수를 센다
        self.updateCnt = 0

    # 라우팅 모듈에 화물 배치 가능한지 확인하는 함수
    # Check whether placing of a cargo is possible according to the routing module
    def isSetEnable(self, leftTopCoordinate, rightBottomCoordinate, obj, path=1):
        """
        @param leftTopCoordinate: 좌상단 좌표
        @param rightBottomCoordinate: 우하단 좌표
        @param obj: 배치할 화물
        :return: True False

        """

        ################################################################################################
        # 라우팅 모듈 제대로 사용하는 부분
        isPossible = False

        # 적절한 라우팅 모듈 가져오기
        propRM = None
        for RModule in self.RM:
            if RModule.Type == obj.type:
                propRM = RModule
                break

        # 입구들 갯수만큼 검사
        # 입구를 미리 sort 하여 상단 입구 먼저 물어보도록 사용
        for enter in self.enterList:
            if (propRM.isPossible(leftTopCoordinate.x, leftTopCoordinate.y, rightBottomCoordinate.x,
                                  rightBottomCoordinate.y,
                                  enter['coordinate']['X'], enter['coordinate']['Y'], enter['volume']['width'],
                                  enter['volume']['length'], path, 0)):
                isPossible = True
                break

        self.checkCnt += 1

        return isPossible

    # 레이아웃을 업데이트 해야 하는 경우 실행하는 함수
    def updateLayout(self, topleftCoordinate, obj):
        if obj.isTransformed:
            width = obj.getLength()
            length = obj.getWidth()
        else:
            width = obj.getWidth()
            length = obj.getLength()

        # 라우팅 모듈쪽에 업데이트 시키는것.
        self.updateCnt += 1
        print "update Cnt : " + str(self.updateCnt) + ", coordinateX : " + str(
            topleftCoordinate.x) + ", coordinateY : " + str(topleftCoordinate.y)
        for rModule in self.RM:
            rModule.graph_update(topleftCoordinate.x, topleftCoordinate.y, topleftCoordinate.x + width - 1,
                                 topleftCoordinate.y + length - 1)
