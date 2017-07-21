#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
시스템 전반에 사용할 기본 interface
Default system interface
"""

# import wx
# import wx.grid

import json
from routing.min_radius import *

SHIP_LAYOUT_INFO = "../common/inputLayout.json"
OBSTACLE_ID = 9
ENTER_ID = 8


# 화물의 종류를 나타내는 클래스
# Class for defining types of objects to be placed on a vessel
class Type:
    def __init__(self, width, height, wheelbase, steeringAngle):
        self.width = width
        self.height = height

        self.L = wheelbase
        self.a = steeringAngle

        if wheelbase <= 0:
            self.min_R = 12000 / 1000  # standard grid size로 나눠야함.
        else:
            self.min_R = cal_radius(wheelbase, steeringAngle)

        self.min_R = int(math.ceil(self.min_R))
        self.radius = pythagoras(self.min_R, self.L)
        self.radius = int(math.ceil(self.radius))

        # # 축거
        # self.wheelbase = wheelbase
        # # 조향각
        # self.steeringAngle = steeringAngle

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height and self.L == other.L and self.a == other.a


# 물체를 표현하는 클래스
# Class for objects to be placed
class Object:
    def __init__(self, groupId, id, type):
        # 해당 물체의 종류를 나타내는 id
        self.groupId = groupId
        # 해당 물체의 고유 id
        self.id = id
        # 물체의 방향전환 결과
        # Whether an object is rotated or not (default value false)
        self.isTransformed = False
        # 물체의 타입
        self.type = type

    def getWidth(self):
        return self.type.width

    def getHeight(self):
        return self.type.height


# 좌표를 지칭하는데 사용하는 클래스
# Class for a coordinate system
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setCoordinate(self, x, y):
        self.x = x
        self.y = y

    def printCoordinate(self):
        print ("X : " + str(self.x) + ",   Y : " + str(self.y))

    def equal(self, coordinate):
        if (self.x == coordinate.x and self.y == coordinate.y):
            return True
        return False

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y


# gird의 cell에 들어 갈 클래스
# Class for cells
class Vertex:
    def __init__(self):
        # 해당 좌표에 어떤 Obejct 가 있는지 저장하는 변수
        # Saves object located at certain vertex
        self.unit = None

    # 해당 좌표가 이미 선점 되었는지 확인하는 변수
    def isOccupied(self):
        if self.unit != None:
            return True
        else:
            return False

    # 해당 좌표에 존재하는 Object의 Id 를 리턴
    # Return object's id located at certain coordinates
    def getObjectId(self):
        if self.unit != None:
            return self.unit.id
        else:
            return 0

    # 같은 Obejct 인지 확인
    def isSameObject(self, Object):
        if self.unit.id == Object.id:
            return True
        else:
            return False


# 선박의 공간을 관리하는 클래스
# Class for management free space of a vessel
class Space:
    def __init__(self):
        # vertex 들을 2차원 배열로 저장할 변수
        self.vertexArr = []

        # 파서를 사용하여 선박의 정보를 가져온다
        parser = ShipInfoParser()
        self.width = int(parser.parseShipInfo()["width"])
        self.height = int(parser.parseShipInfo()["height"])

        # 2차원 배열에 vertex 인스턴스들을 생성한다
        for i in range(self.height):
            self.vertexArr.append([])
            for j in range(self.width):
                self.vertexArr[i].append(Vertex())

        # 입구 정보를 grid 에 배치
        enterInfo = parser.parseEnterInfo()
        for enter in enterInfo:
            enterObject = Object(ENTER_ID, enter["id"],
                                 Type(enter["volume"]["width"], enter["volume"]["height"], 0, 50))
            enterCoordinate = Coordinate(enter["coordinate"]["X"], enter["coordinate"]["Y"])
            self.setObject(enterObject, enterCoordinate)

        # 장애물 정보를 grid 에 배치
        obstacleInfo = parser.parseObstacleInfo()
        for obstacle in obstacleInfo:
            obstacleObject = Object(OBSTACLE_ID, obstacle["id"],
                                    Type(obstacle["volume"]["width"], obstacle["volume"]["height"], 0, 50))
            self.setObject(obstacleObject, Coordinate(obstacle["coordinate"]["X"], obstacle["coordinate"]["Y"]))

    # 현재 레이아웃을 console 에 그리는 함수
    def draw(self):
        for i in range(self.height):
            rowContent = ""
            for j in range(self.width):
                rowContent = rowContent + str(self.vertexArr[i][j].getObjectId()) + " "
            print(rowContent)

    # 주어진 좌표에서 너비와 높이만큼 비어있는지 확인하는 함수
    def isEmptyArea(self, coordinate, width, height):
        for i in range(coordinate.y, coordinate.y + height + 1):
            for j in range(coordinate.x, coordinate.x + width + 1):
                if ((i < self.height) and (j < self.width)):
                    if self.vertexArr[i][j].isOccupied():
                        return False
        return True

    # 주어진 좌상단 좌표에서 너비와 높이만큼 비어있는지 확인하는 함수
    def isEmptyAreaWithXY(self, x, y, width, height):
        for i in range(y, y + height):
            for j in range(x, x + width):
                if ((i < self.height) and (j < self.width)):
                    if self.vertexArr[i][j].isOccupied():
                        return False
        return True

    # 해당 좌표의 vertex를 가져온다.
    def getVertex(self, coordinate):
        return self.vertexArr[coordinate.y][coordinate.x]

    # 해당 좌표의 vertex를 가져온다. 이 때 좌표 객체가 아닌 단순히 x 와 y 값을 이용
    def getVertexx(self, x, y):
        return self.vertexArr[y][x]

    # 주어진 목적지에 Object 를 배치하는 함수
    def setObject(self, Object, Coordinate):
        # Guard condition
        # Object 가 없으면 무시
        if Object == None:
            return False

        # 방향 전환했는지 체크
        if (Object.isTransformed):
            height = Object.getWidth()
            width = Object.getHeight()
        else:
            height = Object.getHeight()
            width = Object.getWidth()

        # 배치 실행
        for i in range(Coordinate.y, Coordinate.y + height):
            for j in range(Coordinate.x, Coordinate.x + width):
                # python 은 call by reference
                self.vertexArr[i][j].unit = Object
        return True

    # 주어진 물체를 공간에서 제거하는 함수
    def delObject(self, Object):
        # 주어진 물체가 있는 좌표를 찾아온다
        targetCoord = self.searchObject(Object)

        # Guard condition
        # Object 가 없으면 무시
        if targetCoord == None:
            return False

        # 방향 전환했는지 체크
        if (Object.isTransform):
            height = Object.width + Coordinate.y
            width = Object.height + Coordinate.x
        else:
            height = Object.height + Coordinate.y
            width = Object.width + Coordinate.x

        for i in range(targetCoord.y, height):
            for j in range(targetCoord.x, width):
                # None 값으로 해당 좌표에 있는 unit 정보를 없애준다
                self.vertexArr[i][j].unit = None
        return True

    # 주어진 Object 를 찾아 Coordinate 를 넘겨주는 함수
    def searchObject(self, Object):
        # Guard condition
        # Object 가 없으면 무시
        if Object == None:
            return None

        # 배열 뒤지기
        for i in range(self.height):
            for j in range(self.width):
                if (self.vertexArr[i][j].isOccupied() & self.vertexArr[i][j].isSameObject(Object)):
                    # 찾는 좌표 리턴
                    return Coordinate(i, j)
        # 찾는것이 없다면 None 리턴
        return None


# 선박의 정보를 파싱하는 클래스
# Class for retrieving information about a vessel from a json file
class ShipInfoParser:
    def __init__(self):
        # json 파일을 읽고 정보를 저장
        configJSON = self.readJSON(SHIP_LAYOUT_INFO)
        self.standradSize = configJSON["standardSize"]
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
        shipJSONData = {}
        shipJSONData["width"] = self.distanceToCellFloor(self.ShipInfo.width)["cellCnt"]
        shipJSONData["height"] = self.distanceToCellFloor(self.ShipInfo.height)["cellCnt"]
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

        obstacleJSONData["volume"]["width"] = self.distanceToCellCeil(obstacleData.width + coordinateXData["remain"])["cellCnt"]
        obstacleJSONData["volume"]["height"] = self.distanceToCellCeil(obstacleData.height + coordinateYData["remain"])["cellCnt"]

        obstacleJSONData["id"] = obstacleData.id

        return obstacleJSONData

    # 길이를 cell 로 변환할 때 올림처리 하는 함수
    # json 으로 리턴
    def distanceToCellCeil(self, distance):
        jsonData = {}
        cellCnt = distance / self.standradSize
        if (distance % self.standradSize != 0):
            cellCnt = cellCnt + 1

        jsonData["cellCnt"] = cellCnt
        jsonData["remain"] = distance % self.standradSize
        return jsonData

    # 길이를 cell 로 변환할 때 내림처리 하는 함수
    # json 으로 리턴
    def distanceToCellFloor(self, distance):
        jsonData = {}
        cellCnt = distance / self.standradSize
        jsonData["cellCnt"] = cellCnt
        jsonData["remain"] = distance % self.standradSize
        return jsonData

    # 실제 부피로 계산하는 함수
    def convertRealVolume(self, cellCnt):
        return cellCnt * self.standradSize * self.standradSize


# 선박 클래스
class Ship:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# 장애물 클래스
class Obstacle:
    def __init__(self, coordinate, width, height, id):
        self.coordinate = coordinate
        self.width = width
        self.height = height
        self.isEnter = False
        self.id = id


# 입구 클래스
class Enter(Obstacle):
    def __init__(self, coordinate, width, height, id):
        Obstacle.__init__(self, coordinate, width, height, id)
        self.isEnter = True
