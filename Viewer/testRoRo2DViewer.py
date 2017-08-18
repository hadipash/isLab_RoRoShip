import matplotlib.pyplot as plt
import time
import common.InitializationCode as ic


def drawPlots(cars):
    # make empty board
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for j in range(0, ic.floors[i].width):
            for k in range(0, ic.floors[i].length):
                rectangle = plt.Rectangle((j, k), height=1, width=1, fc='white', ec='black')
                plt.gca().add_patch(rectangle)
            plt.axis('scaled')

    # insert entrance
    for i in range(len(ic.floors)):
        for ent in ic.floors[i].entrances:
            entranceX = ent.coordinate.x
            entranceY = ent.coordinate.y
            entranceHeight = ent.length
            entranceWidth = ent.width

            plt.figure(i + 1)
            rectangle = plt.Rectangle((entranceX, entranceY), height=entranceHeight,
                                      width=entranceWidth, fc='gray', ec='black')
            plt.gca().add_patch(rectangle)

    # insert pillar
    for i in range(len(ic.floors)):
        for obs in ic.floors[i].obstacles:
            pillarX = obs.coordinate.x
            pillarY = obs.coordinate.y
            pillarHeight = obs.length
            pillarWidth = obs.width

            plt.figure(i + 1)
            rectangle = plt.Rectangle((pillarX, pillarY), height=pillarHeight,
                                      width=pillarWidth, fc='black', ec='black')
            plt.gca().add_patch(rectangle)

    # insert car
    for i in range(len(ic.floors)):
        for car in cars:
            carX = car.coordinates.x
            carY = car.coordinates.y
            carHeight = car.getLength()
            carWidth = car.getWidth()
            carType = car.type

            if carType == 0:
                carColor = 'red'
            elif carType == 1:
                carColor = 'green'
            elif carType == 2:
                carColor = 'blue'
            else:
                carColor = 'yellow'

            plt.figure(i + 1)
            rectangle = plt.Rectangle((carX, carY), height=carHeight,
                                      width=carWidth, fc=carColor, ec='black')
            plt.gca().add_patch(rectangle)
plt.show()
