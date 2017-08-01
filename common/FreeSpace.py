#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Class for handling an available free space of a vessel
"""

from Miscellaneous import *

OBSTACLE_ID = 9
ENTER_ID = 8


# 선박의 공간을 관리하는 클래스
# Class for management free space of a vessel
class Space:
    def __init__(self, floorData, entrancesList, obstaclesList):
        # cell 들을 2차원 배열로 저장할 변수
        self.cellArr = []

        self.width = floorData['width']
        self.length = floorData['length']
        self.height = floorData['height']

        # 2차원 배열에 cell 인스턴스들을 생성한다
        for i in range(self.length):
            self.cellArr.append([])
            for j in range(self.width):
                self.cellArr[i].append(Cell())

        # 입구 정보를 grid 에 배치
        for enter in entrancesList:
            if enter is not None:
                enterObject = Object(ENTER_ID, enter['id'],
                                     Type(enter['volume']['width'], enter['volume']['length'], 0, 50))
                enterCoordinate = Coordinate(enter['coordinate']['X'], enter['coordinate']['Y'])
                self.setObject(enterObject, enterCoordinate)

        # 장애물 정보를 grid 에 배치
        for obstacle in obstaclesList:
            if obstacle is not None:
                obstacleObject = Object(OBSTACLE_ID, obstacle['id'],
                                        Type(obstacle['volume']['width'], obstacle['volume']['length'], 0, 50))
                self.setObject(obstacleObject, Coordinate(obstacle['coordinate']['X'], obstacle['coordinate']['Y']))

    # 현재 레이아웃을 console 에 그리는 함수
    def draw(self):
        for i in range(self.height):
            rowContent = ""
            for j in range(self.width):
                rowContent = rowContent + str(self.cellArr[i][j].getObjectId()) + " "
            print(rowContent)

    # 주어진 좌상단 좌표에서 너비와 높이만큼 비어있는지 확인하는 함수
    def isEmptyArea(self, x, y, width, height):
        for i in range(y, y + height):
            for j in range(x, x + width):
                if (i < self.height) and (j < self.width):
                    if self.cellArr[i][j].isOccupied():
                        return False
        return True

    # 해당 좌표의 vertex를 가져온다.
    def getVertex(self, x, y):
        return self.cellArr[y][x]

    # 주어진 목적지에 Object 를 배치하는 함수
    def setObject(self, obj, coor):
        # Guard condition
        # Object 가 없으면 무시
        if obj is None:
            return False

        # 방향 전환했는지 체크
        if obj.isTransformed:
            length = obj.getWidth()
            width = obj.getLength()
        else:
            length = obj.getLength()
            width = obj.getWidth()

        # 배치 실행
        for i in range(coor.y, coor.y + length):
            for j in range(coor.x, coor.x + width):
                # python 은 call by reference
                self.cellArr[i][j].unit = obj
        return True

    # 주어진 물체를 공간에서 제거하는 함수
    def delObject(self, obj):
        # 주어진 물체가 있는 좌표를 찾아온다
        targetCoord = self.searchObject(obj)

        # Guard condition
        # Object 가 없으면 무시
        if targetCoord is None:
            return False

        # 방향 전환했는지 체크
        if obj.isTransform:
            length = obj.width + targetCoord.y
            width = obj.length + targetCoord.x
        else:
            length = obj.length + targetCoord.y
            width = obj.width + targetCoord.x

        for i in range(targetCoord.y, length):
            for j in range(targetCoord.x, width):
                # None 값으로 해당 좌표에 있는 unit 정보를 없애준다
                self.cellArr[i][j].unit = None
        return True

    # 주어진 Object 를 찾아 Coordinate 를 넘겨주는 함수
    def searchObject(self, obj):
        # Guard condition
        # Object 가 없으면 무시
        if obj is None:
            return None

        # 배열 뒤지기
        for i in range(self.length):
            for j in range(self.width):
                if self.cellArr[i][j].isOccupied() and self.cellArr[i][j].isSameObject(obj):
                    # 찾는 좌표 리턴
                    return Coordinate(i, j)
        # 찾는것이 없다면 None 리턴
        return None
