# -*- coding: utf-8 -*-
'''
JSON 파일을 읽어 dic과 dic내의 value를 list로 만들어 저장한다.
'''
import json
from pprint import pprint
def loadInput(filepath):

    cargo_dic = {}
    dic_to_list = []

    with open(filepath) as f:
        for line in f:
            cargo_dic = json.loads(line) # input_data는 json 전체를 dictionary 형태로 저장
            dic_to_list.append(cargo_dic.values()) # cargo_dic 내의 value를 list로 만들어 dic_to_list에 저장

    for i in range(len(dic_to_list)):
        for j in range(3):
            dic_to_list[i][j] = int(dic_to_list[i][j])

    return dic_to_list