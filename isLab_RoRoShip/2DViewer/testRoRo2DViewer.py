import matplotlib.pyplot as plt
import time

class Floor:
    def __init__(self):
        # entrance = [x, y, height, width]
        self.entrance = []

        # pillar = [x, y, height, width]
        self.pillar = []

        # car = [x, y, height, width, type]
        self.car = []

    pass

floor1 = Floor()
floor2 = Floor()
floor3 = Floor()

floors = [floor1, floor2, floor3]

floors[0].entrance.append([0, 0, 1, 1])
floors[1].entrance.append([0, 0, 1, 1])
floors[2].entrance.append([0, 0, 1, 1])

floors[0].pillar.append([1, 1, 1, 1])
floors[1].pillar.append([1, 1, 1, 1])
floors[2].pillar.append([1, 1, 1, 1])

floors[0].car.append([0, 1, 1, 1, 0])
floors[0].car.append([0, 2, 1, 1, 1])
floors[1].car.append([0, 1, 1, 1, 2])
floors[1].car.append([0, 2, 1, 1, 1])
floors[2].car.append([0, 1, 1, 1, 2])
floors[2].car.append([0, 2, 1, 1, 0])

#make empty board
for i in range(3):
    plt.figure(i + 1)
    for j in range(3):
        for k in range(3):
            rectangle = plt.Rectangle((j, k), height=1, width=1, fc='white', ec='black')
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')

#insert entrance
for i in range(3):
    for j in range(len(floors[i].entrance)):
        entranceX = floors[i].entrance[j][0]
        entranceY = floors[i].entrance[j][1]
        entranceHeight = floors[i].entrance[j][2]
        entranceWidth = floors[i].entrance[j][3]

        plt.figure(i + 1)
        rectangle = plt.Rectangle((entranceX, entranceY), height = entranceHeight,
                                  width = entranceWidth, fc = 'gray', ec = 'black')
        plt.gca().add_patch(rectangle)

#insert pillar
for i in range(3):
    for j in range(len(floors[i].pillar)):
        pillarX = floors[i].pillar[j][0]
        pillarY = floors[i].pillar[j][1]
        pillarHeight = floors[i].pillar[j][2]
        pillarWidth = floors[i].pillar[j][3]

        plt.figure(i + 1)
        rectangle = plt.Rectangle((pillarX, pillarY), height = pillarHeight,
                                  width = pillarWidth, fc = 'black', ec = 'black')
        plt.gca().add_patch(rectangle)

#insert car
for i in range(3):
    for j in range(len(floors[i].car)):
        carX = floors[i].car[j][0]
        carY = floors[i].car[j][1]
        carHeight = floors[i].car[j][2]
        carWidth = floors[i].car[j][3]
        carType = floors[i].car[j][4]
        carColor = ''
        if carType == 0:
            carColor = 'red'
        elif carType == 1:
            carColor = 'green'
        elif carType == 2:
            carColor = 'blue'
        plt.figure(i + 1)
        rectangle = plt.Rectangle((carX, carY), height = carHeight,
                                  width = carWidth, fc = carColor, ec = 'black')
        plt.gca().add_patch(rectangle)
plt.show()

