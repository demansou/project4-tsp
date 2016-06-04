"""
File Name: new.py
Date Created: 05/31/2016
Description: contains top-level instructions for solving TSP
Command line: python new.py [inputfile.txt]
Output to file: inputfile.txt.tour
"""
#############################################################
# Imports
#############################################################

import sys
import re
import math
import timeit
import numpy

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


class MapConnection(object):
    """
    Definition for 2-Dimensional MapConnection object
    connectionid = connection id
    origin = origin node
    destination = destination node
    distance = distance from origin node to destination node in 2-D space
    """
    connectionid = 0
    origin = Node(0, 0, 0)
    destination = Node(0, 0, 0)
    distance = 0

    def __init__(self, connectionid, origin, destination, distance):
        """
        Initialize instance of MapConnection object
        :param connectionid:
        :param origin:
        :param destination:
        :param distance:
        """
        self.connectionid = connectionid
        self.origin = origin
        self.destination = destination
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
    list = re.split("[\n]", filecontents)
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
    :return distance):
    """
    distance = int(
        round(math.sqrt(math.pow((origin.x - destination.x), 2) + math.pow((origin.y - destination.y), 2))))
    return distance


def greedyhamiltoniancycle(map):
    """
    creates greedy hamiltonian circuit connecting all nodes to each other
    each node is visited once except the origin node
    :param map:
    :return hamcycle:
    """
    hamcycle = []
    for i in range(0, len(map) - 1):
        connection = MapConnection(i, map[i], map[i+1], nodedistance(map[i], map[i+1]))
        hamcycle.append(connection)
    connection = MapConnection(len(map), map[len(map) - 1], map[0], nodedistance(map[len(map) - 1], map[0]))
    hamcycle.append(connection)
    return hamcycle


def edge_swap(hamcycle, i, j):
    """
    edge_swap will take the current hamcycle and the index positions of two edges
    Only the destination nodes will be swapped
    :param hamcycle: list of edges [matrixid, destination node id, origin node id, distance]
    :param i: node 1 to swap
    :param j: node 2 to swap
    :return: updated hamcycle with two new edges and edge distance updates
    """
    # The next three lines use a temp node to swap the data
    hamcycle[i].destination = hamcycle[j].destination
    temp_node = hamcycle[i].destination
    hamcycle[j].destination = temp_node
    if DEBUG:
        print("[ANTE SWAP] - distance of ham i:%d\t\tdistance of ham j:%d" % (hamcycle[i].distance, hamcycle[j].distance))

    # Update the distances of the new paths
    hamcycle[i].distance = nodedistance(hamcycle[i].origin, hamcycle[i].destination)
    hamcycle[j].distance = nodedistance(hamcycle[j].origin, hamcycle[j].destination)
    if DEBUG:
        print("[POST SWAP] - distance of ham i:%d\t\tdistance of ham j:%d" % (hamcycle[i].distance, hamcycle[j].distance))
    return hamcycle


def routes_overlap(MapConnection1, MapConnection2):
    """
    function to decide if
    :param MapConnection1: (MapConnection object)
    :param MapConnection2: (MapConnection object)
    :return bool:
    """
    """
    origin1 = numpy.array([float(MapConnection1.origin.x), float(MapConnection1.origin.y)])
    destination1 = numpy.array([float(MapConnection1.destination.x), float(MapConnection1.destination.y)])
    origin2 = numpy.array([float(MapConnection2.origin.x), float(MapConnection2.origin.y)])
    destination2 = numpy.array([float(MapConnection2.destination.x), float(MapConnection2.destination.y)])
    route1 = destination1 - origin1
    route2 = destination2 - origin2
    distance1 = origin1 - origin2
    perpendicularslope = numpy.empty_like(route1)
    perpendicularslope[0] = -route1[1]
    perpendicularslope[1] = route1[0]
    denominator = numpy.dot(perpendicularslope, route2)
    numerator = numpy.dot(perpendicularslope, distance1)
    intersect = (numerator / denominator.astype(float)) * route2 + origin2
    if DEBUG:
        print("[hamcycle] %f %f" % (intersect[0], intersect[1]))
    if origin1[0] > destination1[0]:
        if not (origin1[0] >= intersect[0] >= destination1[0]):
            return False
    elif origin1[0] < destination1[0]:
        if not (origin1[0] <= intersect[0] <= destination1[0]):
            return False
    if origin1[1] > destination1[1]:
        if not (origin1[1] >= intersect[1] >= destination1[1]):
            return False
    elif origin1[1] < destination1[1]:
        if not (origin1[1] <= intersect[1] <= destination1[1]):
            return False
    if origin2[0] > destination2[0]:
        if not (origin2[0] >= intersect[0] >= destination2[0]):
            return False
    elif origin2[0] < destination2[0]:
        if not (origin2[0] <= intersect[0] <= destination2[0]):
            return False
    if origin2[1] > destination2[1]:
        if not (origin2[1] >= intersect[1] >= destination2[1]):
            return False
    elif origin2[1] < destination2[1]:
        if not (origin2[1] <= intersect[1] <= destination2[1]):
            return False
    return True
    """
    origin1 = numpy.array([MapConnection1.origin.x, MapConnection1.origin.y])
    destination1 = numpy.array([MapConnection1.destination.x, MapConnection1.destination.y])
    origin2 = numpy.array([MapConnection2.origin.x, MapConnection2.origin.y])
    destination2 = numpy.array([MapConnection2.destination.x, MapConnection2.destination.y])
    equation1 = numpy.cross((origin1 * destination1), (destination1 * origin2)) \
                * numpy.cross((origin1 * destination1), (destination1 * destination2))
    equation2 = numpy.cross((origin2 * destination2), (destination2 * origin1)) \
                * numpy.cross((origin2 * destination2), (destination2 * destination1))
    if equation1 < 0 and equation2 < 0:
        return True

    return
def optimizehamcycle(hamcycle, map):
    """

    :param hamcycle:
    :return:
    """
    return


def generateoutput(hamcycle):
    """
    generates output in desired format (file.txt.tour)
    :param hamcycle:
    :return distance, nodesvisited:
    """
    distance = 0
    nodesvisited = []
    for i in range(0, len(hamcycle)):
        distance += hamcycle[i].distance
        nodesvisited.append(hamcycle[i].origin)
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
        filehandler.write("%d\n" % node.nodeid)
    return

#############################################################
# Main Function
#############################################################


def main(filepath):
    if DEBUG:
        filecontents = readfile(filepath)
        map = formatmap(filecontents)
        for i in range(0, len(map)):
            print("[map] id: %d\tx coord: %d\ty coord: %d" % (map[i].nodeid, map[i].x, map[i].y))
        hamcycle = greedyhamiltoniancycle(map)
        for i in range(0, len(hamcycle)):
            print("[hamcycle] i: %d\t\torigin.nodeid: %d\tdestination.nodeid: %d\tdistance: %d" % (i, hamcycle[i].origin.nodeid, hamcycle[i].destination.nodeid, hamcycle[i].distance))
        distance, nodesvisited = generateoutput(hamcycle)
        print("distance traveled: %d" % distance)
        for node in nodesvisited:
            print("node visited: %d" % node.nodeid)
        printtofile(filepath, distance, nodesvisited)
        result = routes_overlap(hamcycle[0], hamcycle[1])
        if result == True:
            print("intersects")
        else:
            print("no intersects")
    filecontents = readfile(filepath)
    map = formatmap(filecontents)
    hamcycle = greedyhamiltoniancycle(map)
    distance, nodesvisited = generateoutput(hamcycle)
    printtofile(filepath, distance, nodesvisited)
    return


filepath = getfilepath()
t = timeit.Timer(lambda: main(filepath))
print("%f seconds" % t.timeit(number=1))