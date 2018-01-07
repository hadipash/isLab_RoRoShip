#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
MaxRects GridSearcher의 Interface
Superclass for GridSearcher and MaxRects classes
"""


# 내부 알고리즘 인터페이스 클래스
# 내부 알고리즘들이 필요한 함수들을 정의하고
class PositionAlgorithm:
    def __init__(self):
        # 이벤트 emitter 를 사용하는지 체크
        self.enableEmitter = False
        self.emitter = None

        # 라우팅 모듈 업데이트 횟수를 센다
        self.updateCnt = 0

    # 레이아웃을 업데이트 해야 하는 경우 실행하는 함수
    def updateLayout(self, obj):
        # 라우팅 모듈쪽에 업데이트 시키는것.
        self.updateCnt += 1
        print 'Freight: {:4}, Floor: {:1}, Coordinate X: {:7}, Coordinate Y: {:7}'\
            .format(self.updateCnt, obj.coordinates.floor + 1, obj.coordinates.x, obj.coordinates.y)
