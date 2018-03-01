#!/usr/bin/env python

#TODO rename methods to make sense in line context

from math import sqrt
from xy import *

class Line():
    # These assume to be vertical or horizontal lines
    def __init__(self, start, end):
        #TODO validate that these are XY objects
        #TODO validate length of > 1
        #TODO validate it is horizontal or vertical
        #TODO sort at init time
        #TODO should I be sorting the start and end?
        if isinstance(start, tuple):
            self.start = XY(start)
        elif isinstance(start, XY):
            self.start = start
        else:
            print("What am I supposed to do with this? {} is type {}".format(start, type(start)))

        if isinstance(end, tuple):
            self.end = XY(end)
        elif isinstance(end, XY):
            self.end = end
        else:
            print("What am I supposed to do with this? {} is type {}".format(start, type(start)))

    def __contains__(self, point):
        ''' Check whether a point is on the line '''
        assert isinstance(point, XY), "Argument must be an XY object: {} is type {}".format(point, type(point))

        if self.orientation() == "vertical" and self.start.x == point.x:
            #print("vertical")
            if min(self.start.y, self.end.y) <= point.y <= max(self.start.y, self.end.y):
                return True
        elif self.orientation() == "horizontal" and self.start.y == point.y:
            ##print("horizontal")
            if min(self.start.x, self.end.x) <= point.x <= max(self.start.x, self.end.x):
                return True
        else:
            return False

    def __len__(self):
        ''' The length of the line in pixel, rounded to the nearest integer '''
        run, rise = (self.end - self.start).astuple()

        return round(sqrt(run**2 + rise**2))

    def orientation(self):
        ''' Return whether the line is vertical or horizontal '''
        if self.start.x == self.end.x:
            return "vertical"
        elif self.start.y == self.end.y:
            return "horizontal"
        else:
            print("This line is diagonal: {}".format(self))

    def __eq__(self, line):
        ''' Check whether the line is the same as another line, regardless of direction '''
        return not {self.start, self.end}.symmetric_difference({line.start, line.end})

    def difference(self, line):
        ''' in this, but not other (NOT IMPLEMENTED) '''
        pass

    def intersection(self, line):
        ''' in both (NOT IMPLEMENTED) '''
        pass

    def isdisjoint(self, line):
        ''' null intersection (NOT IMPLEMENTED) '''
        pass

    def issubset(self, line):
        ''' Check whether the line is a sub-segment of a line '''
        #TODO check if they are even on the same line first
        return min(line.start, line.end) <= min(self.start, self.end) and max(self.start, self.end) <= max(line.start, line.end)

    def symmetric_difference(self, line):
        ''' in this XOR other (NOT IMPLEMENTED) '''
        pass

    def union(self, line):
        ''' Return a new line formed of the two lines '''
        if not self.iscontiguous(line):
            #TODO maybe this would be a good place to catch exceptions
            print("Can't union non-contiguous lines: {} and {}".format(self, line))

        return Line(min(self.start, self.end, line.start, line.end), max(self.start, self.end, line.start, line.end))

    def overlaps(self, line):
        if not self.iscontiguous(line):
            #print("{} and {} are not contiguous".format(self, line))
            return False

        min_vertex = min(self.start, self.end, line.start, line.end)
        max_vertex = max(self.start, self.end, line.start, line.end)

        # If the distance between the outer two vertices is less than
        # the sum distance of the two lines, they must overlap
        if len(Line(min_vertex, max_vertex)) < len(self) + len(line):
            return True

    def iscontiguous(self, line):
        ''' Check whether the lines form a contiguous line '''

        if not self.orientation() == line.orientation():
            #print("diff orientations")
            return False

        #TODO This could be slicker
        if line.start in self or line.end in self:
            #print("part of {} falls on {}".format(line, self))
            return True
        if self.start in line or self.end in line: 
            #print("part of {} falls on {}".format(self, line))
            return True

        return False

    def shares_vertex(self, line):
        ''' Check whether the lines share an end point '''
        #TODO probably won't be used
        # this does not check for "touching" because that would include
        # adjacent vertices
        return bool({self.start, self.end}.intersection({line.start, line.end}))

    def astuples(self):
        ''' Return end points as a tuple of tuples (to use with PIL) '''
        return (self.start.astuple(), self.end.astuple())

    def __hash__(self):
        #TODO I don't see how hashing an equivalent data structure is any
        # safer than hashing the __repr__
        return hash(str(self))

    def __repr__(self):
        #return str((self.start, self.end))
        #DEBUG for readability
        return "{}-{}".format(self.start, self.end)
