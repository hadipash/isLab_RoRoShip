#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Program to generate cargo list (only for test purposes)
"""

from Parser import *

TYPE_INFO = "../common/freight_list.json"
CARGO_LIST = "../common/cargo_input.json"

NUM_OF_VEHICLES = 690


def main():
    # read number of types
    typeNum = int(Parser.readJSON(TYPE_INFO)["freight"]["cnt"])

    vehicleID = 0

    tempData = []
    for i in range(30):
        item = {"cargoId": vehicleID,
                "cargoType": 4,
                "groupId": 1}
        tempData.append(item)
        vehicleID += 1

    for i in range(30):
        item = {"cargoId": vehicleID,
                "cargoType": 5,
                "groupId": 1}
        tempData.append(item)
        vehicleID += 1

    for i in range(30):
        item = {"cargoId": vehicleID,
                "cargoType": 6,
                "groupId": 1}
        tempData.append(item)
        vehicleID += 1

    for i in range(130):
        item = {"cargoId": vehicleID,
                "cargoType": 3,
                "groupId": 1}
        tempData.append(item)
        vehicleID += 1

    for i in range(200):
        item = {"cargoId": vehicleID,
                "cargoType": 2,
                "groupId": 1}
        tempData.append(item)
        vehicleID += 1

    for i in range(270):
        item = {"cargoId": vehicleID,
                "cargoType": 1,
                "groupId": 1}
        tempData.append(item)
        vehicleID += 1

    # generate json data
    data = {"numOfType": typeNum, "numOfCargo": NUM_OF_VEHICLES, "data": tempData, "numOfGroup": 1}

    json.dump(data, open(CARGO_LIST, 'w'), indent=2)


if __name__ == '__main__':
    main()
