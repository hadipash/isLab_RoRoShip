#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
실제 크기를 cell size에 맞게 변경함. 화물 종류 json 을 파싱하여 타입 list 로 변환하는 기능을 제공합니다.
Change real sizes according to the cell size
"""

from Miscellaneous import Type

TypeInfoPath = "../common/freight_list.json"


# 미리 정해진 화물들의 타입 정보를 읽어오는 클래스
# Class for reading types of cargoes
class TypeInfoReader:
    def __init__(self, parser):
        self.parser = parser
        # 정보를 읽어와 변수에 담아둔다
        self.preTypeList = self.preprocessTypeList()

    # 타입 리스트를 가져오도록 전처리하는 함수
    def preprocessTypeList(self):
        typeInfo = self.parser.readJSON(TypeInfoPath)

        tmpTypeList = []

        for t in typeInfo["freight"]["freight_type"]:
            tmpTypeList.append(Type(int(self.parser.distanceToCellCeil(int(t["Full_width"]))['cellCnt']),
                                    int(self.parser.distanceToCellCeil(int(t["Full_height"]))['cellCnt']),
                                    int(self.parser.distanceToCellCeil(int(t["Wheel_base"]))['cellCnt']),
                                    int(t["MAX_steer_angle"])))

        return tmpTypeList
