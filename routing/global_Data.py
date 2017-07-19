# -*- coding: utf-8 -*-

#import os
#os.system("python position/layout_info.py")

#from draw_lib import *
#from graph import *

import math
import numpy as np

# state 1 = up, state 2 = down, state 3 = left, state 4 = right
up = 1
down = 2
left = 3
right = 4

available = 1
not_available = 0
#print ship_width,ship_height,grid_size

#enter_info = enter_info()
#obstacle_info = obs_info()

'''
for x in enter_info:
        print "enter_x, enter_y : " + str(x['coordinate']['X']) +", "+ str(x['coordinate']['Y'])
        print "enter_Vol_width, enter_Vol_height  : " + str(x['volume']['width']) +", "+ str(x['volume']['height'])
        print 1234
for x in obstacle_info:
        print "obstarcle_x, obstarcle_y : " + str(x['coordinate']['X']) +", "+ str(x['coordinate']['Y'])
        print "obstarcle_Vol_width, obstarcle_Vol_height  : " + str(x['volume']['width']) +", "+ str(x['volume']['height'])
'''

'''

grid x,y, state 일 경우 top-left가 x, y이고 
state 1, 2은 (width(x), height(y))이고 state 3, 4는 (height(x), width(y))이다.

'''
