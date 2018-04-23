#!/usr/bin/env python

from polytree.xy import Coord
from polytree.ext_label import label_loc_xy
from math import acos, degrees
from polytree.globals import *

class Line():
    ''' A pair of Coords representing a line '''

    def __init__(self, tail, head):
        self._tail = Coord(tail)
        self._head = Coord(head)

    def find_point(self, percentage):
        ''' Returns a Coord near the location that is
        'percentage' between the Line's tail and head '''
        #TODO this needs some refinement to make sure the
        # point is actually on the line, not right next to it
        #TODO should this support relative to caller?

        # Just to shorten the lines below
        start = self._tail
        end = self._head

        multiplier = (100 - percentage) / 100

        if start.x == end.x:
            # This edge is vertical and must be handled differently
            #print(f"{self} is vertical")
            new_y = start.y + (round((end.y - start.y) * multiplier))
            new_point = Coord(start.x, new_y)
        else:
            rise_run = end - start
            new_point = start + (rise_run * multiplier)
            #print(f"{start} + ({rise_run} * {multiplier}) = {new_vertex}")

        return new_point

    def label_coords(self, side):
        ''' Returns a Coord offset from the center of the
        Line, suitable for printing a label '''
        if side == "right":
            offset = 10
        elif side == "left":
            offset = -10

        return label_loc_xy(self._tail, self._head, offset)

    def end_points(self):
        ''' Returns the Line's two Coords as a tuple '''
        #FEATURE use property if I want to fake an attribute ("descriptor")
        return self._tail, self._head

    def angle_between(self, line):
        ''' Returns the angle between two Lines in degrees '''
        vector_a = self._head - self._tail
        vector_b = line._head - line._tail

        dot_product = vector_a.dot_product(vector_b)
        magnitudes = vector_a.magnitude() * vector_b.magnitude()

        try:
            rads = acos(dot_product / magnitudes)
        except ZeroDivisionError:
            angle = 90
        else:
            angle = degrees(rads)

        return angle

    def add_to_draw(self, draw, color=None, width=None):

        color = DEFAULT_LINE_COLOR if color is None else color
        width = DEFAULT_LINE_WIDTH if width is None else width

        #print(f"Drawing Line: color={color} width={width}")
        draw.line((self._tail.as_tuple(), self._head.as_tuple()), fill=color, width=width)

    def __repr__(self):
        ''' Lines are represented as 'XY-XY' '''
        return f"{self._tail}-{self._head}"
