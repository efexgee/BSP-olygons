#!/usr/bin/env python

from math import hypot, isclose, inf
from xy import *
from PIL import Image, ImageDraw

class LineSegment():
    ''' A straight line segment between two points '''

    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_LINE_COLOR = "black"
    _DEFAULT_WIDTH = 2
    # Add additional space beyond the bounding box of the LineSegment
    # when displaying LineSegment alone in .show()
    _CANVAS_PADDING = 10

    _ISCLOSE_REL_TOLERANCE = 0.1  # 10% relative tolerance

    def __init__(self, _tail, _head):
        if isinstance(_tail, tuple):
            self._tail = XY(_tail)
        elif isinstance(_tail, XY):
            self._tail = _tail
        else:
            raise TypeError(f"Start must be an XY object or a tuple. {_tail} is type {type(_tail)}")

        if isinstance(_head, tuple):
            self._head = XY(_head)
        elif isinstance(_head, XY):
            self._head = _head
        else:
            raise TypeError(f"End must be an XY object or a tuple. {_head} is type {type(_head)}")

        # Check after handling types to support mixed types for _tail
        # and _head
        if self._tail == self._head:
            raise ValueError(f"Won't create zero-length LineSegment: {_tail} {_head}")

    def __contains__(self, point):
        #TODO maybe this should handle both XY and LineSegments?
        ''' Check whether a point is on the LineSegment
            THIS IS VERY IMPRECISE '''
        if not isinstance(point, XY):
            #TODO distinguish between programming error and runtime errors
            # don't raise exceptions on typos / bad code
            raise TypeError("Point must be an XY object: {point} is type {type(point)}")

        # If point is one of the LineSegment's vertices, we can't
        # calculate a slope
        if self.has_vertex(point):
            return True

        # Make sure the point is inside the bounding box of the LineSegment
        box = self.bounding_box()
        if not box._tail <= point <= box._head:
            return False

        print("Warning: the __contains__ is very imprecise beyond this point")

        self_slope = self.slope()
        point_slope = LineSegment(self._tail, point).slope()

        return isclose(self.slope(), LineSegment(self._tail, point).slope(), rel_tol=LineSegment._ISCLOSE_REL_TOLERANCE)

    def xy_len(self):
        ''' Return the length of the LineSegment as an XY object representing
            rise over run '''
        offset = self._head - self._tail

        # If the run is negative, convert the slope
        if offset.x < 0:
            offset *= -1

        return offset

    def float_len(self):
        ''' Return the length of the LineSegment as a floating point number '''
        rise, run = self.xy_len().as_tuple()

        return hypot(rise, run)

    def bounding_box(self):
        ''' Return the bounding box of the LineSegment as a LineSegment representing
            the upper left and lower right points of the box '''
        upper_left = XY(min(self._tail.x, self._head.x), min(self._tail.y, self._head.y))
        lower_right = XY(max(self._tail.x, self._head.x), max(self._tail.y, self._head.y))
        return LineSegment(upper_left, lower_right)

    def length(self):
        ''' The length of the LineSegment in pixels, rounded to the nearest integer '''
        return round(self.float_len())

    def __eq__(self, line):
        ''' Check whether the LineSegment is the same as another LineSegment, regardless of direction '''
        return {self._tail, self._head} == {line._tail, line._head}

    def xy_slope(self):
        ''' Return the slope of the LineSegment as an XY object represenating
            rise over run '''
        return self.xy_len()

    def slope(self):
        ''' Return the slope of the LineSegment (as a floating point number) '''
        rise, run = self.xy_slope().as_tuple()

        try:
            return rise / run
        except ZeroDivisionError:
            # Using infinity as the slope of the LineSegment instead of
            # the correct undefined so I can compare the slopes of
            # two LineSegments
            return inf

    def split(self, point):
        ''' Split LineSegment on point XY, returning two new LineSegments '''
        if point not in self:
            #TODO not a KeyError, but leave to troll pedants
            raise KeyError("{point} is not on LineSegment {self}")

        if point == self._tail or point == self._head:
            # Zero-length LineSegments are not allowed
            raise ValueError("Can't split a LineSegment on one of its vertices: LineSegment={self} point={point}")

        return LineSegment(self._tail, point), LineSegment(self._head, point)

    def has_vertex(self, vertex):
        ''' Check whether XY is one of LineSegment's vertices '''
        return vertex in (self._tail, self._head)

    def shares_vertex(self, line):
        ''' Check whether the LineSegments share an _head point '''
        #TODO probably won't be used
        # this does not check for "touching" because that would include
        # adjacent vertices (LineSegments of length 1)
        return bool({self._tail, self._head}.intersection({line._tail, line._head}))

    def as_tuples(self):
        ''' Return _head points as a tuple of tuples (to use with PIL) '''
        return (self._tail.as_tuple(), self._head.as_tuple())

    def add_to_draw(self, draw, color=_DEFAULT_LINE_COLOR, width=_DEFAULT_WIDTH):
        ''' Draw the LineSegment on a provided PIL draw object '''
        draw.line(self.as_tuples(), fill=color, width=width)

    def get_canvas_size(self):
        ''' Provide dimensions required to display LineSegment '''
        #TODO use bounding_box?
        #TODO don't support edge.show this way
        # This is broken out from .show() to allow Edge.show()
        return XY(max(self._tail.x, self._head.x), max(self._tail.y, self._head.y)) + LineSegment._CANVAS_PADDING

    def show(self):
        ''' Display the LineSegment '''
        img_size = self.get_canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), LineSegment._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        return f"{self._tail}-{self._head}"

    def __hash__(self):
        # Hash based on a tuple of the two values
        return hash((self._tail, self._head))
