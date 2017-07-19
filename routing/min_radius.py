# -*- coding: utf-8 -*-

import math


# 최소 회전반경 게산 함수
# Function for calculation the minimum turning radius of a car
def cal_radius(L, a):
    L = float(L)
    a = float(a)
    a = math.radians(a)  # from degrees to radians
    R = L / math.sin(a)
    return R


def pythagoras(min_R, L):
    min_R = float(min_R * min_R)
    L = float(L * L)
    radius = min_R - L
    radius = math.sqrt(radius)
    return radius
