#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Classes and functions to parse json files
"""

import json
from FreeSpace import *

SHIP_LAYOUT_INFO = "../common/inputLayout.json"


# 선박의 정보를 파싱하는 클래스
# Class for retrieving information about a vessel from a json file
class Parser:
    def __init__(self):
        # json 파일을 읽고 정보를 저장
        configJSON = self.readJSON(SHIP_LAYOUT_INFO)
        self.standardSize = configJSON["standardSize"]

        # Get information about floors
        self.FloorInfoList = []
        for floor in configJSON["loadingSpaceList"]["loadingSpace"]:
            self.FloorInfoList.append(Floor(floor["width"], floor["length"], floor["height"]))

        # 입구 정보를 리스트로 관리
        # List of entrances
        self.EnterInfoList = []
        for enterInfo in configJSON["enterList"]["enter"]:
            flNum = enterInfo["floor"]
            self.EnterInfoList[flNum].append(
                Enter(Coordinate(enterInfo["coordinate"]["X"], enterInfo["coordinate"]["Y"]),
                      enterInfo["volume"]["width"],
                      enterInfo["volume"]["length"],
                      enterInfo["id"]))

        # 장애물 정보를 리스트로 관리
        # List of obstacles on a vessel
        self.ObstacleInfoList = []
        for obstacleInfo in configJSON["obstacleList"]["obstacle"]:
            flNum = obstacleInfo["floor"]
            self.ObstacleInfoList[flNum].append(
                Obstacle(Coordinate(obstacleInfo["coordinate"]["X"], obstacleInfo["coordinate"]["Y"]),
                         obstacleInfo["volume"]["width"],
                         obstacleInfo["volume"]["length"],
                         obstacleInfo["id"]))

        # Convert all data about floors, entrances and obstacles into cell representation
        self.floors = []
        for i in range(0, len(self.FloorInfoList)):
            self.floors.append(Space(
                self.parseFloorInfo(self.FloorInfoList[i]),
                self.parseEnterInfo(self.EnterInfoList[i]),
                self.parseObstacleInfo(self.ObstacleInfoList[i])
            ))

    # json 파일을 읽어오는 함수
    def readJSON(self, filename):
        f = open(filename, 'r')
        js = json.loads(f.read())
        f.close()
        return js

    # 배의 정보를 cell로 변환해서 dictionary로 리턴
    def parseFloorInfo(self, floor):
        floorData = {'width': self.distanceToCellFloor(floor.width)['cellCnt'],
                     'length': self.distanceToCellFloor(floor.length)['cellCnt'],
                     'height': floor.height}
        return floorData

    # 입구들의 좌표와 크기를 cell로 변환해서 dictionary로 리턴
    def parseEnterInfo(self, entrances):
        enterList = []

        for enterData in entrances:
            enterList.append(self.parseObstacle(enterData))

        return enterList

    # 장애물들의 좌표와 크기를 cell로 변환해서 dictionary로 리턴
    def parseObstacleInfo(self, obstacles):
        obstacleList = []

        for obstacleData in obstacles:
            obstacleList.append(self.parseObstacle(obstacleData))

        return obstacleList

    # 장애물들의 좌표와 크기를 cell로 변환
    def parseObstacle(self, obstacleData):
        x = self.distanceToCellFloor(obstacleData.coordinate.x)
        y = self.distanceToCellFloor(obstacleData.coordinate.y)

        obstacle = {
            'coordinate': {
                'X': x['cellCnt'],
                'Y': y['cellCnt']
            },
            'volume': {
                'width': self.distanceToCellCeil(obstacleData.width + x['remain'])['cellCnt'],
                'length': self.distanceToCellCeil(obstacleData.length + y['remain'])['cellCnt']
            },
            'id': obstacleData.id
        }

        return obstacle

    # 길이를 cell 로 변환할 때 올림처리 하는 함수
    def distanceToCellCeil(self, distance):
        quotient = distance / self.standardSize
        remainder = distance % self.standardSize

        data = {'cellCnt': (quotient + 1 if remainder else quotient),
                'remain': remainder}

        return data

    # 길이를 cell 로 변환할 때 내림처리 하는 함수
    def distanceToCellFloor(self, distance):
        data = {'cellCnt': distance / self.standardSize,
                'remain': distance % self.standardSize}
        return data

    # 실제 부피로 계산하는 함수
    def convertRealVolume(self, cellCnt):
        return cellCnt * self.standardSize * self.standardSize
