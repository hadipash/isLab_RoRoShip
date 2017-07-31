#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
제안 방안에 따라 만들어진 배치방법
Placement method according to the proposed algorithm
"""

import heapq

from commonClass import *
from IPositionAlgorithm import *


# 알고리즘 수행하는 클래스 중 하나
class GridSearcher(PositionAlgorithm):
    def __init__(self, space, typeList):
        # super class 세팅 및 초기값 세팅
        PositionAlgorithm.__init__(self, space, typeList)
        self.space = space

        # 배치된 사각형을 가지고 있을 리스트
        # List of placed objects
        self.settedObjectList = []
        self.settedSize = 0

        # 후보해를 가지고 있을 리스트
        self.candidate = []

        # 타입 리스트들을 큰 순서로 정렬하여 가장 작은 화물과 가장 큰 화물을 찾아낼 수 있도록 한다.
        typeRelation = sorted(typeList, key=lambda type: type.height)
        typeRelation = sorted(typeRelation, key=lambda type: type.width)
        typeRelation = sorted(typeRelation, key=lambda type: type.width * type.height)

        # 가장 작은 화물과 가장 큰 화물을 가져와 저장한다.
        # 이때 가장 작은 화물을 후보해 제거를 위한 용도로 사용한다.
        # 가장 큰 화물은 후보해 평가시 effectCheck 에서 사용한다. 이는 제안방안의 간섭검사를 하는 부분이다.
        self.delType = typeRelation[0]
        self.delObject = Object(0, -1, self.delType)
        self.largestType = typeRelation[len(typeRelation) - 1]

        # ------------------------------------------------------------
        # 후보해 정리하는 부분.
        # 기본 컨셉은 시작 후보해들은 각 모서리들
        # 큰 화물을 위해 메인 입구 맞은편 면을 후보해로 append

        # 좌상단 좌표들을 후보해로 리스트에 append
        startX = 0 + self.boundary
        startY = 0 + self.boundary
        for x in range(0, 2):
            for y in range(0, 2):
                self.candidate.append(Candidate(Coordinate(startX + x, startY + y), False))
                self.candidate.append(Candidate(Coordinate(startX + x, startY + y), True))

        # 우상단 좌표들을 후보해로 리스트에 append
        startX = self.space.width - 1 - self.boundary
        startY = 0 + self.boundary
        for x in range(0, 2):
            for y in range(0, 2):
                self.candidate.append(Candidate(Coordinate(startX - x, startY + y), False))
                self.candidate.append(Candidate(Coordinate(startX - x, startY + y), True))

        # 좌하단 좌표들을 후보해로 리스트에 append
        startX = 0 + self.boundary
        startY = self.space.height - 1 - self.boundary
        for x in range(0, 2):
            for y in range(0, 2):
                self.candidate.append(Candidate(Coordinate(startX + x, startY - y), False))
                self.candidate.append(Candidate(Coordinate(startX + x, startY - y), True))

        # 우하단 좌표들을 후보해로 리스트에 append
        startX = self.space.width - 1 - self.boundary
        startY = self.space.height - 1 - self.boundary
        for x in range(0, 2):
            for y in range(0, 2):
                self.candidate.append(Candidate(Coordinate(startX - x, startY - y), False))
                self.candidate.append(Candidate(Coordinate(startX - x, startY - y), True))

        # 입구 정보를 가져온다.
        self.Enters = parser.parseEnterInfo()
        # 입구 맞은편 면 전체를 후보해로 리스트에 append
        # 해당 후보해들은 큰 화물이 입력될 때 큰 회전반경으로 구석에 가지 못하는 경우가 있다. 즉, 직진으로만 들어오므로 맞은편도 후보해로 넣음.
        startX = 0
        startY = self.space.height - 1 - self.boundary
        for x in range(0, self.space.width):
            self.candidate.append(Candidate(Coordinate(startX + x, startY), False))
            self.candidate.append(Candidate(Coordinate(startX + x, startY), True))

        # 중복되는 후보해를 제거
        self.adjustCandidateList()

        # ------------------------------------------------------------
        # 가장 작은 화물의 크기를 구해 비어있는 자리를 탐색할 때 cell 탐색 단위를 정한다
        # ex) 가장 작은 화물 크기가 2라면, 빈자리 탐색시 cell을 2칸씩 옮겨가면 빈 위치를 탐색한다

        # 가장 작은 화물 크기를 구한다.
        small = 999
        smallSize = 9999
        for type in typeList:
            if small > type.width:
                small = type.width
            if small > type.height:
                small = type.height
            if smallSize > type.width * type.height:
                smallSize = type.width * type.height

        self.minCargoSize = small
        self.minCargo = smallSize

        # ------------------------------------------------------------
        # 시간이나 연산횟수 같은 퍼포먼스를 측정하기 위한 객체들

        # 타이머 정리
        self.searchEmptyAreaTimer = PerformanceTimer("빈자리 탐색 시간")
        self.routingTime = PerformanceTimer("라우팅 탐색 시간")
        self.searchCandidateTime = PerformanceTimer("후보해 탐색 시간")
        self.searchCandidateCount = PerformanceCounter("후보해 탐색 횟수")
        self.calEffectTime = PerformanceTimer("영향력 검사 시간")
        self.calDistanceTime = PerformanceTimer("입구거리 검사 시간")

        # 카운터 정리
        self.routingCount = PerformanceCounter("라우팅 탐색 횟수")

    # 화물이 배치될 때 후보해를 조절하는 함수
    def setObjectCandidate(self, TLCoordinate, BRCoordinate):
        # 제거할 후보해 리스트
        removeCandidateList = []

        # 배치된 화물 주변 1칸씩 포함하여 탐색
        for coordiY in range(TLCoordinate.y - 1, BRCoordinate.y + 2):
            for coordiX in range(TLCoordinate.x - 1, BRCoordinate.x + 2):

                # 배치된 화물내부의 좌표인지 체크하는 변수들
                inObjectY = (coordiY > TLCoordinate.y - 1) and (coordiY < BRCoordinate.y + 1)
                inObjectX = (coordiX > TLCoordinate.x - 1) and (coordiX < BRCoordinate.x + 1)

                # 배치된 화물내부라면
                if inObjectX and inObjectY:
                    # 제거할 후보해 리스트에 추가
                    removeCandidateList.append(Candidate(Coordinate(coordiX, coordiY), False))
                    removeCandidateList.append(Candidate(Coordinate(coordiX, coordiY), True))

                # 배치된 화물 주변 좌표들을 후보해에 추가
                if ((coordiY == TLCoordinate.y - 1 or coordiY == BRCoordinate.y + 1) or
                        (coordiX == TLCoordinate.x - 1 or coordiX == BRCoordinate.x + 1)):

                    # 벽면에서 boundary 만큼 떨어져 있는지 확인
                    isInXBound = (self.boundary <= coordiX <= self.space.width - 1 - self.boundary)
                    isInYBound = (self.boundary <= coordiY <= self.space.height - 1 - self.boundary)

                    # 벽면 boundary 에 속하지 않으며 화물 주변의 좌표들을 모두 후보해로 append
                    if (isInXBound and isInYBound and (self.space.getVertex(coordiX, coordiY).isOccupied() == False)):
                        self.candidate.append(Candidate(Coordinate(coordiX, coordiY), False))
                        self.candidate.append(Candidate(Coordinate(coordiX, coordiY), True))

        # 후보해 리스트에서 제거할 후보해들을 걸러낸다
        self.candidate = self.arrDiff(self.candidate, removeCandidateList)

    # 중복되는 후보해들을 제거하기 위한 함수
    def adjustCandidateList(self):
        self.candidate = list(set(self.candidate))

    # 외부에서 사용될 함수
    # 입력받은 화물이 배치될 장소를 찾는다
    def searchPosition(self, Object):

        # search 함수를 사용하여 화물의 배치위치를 가져온다
        resultCoordinate = self.search(Object)

        # 회전에 따라 width와 height 를 결정한다
        width = Object.getWidth()
        height = Object.getHeight()
        if Object.isTransformed:
            width = Object.getHeight()
            height = Object.getWidth()

        # 배치할 위치가 있다면
        if resultCoordinate != None:
            # 배치화물 리스트에 배치된 영역을 사각형 객체로 만들어 append 한다. 이는 빈자리 탐색, 간섭검사에서 사용이 가능
            afterX = resultCoordinate.x + width - 1
            afterY = resultCoordinate.y + height - 1
            newCoordi = Coordinate(afterX, afterY)
            self.settedObjectList.append(Rectangle(resultCoordinate, newCoordi))
            # 화물의 후보해를 조절한다
            # 아직 화물이 배치되지 않았지만 해당 장소에 배치될 거라는 판단에 바로 후보해를 조정한다
            self.setObjectCandidate(resultCoordinate, newCoordi)
            self.adjustCandidateList()

        # 로그 출력
        print self.routingCount.sPrint() + "\t " + self.routingTime.sPrint() + "\t " + self.searchCandidateTime.sPrint() + "\t " + self.searchCandidateCount.sPrint() + "\t " + self.calEffectTime.sPrint() + "\t " + self.calDistanceTime.sPrint()
        self.settedSize = self.settedSize + Object.getWidth() * Object.getHeight()

        # 배치 좌표 리턴
        return resultCoordinate

    # 후보해를 뒤지며 평가를 진행하여 배치 위치를 찾아내는 함수
    def search(self, Object):
        # 후보 위치 중에서 적절한 위치를 탐색
        # 마지막엔 적절한 좌표를 리턴
        # 적절한 좌표가 없으면 None 리턴
        # 모든 배치는 주어진 좌표에 화물의 좌상단을 기준으로 계산

        # 결과를 저장할 좌표 객체
        properCoordinate = None

        # 평가 결과를 저장할 heap
        scoreHeap = []

        # 성능 측정 모듈 시작(후보해 탐색 시간을 계산)
        self.searchCandidateTime.start()

        # 후보해 탐색
        for candidate in self.candidate:

            # 후보의 방향에 따라 가로와 세로를 결정
            Height = Object.getHeight()
            Width = Object.getWidth()
            transStr = "세로로 길게 배치"
            if candidate.isTransformed:
                transStr = "가로로 길게 배치"
                Height = Object.getWidth()
                Width = Object.getHeight()

            # 후보해의 좌표를 가져온다
            coordinate = candidate.coordinate
            # 후보해를 기준 좌표(좌상단)로 변환한 좌표
            targetCoordinate = None

            # 성능 측정 모듈 카운트(후보해 탐색 횟수 측정)
            self.searchCandidateCount.add()

            # 여기서 좌상단에 배치가 가능한지 체크. 배치가 안되면 그대로 걸러냄.
            isProperLeft = (coordinate.x + Width <= self.space.width - 1) and\
                           (self.space.getVertex(coordinate.x + 1, coordinate.y).isOccupied() == False)
            isProperTop = (coordinate.y + Height <= self.space.height - 1) and\
                          (self.space.getVertex(coordinate.x, coordinate.y + 1).isOccupied() == False)

            # 주변 벽을 보고 기준좌표를 옮기는 코드
            # 원래는 좌상단 기준으로 배치를 하지만, 좌상단 기준으로 배치를 할 수 없는 경우도 있다.(후보해가 선박의 좌하단 모서리 or 우하단 모서리)
            # 이때는 좌측, 우측 배치가 가능한지 미리 계산해둔 boolean 값을 사용하여 후보해를 조절해준다.
            if isProperLeft and isProperTop:
                # 좌측 상단 배치가 가능하므로 후보해를 그대로 사용한다
                targetCoordinate = coordinate
            elif ((isProperLeft == False) and isProperTop):
                # 후보좌표가 화물의 좌측이 되면 화물을 배치할 수 없는 상태
                # 그러므로 후보해 위치에 화물의 우상단으로 맞춰 배치할 수 있도록 좌표를 조절한다
                if coordinate.x - Width + 1 >= self.boundary:
                    targetCoordinate = Coordinate(coordinate.x - Width + 1, coordinate.y)
            elif (isProperLeft and (isProperTop == False)):
                # 후보좌표가 화물의 상단이 되면 화물을 배치할 수 없는 상태
                # 그러므로 후보해 위치에 화물의 하단으로 맞춰 배치할 수 있도록 좌표를 조절한다
                if (coordinate.y - Height + 1 >= self.boundary):
                    targetCoordinate = Coordinate(coordinate.x, coordinate.y - Height + 1)
            else:
                # 후보좌표가 화물의 좌측 및 상단이 되면 화물을 배치할 수 없는 상태
                # 그러므로 후보해 위치에 화물의 우하단으로 맞춰 배치할 수 있도록 좌표를 조절한다
                if ((coordinate.x - Width + 1 >= self.boundary) and (coordinate.y - Height + 1 >= self.boundary)):
                    targetCoordinate = Coordinate(coordinate.x - Width + 1, coordinate.y - Height + 1)

            if targetCoordinate:
                # 후보해 조절에 성공한 경우
                pass
            else:
                # 후보해를 조절할 수 없는 경우
                continue

            # 성능 측정 모듈 시작(빈자리 탐색 시간을 계산)
            self.searchEmptyAreaTimer.start()
            # 주어진 영역이 비어있는지 확인
            isEmpty = self.isEmptyAreaCoordinate(targetCoordinate, Width, Height)
            self.searchEmptyAreaTimer.end()

            # 해당 후보위치가 비어있다면
            if isEmpty:
                # 후보해에 맞게 객체의 방향을 돌려줌
                Object.isTransformed = candidate.isTransformed

                self.calEffectTime.start()
                # 간섭검사 평가
                effects = self.checkEffect(Object, targetCoordinate)
                self.calEffectTime.end()

                self.calDistanceTime.start()
                # 입구와의 거리 평가
                enterDistance = self.checkEnterDistance(Object, targetCoordinate, 1)
                self.calDistanceTime.end()

                # heap 에 처리할 아이템 생성
                scoreResult = ScoreResult(candidate, targetCoordinate, enterDistance, effects)
                heapq.heappush(scoreHeap, scoreResult)

        self.searchCandidateTime.end()

        # 힙을 사용하여 라우팅 체크
        self.routingTime.start()
        # heap 에 있는 후보해를 모두 탐색하며 라우팅이 되는지 체크할 때, 중복된 후보해가 나올수도 있다. 이 때 중복 라우팅을 피하기 위해 진전 위치와 방향을 저장한다
        cacheCoordi = Coordinate(-1, -1)
        cacheTrans = False
        heapCounter = 0
        # 힙 조사
        for i in range(len(scoreHeap)):
            # 힙에서 결과를 하나 꺼냄
            scoreResult = heapq.heappop(scoreHeap)
            # 실제 배치할 좌표
            targetCoordi = scoreResult.coordinate
            # 후보해
            candidate = scoreResult.candidate

            # 같은 좌표가 등장할 수가 있다. 그것을 제거하기 위한 코드
            if (cacheCoordi == candidate.coordinate and cacheTrans == candidate.isTransformed):
                continue

            # 방향에 따라 가로, 세로 길이를 정하며 화물의 방향도 정해준다
            Height = Object.getHeight()
            Width = Object.getWidth()
            transStr = "세로로 길게 배치"
            Object.isTransformed = False
            if candidate.isTransformed:
                transStr = "가로로 길게 배치"
                Height = Object.getWidth()
                Width = Object.getHeight()
                Object.isTransformed = True

            # 중복 좌표를 제거하기 위한 캐시값을 업데이트 한다
            cacheCoordi = targetCoordi
            cacheTrans = candidate.isTransformed

            # 우하단 좌표를 만든다
            brCoordinate = Coordinate(targetCoordi.x + Width - 1, targetCoordi.y + Height - 1)

            # 성능 측정을 위한 코드
            self.routingCount.add()
            heapCounter = heapCounter + 1

            # Gui 프로그램쪽으로 이벤트를 발생시키는 코드.
            # 프로그램 최종 시연을 위해 추가된 코드
            if self.enableEmitter:
                # 이벤트 발생
                self.emitter.emit(targetCoordi, Object, False)
                # 이벤트를 발생시키면 알고리즘 계산을 멈춰 gui에서 너무 빨리 보이지 않도록 한다
                time.sleep(0.2)

            # 배치가 가능한지 확인한다
            if (self.isSetEnable(targetCoordi, brCoordinate, Object) == True):
                # 배치가 가능한 경우
                properCoordinate = targetCoordi

                # 해당 위치에 배치가 가능하다고 Gui 에 이벤트를 발생시킨다
                if self.enableEmitter:
                    self.emitter.emit(targetCoordi, Object, True)
                    time.sleep(0.1)

                # 로그를 출력
                print "candidate " + str(heapCounter) + "번째  후보좌표 : ( " + str(candidate.coordinate.x) + ", " + str(
                    candidate.coordinate.y) + " )" + ", 변환좌표 : ( {}, {} ) ".format(
                    targetCoordi.x, targetCoordi.y) + "\t {}*{}".format(Object.getWidth(),
                                                                        Object.getHeight()) + "\t " + transStr + ", 전체 score : {}, 거리 : {}, 영향력 : {}".format(
                    scoreResult.getScore(), scoreResult.distScore, scoreResult.effScore)

                # 배치할 위치를 찾았다면 탐색 종료
                break
            else:
                # 후보해에 배치가 불가능한 경우
                delStr = "  후보해 제거 안됨"
                tmpWidth = self.delObject.getWidth()
                tmpHeight = self.delObject.getHeight()
                if candidate.isTransformed:
                    tmpWidth = self.delObject.getHeight()
                    tmpHeight = self.delObject.getWidth()

                tmpBrCoordinate = Coordinate(targetCoordi.x + tmpWidth - 1, targetCoordi.y + tmpHeight - 1)

                # 가장 작은 크기의 화물을 배치시켜 보고, 불가능 하다면 후보해를 제거함
                if (self.isSetEnable(targetCoordi, tmpBrCoordinate, self.delObject, path=0) == False):
                    self.candidate.remove(candidate)
                    delStr = "  후보해 제거됨"

                # 로그 출력
                print "candidate " + str(heapCounter) + "번째  후보좌표 : ( " + str(candidate.coordinate.x) + ", " + str(
                    candidate.coordinate.y) + " )" + ", 변환좌표 : ( {}, {} ) ".format(
                    targetCoordi.x, targetCoordi.y) + "\t {}*{}".format(Object.getWidth(),
                                                                        Object.getHeight()) + "\t " + transStr + ", 전체 score : {}, 거리 : {}, 영향력 : {}".format(
                    scoreResult.getScore(), scoreResult.distScore, scoreResult.effScore) + delStr

        self.routingTime.end()

        # 좌표를 리턴. null 이면 배치할 장소가 없는 경우.
        return properCoordinate

    # 빈 공간을 탐색하는 함수
    # 이 함수는 x, y 2개의 변수를 받아서 사용
    def isEmptyArea(self, x, y, width, height):
        # 기존에 빈 공간 탐지하던 방법
        return self.space.isEmptyArea(x, y, width, height)

        # 새로운 방법
        # 이미 배치된 화물들과 겹치는지 체크하는 방법
        # for setted in self.settedObjectList:
        #     # intersected = setted.isIntersect(Rectangle(targetCoordinate, Coordinate(targetCoordinate.x + width-1, targetCoordinate.y + height-1)))
        #     intersected = setted.isIntersectArea(x, y, width, height)
        #     if(intersected):
        #         return False
        # return True

    # 빈 공간을 탐색하는 함수
    # 이 함수는 coordinate 객체를 받아서 사용
    def isEmptyAreaCoordinate(self, coordinate, width, height):
        # 기존에 빈 공간 탐지하던 방법
        return self.space.isEmptyArea(coordinate.x, coordinate.y, width, height)

        # 새로운 방법
        # 이미 배치된 화물들과 겹치는지 체크하는 방법
        # for setted in self.settedObjectList:
        #     # intersected = setted.isIntersect(Rectangle(targetCoordinate, Coordinate(targetCoordinate.x + width-1, targetCoordinate.y + height-1)))
        #     intersected = setted.isIntersectArea(x, y, width, height)
        #     if(intersected):
        #         return False
        # return True

    # 평가요소2. 간섭검사
    def checkEffect(self, Object, coordinate):
        # 물체가 해당 좌표에 배치 되었을 경우 다른 타입의 화물에 주는 영향을 체크
        # 해당 위치에서 다른 화물에 주는 간섭의 수를 리턴

        # 배치되려는 장소 주변을 모두 탐색 하는것이 아닌, 상하좌우 4방향으로 모서리, 중간 에 장애물이 있는지 확인하고
        # 그 장애물이 있는 쪽으로는 배치를 시도하지 않음

        # 리턴할 간섭정도
        EffectCnt = 0

        # 화물의 방향을 보고 가로, 세로 길이 결정
        Width = Object.getWidth()
        Height = Object.getHeight()
        if Object.isTransformed:
            Width = Object.getHeight()
            Height = Object.getWidth()

        leftLimit = False
        rightLimit = False
        upLimit = False
        bottomLimit = False

        # 왼편 확인
        if coordinate.x == 0 + self.boundary:
            leftLimit = True
        else:
            for y in range(coordinate.y, coordinate.y + Height):
                if (self.space.getVertex(coordinate.x - 1, y).isOccupied()):
                    leftLimit = True
                    break

        # 오른편 확인
        if coordinate.x + Width - 1 == self.space.width - 1 - self.boundary:
            rightLimit = True
        else:
            for y in range(coordinate.y, coordinate.y + Height):
                if (self.space.getVertex(coordinate.x + Width, y).isOccupied()):
                    rightLimit = True
                    break

        # 위쪽 확인
        if coordinate.y == 0 + self.boundary:
            upLimit = True
        else:
            for x in range(coordinate.x, coordinate.x + Width):
                if (self.space.getVertex(x, coordinate.y - 1).isOccupied()):
                    upLimit = True
                    break

        # 아래쪽 확인
        if coordinate.y + Height - 1 == self.space.height - 1 - self.boundary:
            bottomLimit = True
        else:
            for x in range(coordinate.x, coordinate.x + Width):
                if (self.space.getVertex(x, coordinate.y + Height).isOccupied()):
                    bottomLimit = True
                    break

        # --------------------------------------------------
        # 현재 화물로 인해 제일 큰 화물 배치가 불가능한 영역을 계산할 것.
        # 그 영역의 x 범위와 y범위를 구해 영역을 계산함.
        # 이때 minX 와 maxX 로 x 범위를 구하고
        # minY 와 maxY 로 y 범위를 구한다

        # boundary 를 확보해야 라우팅이 잘 되기 때문에 boudnary 를 계산한다
        minX = self.boundary
        if (leftLimit):
            # 왼편에 장애물이 있는 경우
            EffectCnt -= 5
            minX = coordinate.x
        elif coordinate.x - self.largestType.width > self.boundary:
            # 왼편에 장애물이 없는 경우
            minX = coordinate.x - self.largestType.width + 1

        # boundary 를 확보해야 라우팅이 잘 되기 때문에 boudnary 를 계산한다
        maxX = self.space.width - 1 - self.boundary
        rightCoordiX = coordinate.x + Width - 1
        if (rightLimit):
            # 오른편에 장애물이 있는 경우
            EffectCnt -= 5
            maxX = rightCoordiX
        if (rightCoordiX + self.largestType.width < self.space.width - self.boundary):
            # 오른편에 장애물이 없는 경우
            maxX = rightCoordiX + self.largestType.width - 1

        minY = self.boundary
        if upLimit:
            # 위쪽에 장애물이 있는 경우
            EffectCnt -= 5
            minY = coordinate.y
        if (coordinate.y - self.largestType.height > self.boundary):
            # 위쪽에 장애물이 없는 경우
            minY = coordinate.y - self.largestType.height + 1

        maxY = self.space.height - 1 - self.boundary
        bottomCoordiY = coordinate.y + Height - 1
        if bottomLimit:
            # 아래쪽에 장애물이 있는 경우
            EffectCnt -= 5
            maxY = bottomCoordiY
        if (bottomCoordiY + self.largestType.height < self.space.height - self.boundary):
            # 아래쪽에 장애물이 없는 경우
            maxY = bottomCoordiY + self.largestType.height - 1

        # 큰 화물 회전 후 측정
        # 위와 같은 코드가 반복 됨

        # x 의 boundary value 1
        minXtr = self.boundary
        if leftLimit:
            EffectCnt -= 5
            minXtr = coordinate.x
        if (coordinate.x - self.largestType.height > self.boundary):
            minXtr = coordinate.x - self.largestType.height + 1
        # 1을 한번 더 빼주는 이유는 한칸 띄워야 라우팅이 잘 되기 때문
        maxXtr = self.space.width - 1 - self.boundary
        rightCoordiXtr = coordinate.x + Width - 1
        if rightLimit:
            EffectCnt -= 5
            maxXtr = rightCoordiX
        if (rightCoordiXtr + self.largestType.height < self.space.width - self.boundary):
            maxXtr = rightCoordiXtr + self.largestType.height - 1

        minYtr = self.boundary
        if upLimit:
            EffectCnt -= 5
            minYtr = coordinate.y
        if (coordinate.y - self.largestType.width > self.boundary):
            minYtr = coordinate.y - self.largestType.width + 1

        maxYtr = self.space.height - 1 - self.boundary
        bottomCoordiYtr = coordinate.y + Height - 1
        if bottomLimit:
            EffectCnt -= 5
            maxYtr = bottomCoordiY
        if (bottomCoordiYtr + self.largestType.width < self.space.height - self.boundary):
            maxYtr = bottomCoordiYtr + self.largestType.width - 1

        cntOcc = 0

        # centerX = (minX+maxX)/2
        # centerY = (minY+maxY)/2
        #
        # xMaxDistance = maxX - centerX
        # yMaxDistance = maxY - centerY
        #
        # maxValue = xMaxDistance + yMaxDistance

        # for X in range(minX, maxX, self.minCargoSize):
        #     for Y in range(minY, maxY, self.minCargoSize):
        #         occufied = self.space.vertexArr[Y][X].isOccupied()
        #
        #         if (occufied):
        #             x = abs(X - centerX)
        #             y = abs(Y - centerY)
        #             # cntOcc += 1 * (1 + maxValue - x - y)
        #             cntOcc += 1

        # 영역을 계산
        process = (maxX - minX) * (maxY - minY) + (maxXtr - minXtr) * (maxYtr - minYtr)

        EffectCnt += (process - cntOcc)
        return EffectCnt

    # 평가요소 2. 입구와의 거리 계산
    def checkEnterDistance(self, Object, coordinate, EntNum):
        # 물체가 해당 좌표에 배치 되었을 경우 입구와 얼마나 멀리 있는지 체크
        # 해당 위치에서 입구까지의 거리를 리턴
        Enters = self.Enters

        # 방향에 따라 가로인지 세로인지 결정
        Width = Object.getWidth()
        Height = Object.getHeight()
        if (Object.isTransformed):  # 돌린 방향
            Width = Object.getHeight()
            Height = Object.getWidth()

        # 화물의
        ObjectCenterX = coordinate.x + Width / 2
        ObjectCenterY = coordinate.y

        # 거리를 계산할 입구를 가져온다
        Enter = Enters[EntNum]

        # 입구와의 거리계산
        # 직선거리로 계산
        EnterCenterX = Enter["coordinate"]["X"] + (Enter["volume"]["width"] / 2)
        EnterCenterY = Enter["coordinate"]["Y"] + (Enter["volume"]["height"] / 2)
        EnterDistance = math.sqrt(abs(ObjectCenterX - EnterCenterX) ** 2 + abs(ObjectCenterY - EnterCenterY) ** 2)

        # 결과값 리턴
        return EnterDistance

    # 차집합 연산.
    # 첫번째 array에 있는 원소들 중 두번째 array에 없는것들만 리턴
    def arrDiff(self, first, second):
        second = set(second)
        return [item for item in first if item not in second]
