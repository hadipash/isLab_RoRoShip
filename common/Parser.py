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
        self.ShipInfo = Ship(int(configJSON["shipSize"]["width"]), int(configJSON["shipSize"]["height"]))

        # 입구 정보를 리스트로 관리
        # List of entrances
        self.EnterInfoList = []
        for enterInfo in configJSON["enterInfo"]["positions"]:
            self.EnterInfoList.append(Enter(Coordinate(enterInfo["coordinate"]["X"], enterInfo["coordinate"]["Y"]),
                                            enterInfo["volume"]["width"],
                                            enterInfo["volume"]["height"],
                                            enterInfo["id"]))

        # 장애물 정보를 리스트로 관리
        # List of obstacles on a vessel
        self.ObstacleInfoList = []
        for obstacleInfo in configJSON["obstacleInfo"]["positions"]:
            self.ObstacleInfoList.append(
                Obstacle(Coordinate(obstacleInfo["coordinate"]["X"], obstacleInfo["coordinate"]["Y"]),
                         obstacleInfo["volume"]["width"],
                         obstacleInfo["volume"]["height"],
                         obstacleInfo["id"]))

    # json 파일을 읽어오는 함수
    def readJSON(self, filename):
        f = open(filename, 'r')
        js = json.loads(f.read())
        f.close()
        return js

    # 배의 정보를 cell로 변환해서 json 데이터로 리턴
    def parseShipInfo(self):
        shipJSONData = {"width": self.distanceToCellFloor(self.ShipInfo.width)["cellCnt"],
                        "height": self.distanceToCellFloor(self.ShipInfo.height)["cellCnt"]}
        return shipJSONData

    # 입구들의 좌표와 크기를 cell로 변환해서 json 리스트로 리턴
    def parseEnterInfo(self):
        enterList = []
        for enterData in self.EnterInfoList:
            enterJSONData = self.parseObstacle(enterData)
            enterList.append(enterJSONData)

        return enterList

    # 장애물들의 좌표와 크기를 cell로 변환해서 json 리스트로 리턴
    def parseObstacleInfo(self):
        obstacleList = []
        for obstacleData in self.ObstacleInfoList:
            obstacleJSONData = self.parseObstacle(obstacleData)

            # obstacleList.append(json.dump(obstacleJSONData))
            obstacleList.append(obstacleJSONData)

        return obstacleList

    # 장애물들의 좌표와 크기를 cell로 변환
    def parseObstacle(self, obstacleData):
        obstacleJSONData = {}
        obstacleJSONData["coordinate"] = {}
        obstacleJSONData["volume"] = {}

        coordinateXData = self.distanceToCellFloor(obstacleData.coordinate.x)
        obstacleJSONData["coordinate"]["X"] = coordinateXData["cellCnt"]

        coordinateYData = self.distanceToCellFloor(obstacleData.coordinate.y)
        obstacleJSONData["coordinate"]["Y"] = coordinateYData["cellCnt"]

        obstacleJSONData["volume"]["width"] = self.distanceToCellCeil(obstacleData.width +
                                                                      coordinateXData["remain"])["cellCnt"]
        obstacleJSONData["volume"]["height"] = self.distanceToCellCeil(obstacleData.height +
                                                                       coordinateYData["remain"])["cellCnt"]

        obstacleJSONData["id"] = obstacleData.id

        return obstacleJSONData

    # 길이를 cell 로 변환할 때 올림처리 하는 함수
    # json 으로 리턴
    def distanceToCellCeil(self, distance):
        jsonData = {}
        cellCnt = distance / self.standardSize
        if distance % self.standardSize != 0:
            cellCnt = cellCnt + 1

        jsonData["cellCnt"] = cellCnt
        jsonData["remain"] = distance % self.standardSize
        return jsonData

    # 길이를 cell 로 변환할 때 내림처리 하는 함수
    # json 으로 리턴
    def distanceToCellFloor(self, distance):
        jsonData = {}
        cellCnt = distance / self.standardSize
        jsonData["cellCnt"] = cellCnt
        jsonData["remain"] = distance % self.standardSize
        return jsonData

    # 실제 부피로 계산하는 함수
    def convertRealVolume(self, cellCnt):
        return cellCnt * self.standardSize * self.standardSize
