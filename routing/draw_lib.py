# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

##### color def #####

BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED2 = (236,112,99)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DEEP_GRAY = (66,73,73)
WHITE = (255,255,255)
PINK = (247,17,128)
PURPLE = (162,22,237)

BGC = WHITE #Back ground color

##### color def #####

dash_size = 4

####################### dashed line #######################

def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

####################### dashed line #######################

####################### opengl lib #######################

def gl_set(width,height):  
    glDisable(GL_DEPTH_TEST)  
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    glOrtho(0, width, height, 0, 0, 1)  
    glMatrixMode(GL_MODELVIEW)

def leftInFrame(FRAME_RATE = 24):
    leftInFrame.next_time = 0
    now = pygame.time.get_ticks()
    if leftInFrame.next_time <= now:
        leftInFrame.next_time = now + FRAME_RATE
        return 0
    return leftInFrame.next_time - now

def draw(x,y,width,height):  
    glBegin(GL_QUADS)  
    glVertex2f(x,y);  
    glVertex2f(x+width,y);  
    glVertex2f(x+width,y+height);  
    glVertex2f(x,y+height);  
    glEnd();  

def draw_line(x,y,width,height):  
    glBegin(GL_LINES)  
    glVertex2f(x,y);  
    glVertex2f(x+width,y+height);  
    glEnd();
'''
0 -> 1 0~ 90 d (+90)
1 -> 2 90 180 d (+90)
2 -> 3 180~ 270 d (+90)
3 -> 0 270 0 d (+90)
'''
def rotate(center_x, center_y, angle):
    glTranslate( center_x , center_y, 0)
    glRotate(angle ,0,0,1 )
    glTranslate( -center_x, -center_y, 0)

def draw_rotate(center_x, center_y, n_angle, e_angle, x,y,width,height):
    degree = n_angle
    if (e_angle > 0):
        set_d = 15
    else:
        set_d = -15
    if(degree != e_angle):
        rotate(center_x, center_y, degree+set_d)
        draw(x,y,width,height)
        degree += set_d
    return degree

####################### opengl lib #######################