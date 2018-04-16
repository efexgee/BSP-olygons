#!/usr/bin/env python

from PIL import Image, ImageDraw
from polytree.xy import XY
from polytree.ext_label import label_loc_xy
from math import acos, degrees

class Line():

    # Padding when displaying Lines on their own
    _CANVAS_PADDING = 10
    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_LINE_COLOR = "black"
    _DEFAULT_LINE_WIDTH = 2

    def __init__(self, tail, head):
        self._tail = XY(tail)
        self._head = XY(head)

    def find_point(self, percentage):
        #TODO this needs some refinement to make sure the
        # point is actually on the line, not right next to it
        #TODO should this support relative to caller?

        start = self._tail
        end = self._head

        multiplier = (100 - percentage) / 100

        if start._x == end._x:
            # This edge is vertical and must be handled differently
            #print(f"{self} is vertical")
            new_y = start._y + (round((end._y - start._y) * multiplier))
            new_point = XY(start._x, new_y)
        else:
            # Cast to XY so we can get negative values
            #HELP this is very awkward casting
            rise_run = XY(end.as_tuple()) - XY(start.as_tuple())
            new_point = XY(start + (rise_run * multiplier))
            #print(f"{start} + ({rise_run} * {multiplier}) = {new_vertex}")

        return new_point

    def label_coords(self, side):
        if side == "right":
            offset = 10
        elif side == "left":
            offset = -10

        return label_loc_xy(self._tail, self._head, offset)

    def end_points(self):
        #FEATURE use property if I want to fake an attribute ("descriptor")
        return self._tail, self._head

    def angle_between(self, line):
        vector_a = self._head - self._tail
        vector_b = line._head - line._tail

        dot_product = vector_a.dot_product(vector_b)
        magnitudes = vector_a.magnitude() * vector_b.magnitude()

        #HELP or via exception?
        if magnitudes == 0:
            #TODO I think this is right
            return 90

        rads = acos(dot_product / magnitudes)
        angle = degrees(rads)

        return angle

    def add_to_draw(self, draw, color=None, width=None):

        color = Line._DEFAULT_LINE_COLOR if color is None else color
        width = Line._DEFAULT_LINE_WIDTH if width is None else width

        draw.line((self._tail.as_tuple(), self._head.as_tuple()), fill=color, width=width)

    def show(self, color=None, width=None):
        ''' Display the Line '''

        img_size = XY(max(self._tail.x, self._head.x), max(self._tail.y, self._head.y)) + Line._CANVAS_PADDING
        img = Image.new("RGBA", img_size.as_tuple(), Line._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw, color, width)

        img.show()

    def __repr__(self):
        return f"{self._tail}-{self._head}"
