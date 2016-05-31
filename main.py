"""
File Name: main.py
Date Created: 05/31/2016
Description: contains top-level instructions for solving TSP
"""
#############################################################
# Imports
#############################################################

import re

#############################################################
# DEBUG
# 1 = ON
# 0 = OFF
#############################################################

DEBUG = 1

#############################################################
# Classes
#############################################################


class Node(object):
    """
    Definition for 2-Dimensional Node object
    id = node id
    x = x coordinate
    y = y coordinate
    """
    id = 0
    x = 0
    y = 0

    def __init__(self, id, x, y):
        """
        Initialize instance of Node object
        with id, x coordinate, y coordinate
        :param id:
        :param x:
        :param y:
        """
        self.id = id
        self.x = x
        self.y = y

#############################################################
# Supplemetal Functions
#############################################################


def readfile(filepath):
    """
    reads from filepath and returns file contents
    :param filepath:
    :return filecontents:
    """
    file = open(filepath, 'r')
    filecontents = file.read()
    filecontents = filecontents.strip()
    return filecontents


def formatmap(filecontents):
    """
    reads filecontents and formats
    :param filecontents:
    :return map:
    """
    map = []
    list = re.split("[\n]",filecontents)
    for i in range(0,len(list)):
        list[i] = re.split("[ ]",list[i])
        map.append(Node(list[i][0], list[i][1], list[i][2]))
    return map


def nodedistance(node):
    """
    returns sum of x and y coordinates of node object
    uses absolute values
    :param node:
    :return node.id, distance):
    """
    distance = abs(node.x) + abs(node.y)
    return node.id, distance

#############################################################
# Main Function
#############################################################


def main():
    if DEBUG:
        # print('Read file test:')
        filepath = 'tsp_example_1.txt'
        filecontents = readfile(filepath)
        map = formatmap(filecontents)
        for i in range(0,len(map)):
            print('id: %s\tx coord: %s\ty coord: %s' % (map[i].id, map[i].x, map[i].y))
    return

main()
