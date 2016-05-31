"""
File Name: main.py
Date Created: 05/31/2016
Description: contains top-level instructions for solving TSP
"""

#############################################################
# Classes
#############################################################


class Node(object):
    """
    Definition for 2-Dimensional Node object
    x = x coordinate
    y = y coordinate
    """
    id = 0
    x = 0
    y = 0

    def __init__(self, id, x, y):
        """
        Initialize instance of Node object
        :param x:
        :param y:
        """
        self.id = id
        self.x = x
        self.y = y

##############################################################
# Supplemetal Functions
##############################################################


def distance(node):
    """
    returns sum of x and y coordinates of node object
    uses absolute values
    :param node:
    :return node.x + node.y:
    """
    return abs(node.x) + abs(node.y)

#############################################################
# Main Function
#############################################################


def main():
    return

main()