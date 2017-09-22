#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Sample program
"""

from PositionModule import *
from Viewer.testRoRo2DViewer import *


def main():
    initialize()
    # 성능 측정기 생성
    # Declare performance measurement unit
    performance = PerformanceTimer("해 평가 소요 시간")

    # 입력 데이터 생성
    # Retrieve input data from files
    ObjectList = getObjectSampleList()

    # 위치 결정 모듈 생성
    # Initialize positioning module
    positionModule = PositionModule()

    performance.start()
    # 위치결정 모듈 사용. PositionResult 라는 형태의 클래스 리턴. 이 클래스는 PositionModule.py 파일에 정의되어 있음
    positionResult = positionModule.setPosition(ObjectList)
    performance.end()

    print
    print "Total area: " + str(positionResult.totalArea) + " m²"
    print "Remain area: " + str(positionResult.remainArea) + " m²"
    print "Number of placed cargoes: " + str(positionResult.placedNum)
    print "Number of failed to place cargoes: " + str(positionResult.notPlacedNum)
    print

    print performance.sPrint()

    drawPlots(ObjectList)


if __name__ == '__main__':
    main()
