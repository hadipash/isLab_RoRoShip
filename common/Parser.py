#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Classes and functions to parse json files
"""

import json
from Miscellaneous import *

SHIP_LAYOUT_INFO = "../common/inputLayout.json"
TYPE_INFO = "../common/freight_list.json"


# 선박의 정보를 파싱하는 클래스
# Class for retrieving information about a vessel and cargoes types from json files
class Parser:
    def __init__(self):
        # Variables for parse a ship
        self.floors = []
        self.typeList = []

        self.parseShipInformation()
        self.parseTypeInformation()

    def parseShipInformation(self):
        # json 파일을 읽고 정보를 저장
        configJSON = self.readJSON(SHIP_LAYOUT_INFO)

        # Get information about floors
        FloorInfoList = []
        for floor in configJSON["loadingSpaceList"]["loadingSpace"]:
            FloorInfoList.append(Floor(floor["width"], floor["length"], floor["height"]))

        # 입구 정보를 리스트로 관리
        # List of entrances
        EnterInfoList = []
        for enterInfo in configJSON["enterList"]["enter"]:
            flNum = enterInfo["floor"]
            EnterInfoList[flNum].append(
                Enter(Coordinate(enterInfo["coordinate"]["X"], enterInfo["coordinate"]["Y"]),
                      enterInfo["volume"]["width"],
                      enterInfo["volume"]["length"],
                      enterInfo["id"]))

        # 장애물 정보를 리스트로 관리
        # List of obstacles on a vessel
        ObstacleInfoList = []
        for obstacleInfo in configJSON["obstacleList"]["obstacle"]:
            flNum = obstacleInfo["floor"]
            ObstacleInfoList[flNum].append(
                Obstacle(Coordinate(obstacleInfo["coordinate"]["X"], obstacleInfo["coordinate"]["Y"]),
                         obstacleInfo["volume"]["width"],
                         obstacleInfo["volume"]["length"],
                         obstacleInfo["id"]))

        # Create array of available space and entrances/obstacles in each floor
        for i in range(0, len(FloorInfoList)):
            self.floors.append(Space(
                FloorInfoList[i],
                EnterInfoList[i],
                ObstacleInfoList[i]
            ))

    def parseTypeInformation(self):
        configJSON = self.readJSON(TYPE_INFO)

        for t in configJSON["freight"]["freight_type"]:
            self.typeList.append(Type(t["Full_width"], t["Full_height"], t["Wheel_base"], t["MAX_steer_angle"]))

    # json 파일을 읽어오는 함수
    def readJSON(self, filename):
        f = open(filename, 'r')
        js = json.loads(f.read())
        f.close()
        return js
