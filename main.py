"""
File Name: main.py
Date Created: 05/31/2016
Description: contains top-level instructions for solving TSP
"""
#############################################################
# Imports
#############################################################

import re
import math

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
    nodeid = node id
    x = x coordinate
    y = y coordinate
    """
    nodeid = 0
    x = 0
    y = 0

    def __init__(self, nodeid, x, y):
        """
        Initialize instance of Node object
        with nodeid, x coordinate, y coordinate
        :param nodeid:
        :param x:
        :param y:
        """
        self.nodeid = nodeid
        self.x = x
        self.y = y


class TSPMatrix(object):
    """
    Definition for Matrix object
    matrixid = new id for connection
    originid = origin node id
    destinationid = destination node id
    distsaince = distance from origin to destination
    """
    matrixid = 0
    originid = 0
    destinationid = 0
    distance = 0

    def __init__(self, matrixid, originid, destinationid, distance):
        """
        initialize instance of TSPMatrix object
        with id, originid, destinationid, distance
        :param id:
        :param originid:
        :param destinationid:
        :param distance:
        """
        self.matrixid = matrixid
        self.originid = originid
        self.destinationid = destinationid
        self.distance = distance

#############################################################
# Supplemental Functions
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
        map.append(Node(int(list[i][0]), int(list[i][1]), int(list[i][2])))
    return map


def nodedistance(origin, destination):
    """
    returns Euclidean distance between origin and destination
    uses absolute values
    :param origin, destination:
    :return origin.id, destination.id, distance):
    """
    distance = int(round(math.sqrt(math.pow((origin.x - destination.x), 2) + math.pow((origin.y - destination.y), 2))))
    return origin.nodeid, destination.nodeid, distance


def connectmap(map):
    """
    connects all points in a map object
    returns a list of connections
    :param map:
    :return connections:
    """
    connections = []
    count = 0
    for i in range(0, len(map)):
        for j in range(i, len(map)):
            originid, destinationid, distance = nodedistance(map[i],map[j])
            connections.append(TSPMatrix(count, originid, destinationid, distance))
            count += 1
    return connections

#############################################################
# Main Function
#############################################################


def main():
    if DEBUG:
        filepath = 'tsp_example_1.txt'
        filecontents = readfile(filepath)
        map = formatmap(filecontents)
        for i in range(0, len(map)):
            print('[map] id: %d\tx coord: %d\ty coord: %d' % (map[i].nodeid, map[i].x, map[i].y))
        connections = connectmap(map)
        for i in range(0, len(connections)):
            print('[connections] id: %d\torigin id: %d\tdestination id: %d\tdistance: %d'
                  % (connections[i].matrixid, connections[i].originid, connections[i].destinationid, connections[i].distance))
    return

main()
