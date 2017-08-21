import matplotlib.pyplot as plt
import common.InitializationCode as ic

# orientation of plots
vertical = False
# array of colors
colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange', 'purple', 'skyblue']


# layout initialization
def plotInitial():
    for i in range(len(ic.floors)):
        plt.figure(i + 1)
        # make empty board
        if vertical:
            rectangle = plt.Rectangle((0, 0), height=ic.floors[i].length, width=ic.floors[i].width,
                                      fc='white', ec='black')
        else:
            rectangle = plt.Rectangle((0, 0), height=ic.floors[i].width, width=ic.floors[i].length,
                                      fc='white', ec='black')
        plt.gca().add_patch(rectangle)

        # insert entrance
        for ent in ic.floors[i].entrances:
            if vertical:
                rectangle = plt.Rectangle((ent.coordinate.x, ent.coordinate.y), height=ent.length,
                                          width=ent.width, fc='gray', ec='black')
            else:
                rectangle = plt.Rectangle((ent.coordinate.y, ent.coordinate.x), height=ent.width,
                                          width=ent.length, fc='gray', ec='black')
            plt.gca().add_patch(rectangle)

        # insert pillar
        for obs in ic.floors[i].obstacles:
            if vertical:
                rectangle = plt.Rectangle((obs.coordinate.x, obs.coordinate.y), height=obs.length,
                                          width=obs.width, fc='black', ec='black')
            else:
                rectangle = plt.Rectangle((obs.coordinate.y, obs.coordinate.x), height=obs.width,
                                          width=obs.length, fc='black', ec='black')
            plt.gca().add_patch(rectangle)

        # insert notLoadable
        for nLoad in ic.floors[i].notLoadable:
            if vertical:
                rectangle = plt.Rectangle((nLoad.coordinate.x, nLoad.coordinate.y), height=nLoad.length,
                                          width=nLoad.width, fc='whitesmoke', ec='black')
            else:
                rectangle = plt.Rectangle((nLoad.coordinate.y, nLoad.coordinate.x), height=nLoad.width,
                                          width=nLoad.length, fc='whitesmoke', ec='black')
            plt.gca().add_patch(rectangle)

        # insert ramps
        for ramp in ic.floors[i].ramps:
            if vertical:
                rectangle = plt.Rectangle((ramp.coordinate.x, ramp.coordinate.y), height=ramp.length,
                                          width=ramp.width, fc='midnightblue', ec='black')
            else:
                rectangle = plt.Rectangle((ramp.coordinate.y, ramp.coordinate.x), height=ramp.width,
                                          width=ramp.length, fc='midnightblue', ec='black')
            plt.gca().add_patch(rectangle)

        # insert slopes
        for slope in ic.floors[i].slopes:
            if vertical:
                rectangle = plt.Rectangle((slope.coordinate.x, slope.coordinate.y), height=slope.length,
                                          width=slope.width, fc='lightgray', ec='black')
            else:
                rectangle = plt.Rectangle((slope.coordinate.y, slope.coordinate.x), height=slope.width,
                                          width=slope.length, fc='lightgray', ec='black')
            plt.gca().add_patch(rectangle)

        plt.axis('scaled')


def drawPlots(cars):
    plotInitial()

    # insert car
    for car in cars:
        if car.coordinates.floor != -1:
            carColor = ''
            for i in range(len(ic.typeList)):
                if car.type == ic.typeList[i]:
                    carColor = colors[i]

            plt.figure(car.coordinates.floor + 1)
            if vertical:
                rectangle = plt.Rectangle((car.coordinates.x, car.coordinates.y), height=car.getLength(),
                                          width=car.getWidth(), fc=carColor, ec='black')
            else:
                rectangle = plt.Rectangle((car.coordinates.y, car.coordinates.x), height=car.getWidth(),
                                          width=car.getLength(), fc=carColor, ec='black')
            plt.gca().add_patch(rectangle)

    plt.show()
