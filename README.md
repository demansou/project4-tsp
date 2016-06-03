# project4-tsp

## Goals
To take a two dimensional map with various cities represented by
x and y coordinates. We will compute the shortest tour to visit all
cities and to return to the starting city. This assumes that each city
has a connection to all other cities. The distance from one city to
another is sqrt[(x1 - x2)^2 + (y1 - y2)^2]
* Ratio of this solution compared to optimal is 1.25 (this/optimal)

## How to Run
Launch the program by using the following command:
``` python2.7 main.py [input_file_name]```

## Input Files
This program is designed to read text input files. Each line will define
a city and its location in the following format:
* The first number is the city identifier
* The second number is the city's x coordinate
* The third number is the city's y coordinate.
If debug mode is enabled (1), the default file name is 'tsp_example_1.txt'

## Output Files
Output will be saved as [filename.txt].tour. the output fille will have
a line count of [number of cities] + 1. the first line will hold an
integer representing the length of the tour. Each line following will
hold the city identifiers in the order they are visited.

## Example
```python2.7 main.py tsp_example_1.txt```

Input: tsp_test.txt
Output tsp_test.txt.tour

tsp_example_1.txt contents:
```
1 0 0
2 1 3
3 6 0
```

tsp_example_1.txt.tour contents:
```
15
2
1
3
```

