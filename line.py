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

    def __init__(self, start, end):
        if start == end:
            raise ValueError(f"Won't create zero-length LineSegment: {start} {end}")

        if isinstance(start, tuple):
            self.start = XY(start)
        elif isinstance(start, XY):
            self.start = start
        else:
            raise TypeError(f"What am I supposed to do with this? {start} is type {type(start)}")

        if isinstance(end, tuple):
            self.end = XY(end)
        elif isinstance(end, XY):
            self.end = end
        else:
            raise TypeError("What am I supposed to do with this? {} is type {}".format(start, type(start)))

    def __contains__(self, point):
        #TODO maybe this should handle both XY and LineSegments?
        ''' Check whether a point is on the LineSegment
            THIS IS VERY IMPRECISE '''
        if not isinstance(point, XY):
            #TODO distinguish between programming error and runtime errors
            # don't raise exceptions on typos / bad code
            raise TypeError("Argument must be an XY object: {} is type {}".format(point, type(point)))

        # If point is one of the LineSegment's vertices, we can't
        # calculate a slope
        if self.has_vertex(point):
            return True

        # Make sure the point is inside the bounding box of the LineSegment
        box = self.bounding_box()
        if not box.start <= point <= box.end:
            return False

        print("Warning: the __contains__ is very imprecise beyond this point")

        self_slope = self.slope()
        point_slope = LineSegment(self.start, point).slope()

        return isclose(self.slope(), LineSegment(self.start, point).slope(), rel_tol=LineSegment._ISCLOSE_REL_TOLERANCE)

    def xy_len(self):
        ''' Return the length of the LineSegment as an XY object representing
            rise over run '''
        offset = self.end - self.start

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
        upper_left = XY(min(self.start.x, self.end.x), min(self.start.y, self.end.y))
        lower_right = XY(max(self.start.x, self.end.x), max(self.start.y, self.end.y))
        return LineSegment(upper_left, lower_right)

    def length(self):
        ''' The length of the LineSegment in pixels, rounded to the nearest integer '''
        return round(self.float_len())

    def __eq__(self, line):
        ''' Check whether the LineSegment is the same as another LineSegment, regardless of direction '''
        return {self.start, self.end} == {line.start, line.end}

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

        if point == self.start or point == self.end:
            # Zero-length LineSegments are not allowed
            raise ValueError("Can't split a LineSegment on one of its vertices: LineSegment={self} point={point}".format(self, point))

        return LineSegment(self.start, point), LineSegment(self.end, point)

    def has_vertex(self, vertex):
        ''' Check whether XY is one of LineSegment's vertices '''
        return vertex in (self.start, self.end)

    def shares_vertex(self, line):
        ''' Check whether the LineSegments share an end point '''
        #TODO probably won't be used
        # this does not check for "touching" because that would include
        # adjacent vertices (LineSegments of length 1)
        #TODO what's a better way to write this?
        return bool({self.start, self.end}.intersection({line.start, line.end}))

    def as_tuples(self):
        ''' Return end points as a tuple of tuples (to use with PIL) '''
        return (self.start.as_tuple(), self.end.as_tuple())

    def add_to_draw(self, draw, color=_DEFAULT_LINE_COLOR, width=_DEFAULT_WIDTH):
        ''' Draw the LineSegment on a provided PIL draw object '''
        draw.line(self.as_tuples(), fill=color, width=width)

    def get_canvas_size(self):
        ''' Provide dimensions required to display LineSegment '''
        # This is broken out from .show() to allow Edge.show()
        return XY(max(self.start.x, self.end.x), max(self.start.y, self.end.y)) + LineSegment._CANVAS_PADDING

    def show(self):
        ''' Show the LineSegment '''
        img_size = self.get_canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), LineSegment._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        return "{self.start}-{self.end}"

    def __hash__(self):
        # Hash based on a tuple of the two values
        return hash((self.start, self.end))
