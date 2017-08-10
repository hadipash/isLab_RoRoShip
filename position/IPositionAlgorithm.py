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

        # 이벤트 emitter 를 사용하는지 체크
        self.enableEmitter = False
        self.emitter = None

        # 라우팅 모듈에 라우팅 확인하는 수를 센다
        self.checkCnt = 0
        # 라우팅 모듈 업데이트 횟수를 센다
        self.updateCnt = 0

    # 레이아웃을 업데이트 해야 하는 경우 실행하는 함수
    def updateLayout(self, topleftCoordinate, obj):
        # 라우팅 모듈쪽에 업데이트 시키는것.
        self.updateCnt += 1
        print "update Cnt : " + str(self.updateCnt) + ", coordinateX : " + str(
            topleftCoordinate.x) + ", coordinateY : " + str(topleftCoordinate.y)
