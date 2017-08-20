import matplotlib.pyplot as plt
import common.InitializationCode as ic

def drawPlots(cars):
    # make empty board

    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        rectangle = plt.Rectangle((0, -ic.floors[i].length), height=ic.floors[i].length, width=ic.floors[i].width, fc='white', ec='black')
        plt.gca().add_patch(rectangle)
        #plt.axis('scaled')

    # insert entrance
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for ent in ic.floors[i].entrances:
            entranceX = ent.coordinate.x
            entranceY = ent.coordinate.y
            entranceHeight = ent.length
            entranceWidth = ent.width

            rectangle = plt.Rectangle((entranceX, -(entranceY + entranceHeight)), height=entranceHeight,
                                      width=entranceWidth, fc='gray', ec='black')
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')

    # insert pillar
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for obs in ic.floors[i].obstacles:
            pillarX = obs.coordinate.x
            pillarY = obs.coordinate.y
            pillarHeight = obs.length
            pillarWidth = obs.width

            rectangle = plt.Rectangle((pillarX, -(pillarY + pillarHeight)), height=pillarHeight,
                                      width=pillarWidth, fc='black', ec='black')
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')
    # TODO: add also ic.floors[i].notLoadable, ic.floors[i].ramps, ic.floors[i].slopes
    # ic.floors[i].decks ignore for this moment

    #insert notLoadble
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for nLoad in ic.floors[i].notLoadable:
            nLoadX = nLoad.coordinate.x
            nLoadY = nLoad.coordinate.y
            nLoadHeight = nLoad.length
            nLoadWidth = nLoad.width

            rectangle = plt.Rectangle((nLoadX, -(nLoadY + nLoadHeight)), height=nLoadHeight,
                                      width=nLoadWidth, fc='orange', ec='black')
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')

    # insert ramps
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for ramp in ic.floors[i].ramps:
            rampX = ramp.coordinate.x
            rampY = ramp.coordinate.y
            rampHeight = ramp.length
            rampWidth = ramp.width

            rectangle = plt.Rectangle((rampX, -(rampY + rampHeight)), height=rampHeight,
                                          width=rampWidth, fc='purple', ec='black')
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')

    # insert slopes
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for slope in ic.floors[i].slopes:
            slopeX = slope.coordinate.x
            slopeY = slope.coordinate.y
            slopeHeight = slope.length
            slopeWidth = slope.width

            rectangle = plt.Rectangle((slopeX, -(slopeY + slopeHeight)), height=slopeHeight,
                                          width=slopeWidth, fc='gray', ec='black')
            plt.gca().add_patch(rectangle)
        plt.axis('scaled')

    # insert car
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        for car in cars:
            carFloor = car.coordinates.floor
            carX = car.coordinates.x
            carY = car.coordinates.y
            carHeight = car.getLength()
            carWidth = car.getWidth()
            carType = car.getType()
            carColor = ''

            if carType == "Compact_Car":
                carColor = 'red'
            elif carType == "Midsize_Car":
                carColor = 'green'
            elif carType == "Large_Car":
                carColor = 'blue'
            elif carType == "Bus":
                carColor = 'yellow'
            elif carType == "Excavator":
                carColor = 'blue'
            elif carType == "Wheel_Loaders":
                carColor = 'skyblue'

            if carFloor == i:
                rectangle = plt.Rectangle((carX, -(carY + carHeight)), height=carHeight,
                                      width=carWidth, fc=carColor, ec='black')
                plt.gca().add_patch(rectangle)

        plt.axis('scaled')
    plt.show()