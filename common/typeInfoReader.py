#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
실제 크기를 cell size에 맞게 변경함. 화물 종류 json 을 파싱하여 타입 list 로 변환하는 기능을 제공합니다.
Change real sizes according to the cell size
"""

from common.LayoutInterface import *

TypeInfoPath = "../common/freight_list.json"

# 미리 정해진 화물들의 타입 정보를 읽어오는 클래스
class TypeInfoReader :
    def __init__(self):
        # 정보를 읽어와 변수에 담아둔다
        self.preTypeList = preprocessTypeList(TypeInfoPath)

# 사용 샘플
def main():

    # 생성
    typeReader = TypeInfoReader()

    # 생성 확인
    i = 0
    for type in typeReader.preTypeList:
        i+=1
        print str(i) + " 번째 타입::   width :" + str(type.width) + ", height :" + str(type.height) + ", Wheel base :" + str(type.L) + ", steerAngle :" + str(type.a) + ", minRadius :" + str(type.min_R)

# 타입 리스트를 가져오도록 전처리하는 함수
def preprocessTypeList(typeInfoPath):

    parser = ShipInfoParser()

    typeInfo = readJSON(typeInfoPath)

    tmpTypeList = []

    for type in typeInfo["freight"]["freight_type"]:
        tmpTypeList.append(Type(int(parser.distanceToCellCeil(int(type["Full_width"]))["cellCnt"]),
                                int(parser.distanceToCellCeil(int(type["Full_height"]))["cellCnt"]),
                                int(parser.distanceToCellCeil(int(type["Wheel_base"]))["cellCnt"]),
                                int(type["MAX_steer_angle"])))

    return tmpTypeList


# json 파일을 읽어오는 함수
def readJSON(filename):
    f = open(filename, 'r')
    js = json.loads(f.read())
    f.close()
    return js

if __name__ == '__main__':
    main()
