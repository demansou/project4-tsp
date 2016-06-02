"""
File Name: main.py
Date Created: 05/31/2016
Description: contains top-level instructions for solving TSP
Command line: python main.py [inputfile.txt]
Output to file: inputfile.txt.tour
"""
#############################################################
# Imports
#############################################################

import sys
import re
import math
import timeit

#############################################################
# DEBUG
# 1 = ON
# 0 = OFF
#############################################################

DEBUG = 0

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


def getfilepath():
    """
    parses command line to return input file
    :return filepath:
    """
    for arg in sys.argv:
        if arg.find(".txt") > -1:
            filepath = arg
            return filepath
    while True:
        print("[main.py] please enter an input file in format: inputfile.txt")
        filepath = raw_input("Your input file: ")
        if filepath.find(".txt") > -1:
            break
    return filepath


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
    for i in range(0, len(list)):
        list[i] = list[i].strip()
        list[i] = re.split("[ ]", list[i])
        list[i] = filter(None, list[i])
        for j in range(0, len(list[i])):
            list[i][j] = list[i][j].strip()
        if DEBUG:
            print("%s %s %s" % (list[i][0], list[i][1], list[i][2]))
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


def greedyhamiltoniancycle(connections, map):
    """
    creates greedy hamiltonian circuit connecting all nodes to each other
    each node is visited once except the origin node
    :param connections, map:
    :return circuit:
    """
    hamcycle = []
    destinationused = []
    minconnection = [0, 0, 0, 0]
    for i in range(len(connections) - 1, -1, -1):
        if connections[i].distance == 0:
            if i < len(connections) - 1:
                hamcycle.append(minconnection)
                destinationused.append(minconnection[2])
            minconnection = [connections[i].matrixid, connections[i].originid,
                             connections[i].destinationid, connections[i].distance]
        else:
            if minconnection[3] == 0:
                if connections[i].destinationid not in destinationused:
                    minconnection = [connections[i].matrixid, connections[i].originid,
                                     connections[i].destinationid, connections[i].distance]
            else:
                if minconnection[3] > connections[i].distance:
                    if connections[i].destinationid not in destinationused:
                        minconnection = [connections[i].matrixid, connections[i].originid,
                                         connections[i].destinationid, connections[i].distance]
    # this one is reversed origin <~> destination
    minconnection = [connections[len(map) - 1].matrixid, connections[len(map) - 1].destinationid,
                     connections[len(map) - 1].originid, connections[len(map) - 1].distance]
    hamcycle.append(minconnection)
    return hamcycle

# need to optimize path generated by greedy hamiltonian cycle function (2-opt)

def generateoutput(hamcycle):
    """
    generates output in desired format (file.txt.tour)
    :param hamcycle:
    :return:
    """
    distance = 0
    nodesvisited = []
    for i in range(0,len(hamcycle)):
        distance += hamcycle[i][3]
        nodesvisited.append(hamcycle[i][1])
    return distance, nodesvisited


def printtofile(filepath, distance, nodesvisited):
    """
    prints TSP optimal distance and nodes visited
    :param filepath:
    :param distance:
    :param nodesvisited:
    :return:
    """
    filepath = filepath + ".tour"
    filehandler = open(filepath, "w")
    filehandler.write("%d\n" % distance)
    for node in nodesvisited:
        filehandler.write("%d\n" % node)
    return

#############################################################
# Main Function
#############################################################


def main(filepath):
    if DEBUG:
        filepath = getfilepath()
        filecontents = readfile(filepath)
        map = formatmap(filecontents)
        for i in range(0, len(map)):
            print("[map] id: %d\tx coord: %d\ty coord: %d" % (map[i].nodeid, map[i].x, map[i].y))
        connections = connectmap(map)
        for i in range(0, len(connections)):
            print("[connections] id: %d\torigin id: %d\tdestination id: %d\tdistance: %d"
                  % (connections[i].matrixid, connections[i].originid, connections[i].destinationid, connections[i].distance))
        hamcycle = greedyhamiltoniancycle(connections, map)
        for i in range(0, len(hamcycle)):
            print("[hamcycle] %d:\t%s" % (i, hamcycle[i]))
        distance, nodesvisited = generateoutput(hamcycle)
        print("[output] %d" % distance)
        for i in range(0, len(nodesvisited)):
            print("[output] %d" % nodesvisited[i])
        printtofile(filepath, distance, nodesvisited)
    filecontents = readfile(filepath)
    map = formatmap(filecontents)
    connections = connectmap(map)
    hamcycle = greedyhamiltoniancycle(connections, map)
    distance, nodesvisited = generateoutput(hamcycle)
    printtofile(filepath, distance, nodesvisited)
    return


filepath = getfilepath()
t = timeit.Timer(lambda: main(filepath))
print("%f seconds" % t.timeit(number=1))
