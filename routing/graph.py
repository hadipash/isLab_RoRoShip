# -*- coding: utf-8 -*-

# graph vertex & edge py
import graph_m  # update, init, path_chk
from global_Data import *
import numpy as np
#import simul

class graph:
    def __init__(self, Type, Space):
        self.Type = Type
        self.Type.min_R += 2
        self.bump = 0
        if (self.Type.L ==0):
            self.bump = (self.Type.height - 12)/2
        else:
            if self.Type.height % 2 != self.Type.L % 2:
                self.bump = (self.Type.height - self.Type.L - 1) / 2
            else:
                self.bump = (self.Type.height - self.Type.L) / 2
        if self.bump < 1:
             self.bump = 1
        # top-left x, y에 화물이 위치할 수 있는가.
        # self.vertex = [[[0 for state in range(2)] for y in range(ship_grid_height+5)] for x in range(ship_grid_width+5)]  #x = width, y = height => 0, x = height, y = width => 1의 상태
        self.vertex = np.ones(shape=(Space.width, Space.height, 2))
        # top-left x, y에서 도달 가능한 좌표 list
        self.curve = [[[[-1 for co in range(2)] for state in range(8)] for y in range(Space.height)] for state in
                      range(Space.width)]  # 도달가능한 좌표 append / edge
        self.curve = np.array(self.curve)
        # self.curve = np.ones(shape=(ship_width+5,ship_height+5,4))
        self.Space = np.ones(shape=(Space.width, Space.height))
        for x in range(Space.width):
            for y in range(Space.height):
                self.Space[x][y] = Space.cellArr[y][x].isOccupied() # space[50][200] vertex[200][50]
        self.RB = np.zeros(shape=(Space.width, Space.height, 4, 4))
        
        '''
        A = simul.window(Space)
        A.background()
        A.display(Type)
        '''
    def graph_initt(self):

        height = int(self.Type.height)
        width = int(self.Type.width)
        #print "h, L, bump : ", height, self.Type.L, self.bump

        min_R = int(self.Type.min_R)

        traed = int(self.Type.width)
        radius = int(self.Type.radius)
        #print ""
        #print "min, ra : ",min_R, radius
        #print height, width

        # state 1 = up, state 2 = down, state 3 = left, state 4 = right

        ### up down left right available###
        self.vertex, self.curve = graph_m.init(width, height, min_R, radius, self.bump, self.Space)
        
        '''
        for x in range(0, 50):
            for y in range(0, 100):
                print (int)(self.vertex[x][y][0]),
            print
        
        print
        
        for x in range(0, 50):
            for y in range(0, 50):
                for k
                 in range(8):
                    print (int)(self.curve[x][y][k][0]),
                print "|",
            print
        '''

        return True

    ### graph update ###
    def graph_update(self, s_x, s_y, e_x, e_y):

        w, h = self.Type.width, self.Type.height
        min_R = int(self.Type.min_R)
        radius = int(self.Type.radius)

        #print "e_x : " + str(e_x) + ", e_y : " + str(e_y)
        #print s_x, e_x, s_y, e_y
        for x in range(s_x, e_x + 1):
            for y in range(s_y, e_y + 1):
                # self.Space[x][y] = not_available
                self.Space[x][y] = 1#not_available

        self.vertex, self.curve = graph_m.update(s_x, s_y, e_x, e_y, w, h, radius, self.bump, self.vertex,
                                                 self.curve)  # , self.vertex, self.curve) # curve, vertex
        '''
        if(h == 6 and w == 2): 
            for x in range(0, 50):
                for y in range(50, 100):
                    print (int)(self.vertex[x][y][0]),#(int)(self.Space[x][y]),
                print
        
        
        for x in range(0, 50):
            for y in range(0, 50):
                print (int)(self.vertex[x][y][0]),
            print
        
        print
        '''
        return True

    def isPossible(self, s_x, s_y, e_x, e_y, ent_x, ent_y, ent_w, ent_h, _path = 1, _print = 0):
        # print default 값은 출력안함 (0), print 1이면 경로출력!
        w, h = self.Type.width, self.Type.height
        min_R = int(self.Type.min_R)
        re = True
        
        #print " "
        #print "enter ",ent_x, ent_y, ent_w,ent_h
        #print "type :" , w,", ",h
        #print "go to:",s_x,s_y,e_x,e_y
        
        re = graph_m.path_chk(s_x, s_y, e_x, e_y, ent_x, ent_y, ent_w, ent_h, w, h, min_R, self.bump, _path, _print, self.vertex,
                              self.curve)  # curve, vertex
        #re = True
        return re


    def reachability(self, e_x, e_y, ent_w, ent_h):
        w, h = self.Type.width, self.Type.height
        min_R = int(self.Type.min_R)
        self.RB = graph_m.path_list( ent_x, ent_y, ent_w, ent_h, w, h, min_R, self.vertex,
                              self.curve)
        return 1;