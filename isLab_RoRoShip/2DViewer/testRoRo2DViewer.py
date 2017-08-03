import matplotlib.pyplot as plt

mList = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 2, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 2, 0],
    [2, 0, 2],
    [2, 1, 0],
    [2, 2, 0],
]
plt.figure(1)
for i in range(9):
    if mList[i][2] == 0:
        myFc = 'w'
    elif mList[i][2] == 1:
        myFc = 'r'
    elif mList[i][2] == 2:
        myFc = 'b'

    rectangle = plt.Rectangle((mList[i][0], mList[i][1]), height = 1, width = 1, fc = myFc, ec = 'black')
    plt.gca().add_patch(rectangle)
plt.axis('scaled')

plt.figure(2)
for i in range(9):
    if mList[i][2] == 0:
        myFc = 'white'
    elif mList[i][2] == 1:
        myFc = 'red'
    elif mList[i][2] == 2:
        myFc = 'black'

    rectangle = plt.Rectangle((mList[i][0], mList[i][1]), height = 1, width = 1, fc = myFc, ec = 'black')
    plt.gca().add_patch(rectangle)
plt.axis('scaled')

plt.figure(3)
for i in range(9):
    if mList[i][2] == 0:
        myFc = 'w'
    elif mList[i][2] == 1:
        myFc = 'r'
    elif mList[i][2] == 2:
        myFc = 'green'

    rectangle = plt.Rectangle((mList[i][0], mList[i][1]), height = 1, width = 1, fc = myFc, ec = 'black')
    plt.gca().add_patch(rectangle)
plt.axis('scaled')

plt.show()

