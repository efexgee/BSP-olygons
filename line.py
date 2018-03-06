#!/usr/bin/env python

#TODO rename methods to make sense in line context

from math import hypot, isclose, inf
from xy import *
from PIL import Image, ImageDraw

class Line():
    ''' A straight line between two points '''

    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_LINE_COLOR = "black"
    _DEFAULT_WIDTH = 2
    # Add additional space beyond the bounding box of the Line
    # when displaying Line alone in .show()
    _CANVAS_PADDING = 10

    # These assume to be vertical or horizontal lines
    def __init__(self, start, end):
        #TODO validate that these are XY objects
        #TODO validate length of > 1
        #TODO validate it is horizontal or vertical
        #TODO sort at init time
        #TODO should I be sorting the start and end?
        if start == end:
            raise ValueError("Won't create zero-length Line: {} {}".format(start, end))

        if isinstance(start, tuple):
            self.start = XY(start)
        elif isinstance(start, XY):
            self.start = start
        else:
            raise TypeError("What am I supposed to do with this? {} is type {}".format(start, type(start)))

        if isinstance(end, tuple):
            self.end = XY(end)
        elif isinstance(end, XY):
            self.end = end
        else:
            raise TypeError("What am I supposed to do with this? {} is type {}".format(start, type(start)))

    def __contains__(self, point):
        #TODO poor form to overload a dunder like this?
        #TODO maybe this should handle both XY and Lines?
        # would that be terrible? or Pythonic?
        ''' Check whether a point is on the line '''
        if not isinstance(point, XY):
            raise TypeError("Argument must be an XY object: {} is type {}".format(point, type(point)))

        # If point is one of the Line's vertices, we can't
        # calculate a slope
        if self.has_vertex(point):
            #TODO It is curious how I sometimes feel I need to have
            # the explicit else and sometimes not
            return True

        #TODO Oh good. Checking for equality on floats. This
        # can't possibly go wrong
        # Using default args to math.isclose()
        return isclose(self.slope(), Line(self.start, point).slope())

    def xy_len(self):
        ''' Return the length of the Line as an XY object representing
            rise over run '''
        offset = self.end - self.start

        # If the run is negative, convert the slope
        if offset.x < 0:
            offset *= -1

        return offset

    def float_len(self):
        ''' Return the length of the Line as a floating point number '''
        rise, run = self.xy_len().astuple()

        return hypot(rise, run)

    def __len__(self):
        ''' The length of the line in pixels, rounded to the nearest integer '''
        #TODO Are we OK with this staggered design?
        return round(self.float_len())

    def __eq__(self, line):
        ''' Check whether the line is the same as another line, regardless of direction '''
        return not {self.start, self.end}.symmetric_difference({line.start, line.end})

    def xy_slope(self):
        ''' Return the slope of the Line as an XY object represenating
            rise over run '''
        #TODO is this OK? essentially just aliasing
        return self.xy_len()

    def slope(self):
        ''' Return the slope of the Line (as a floating point number) '''
        rise, run = self.xy_slope().astuple()

        #TODO is this how this is done?
        try:
            return rise / run
        except ZeroDivisionError:
            # The slope of a vertical line is undefined but I think
            # using infinity makes compares tighter
            return inf

    def split(self, vertex):
        ''' Split Line on vertex XY, returning two new Lines '''
        if vertex not in self:
            #TODO KeyError real iffy here
            raise KeyError("{} is not on Line {}".format(vertex, self))

        if vertex == self.start or vertex == self.end:
            # Zero-length Lines are not allowed
            raise ValueError("Can't split a Line on one of its vertices: line={} vertex={}".format(self, vertex))

        return Line(self.start, vertex), Line(self.end, vertex)

    def has_vertex(self, vertex):
        ''' Check whether XY is one of Line's vertices '''
        return vertex == self.start or vertex == self.end

    def shares_vertex(self, line):
        ''' Check whether the lines share an end point '''
        #TODO probably won't be used
        # this does not check for "touching" because that would include
        # adjacent vertices
        return bool({self.start, self.end}.intersection({line.start, line.end}))

    def astuples(self):
        ''' Return end points as a tuple of tuples (to use with PIL) '''
        #TODO doesn't feel good.
        return (self.start.astuple(), self.end.astuple())

    def add_to_draw(self, draw, color=_DEFAULT_LINE_COLOR, width=_DEFAULT_WIDTH):
        ''' Draw the line on a provided PIL draw object '''
        draw.line(self.astuples(), fill=color, width=width)

    def get_canvas_size(self):
        ''' Provide dimensions required to display Line '''
        # This is broken out from .show() to allow Edge.show()
        return XY(max(self.start.x, self.end.x), max(self.start.y, self.end.y)) + Line._CANVAS_PADDING

    def show(self):
        ''' Show the line '''
        img_size = self.get_canvas_size()

        img = Image.new("RGBA", img_size.astuple(), Line._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        #return str((self.start, self.end))
        #DEBUG for readability
        return "{}-{}".format(self.start, self.end)

    def __hash__(self):
        #TODO I don't see how hashing an equivalent data structure is any
        # safer than hashing the __repr__
        return hash(str(self))
