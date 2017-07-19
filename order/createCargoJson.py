# -*- coding: utf-8 -*-

import random
import json

numOfCargo = input("Please input the number of cargo ")

numOfCargoType = input("Please input the number of cargo type ")
listOfCargoType = [0]
i = 1
extraCargo = numOfCargo
checkNumOfCargoType = 0
while i <= numOfCargoType :
    cargoType = input("Please input %d th type's number of cargo (extra cargo is %d)" % (i, extraCargo))
    listOfCargoType.append(cargoType)
    extraCargo = extraCargo - cargoType
    checkNumOfCargoType = checkNumOfCargoType + cargoType
    i = i + 1
if checkNumOfCargoType != numOfCargo :
    exit(-1)

numOfGroupType = input("Please input the number of group type ")
listOfGroupType = [0]
i = 1
extraCargo = numOfCargo
checkNumOfCargoGroup = 0
while i <= numOfGroupType :
    groupType = input("Please input %d th group's number of cargo (extra cargo is %d)" % (i, extraCargo))
    listOfGroupType.append(groupType)
    extraCargo = extraCargo - groupType
    checkNumOfCargoGroup = checkNumOfCargoGroup+ groupType
    i = i + 1
if checkNumOfCargoGroup != numOfCargo :
    exit(-1)

cargoId = 0
file = open('cargo_input.json', 'w')
file.close()
file = open('cargo_input.json', 'a')

jsonLine = json.dumps({"NumberOfCargo": numOfCargo, "NumberOfType": numOfCargoType, "NumberOfGroup": numOfGroupType})
print jsonLine
file.write(jsonLine + "\n")

while cargoId < numOfCargo:

    cargoType
    while 1:
        cargoType = random.randint(1, numOfCargoType)
        if listOfCargoType[cargoType] != 0:
            listOfCargoType[cargoType] = listOfCargoType[cargoType] - 1
            break

    groupType
    while 1:
        groupType = random.randint(1, numOfGroupType)
        if listOfGroupType[groupType] != 0:
            listOfGroupType[groupType] = listOfGroupType[groupType] - 1
            break

    jsonLine = json.dumps({"cargoId" :  cargoId , "cargoType"  : cargoType , "groupId" :groupType})
    print jsonLine

    file.write(jsonLine + "\n")

    cargoId = cargoId + 1

file.close()