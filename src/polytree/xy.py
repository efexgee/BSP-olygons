#!/usr/bin/env python

from math import hypot
from polytree.globals import *

class XY():
    ''' a pair of x and y values which represent either a
        coordinate or a lengths in the x and y axes '''

    #MAYBE try to implement iterator so XY can be used as a tuple

    #TODO rename x and y
    def __init__(self, x, y=None):
        #MAYBE Can I check for "isindexable"?
        # is container? from abstract classes (wwad)
        # hasattr getitem - would allow dicts
        # or catch exception on index
        # *var on call unpacks the doodad (WWAD)
        if isinstance(x, tuple):
            self.x, self.y = x
        elif isinstance(x, int):
            self.x = x

            self.y = x if y is None else y

        elif isinstance(x, XY):
            self.x = x.x
            self.y = x.y
        else:
            raise TypeError(f"Can't interpret argument types: x={type(x)} y={(y)}")

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Value is not an integer: {value}")
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Value is not an integer: {value}")
        self._y = value

    def __add__(self, value):
        if isinstance(value, XY):
            return XY(self.x + value.x, self.y + value.y)
        elif isinstance(value, int):
            return XY(self.x + value, self.y + value)

    def __mul__(self, value):
        if isinstance(value, XY):
            return XY(self.x * value.x, self.y * value.y)
        #TODO don't treat int and float separately
        elif isinstance(value, int):
            return XY(self.x * value, self.y * value)
        elif isinstance(value, float):
            return XY(round(self.x * value), round(self.y * value))

    def __floordiv__(self, value):
        if isinstance(value, XY):
            return XY(self.x // value.x, self.y // value.y)
        elif isinstance(value, int):
            return XY(self.x // value, self.y // value)

    def __eq__(self, xy):
        if self.x == xy.x and self.y == xy.y:
            return True
        else:
            return False

    def fitsin(self, xy):
        #TODO shouldn't be a method at all, as this name/concept
        # Both x and y are greater than xy's x and y
        # i.e. a rectangle with dimensions 'xy' could
        # fit inside a rectangle with our dimensions
        if self.x < xy.x and self.y < xy.y:
            return True
        else:
            return False

    def __gt__(self, xy):
        return self.x > xy.x and self.y > xy.y

    def __ge__(self, xy):
        ''' Greater than or equal to ( >= ) '''
        return self.x >= xy.x and self.y >= xy.y

    def __sub__(self, value):
        if isinstance(value, XY):
            x = self.x - value.x
            y = self.y - value.y
        elif isinstance(value, int):
            x = self.x - value
            y = self.y - value

        return XY(x, y)

    #ASK for some reason I think @property is no good here
    def magnitude(self):
        return hypot(self.x, self.y)

    def dot_product(self, vector):
        return (self.x * vector.x) + (self.y * vector.y)

    def is_in_box(self, a, b):
        return min(a.x, b.x) <= self.x <= max(a.x, b.x) \
           and min(a.y, b.y) <= self.y <= max(a.y, b.y)

    def as_tuple(self):
        return (self.x, self.y)

    #HELP should this only exist on Coord?
    def add_to_draw(self, draw, color=None, size=None):
        ''' Add a point at XY to a PIL draw object '''

        color = DEFAULT_POINT_COLOR if color is None else color
        size = DEFAULT_POINT_SIZE if size is None else size

        if size == 1:
            draw.point(self.as_tuple(), fill=color)
        else:
            radius = size // 2
            draw.ellipse((self - Offset(radius).as_tuple(), self + Offset(radius).as_tuple()), fill=color)

    def __repr__(self):
        return f"({self.x: {COORD_PADDING}},{self.y: {COORD_PADDING}})"

class Coord(XY):
    ''' An XY coordinate (must be positive) '''
    def __init__(self, x, y=None):
        super().__init__(x, y)

        #HELP hacky? I like it
        if self.x < 0 or self.y < 0:
            raise ValueError(f"Coords must be non-negative: x={x} y={y}")

    #HELP wrap here, don't squeeze logic into XY, right?
    def __sub__(self, value):
        #HELP math once, coerce many, right? less noisy
        result = super().__sub__(value)

        if isinstance(value, Coord):
            # Coord - Coord = Offset
            return Offset(result)
        elif isinstance(value, Offset):
            # Coord - Offset = Coord
            return Coord(result)
        else:
            # Type is undefined for other combinations
            return result

    def __add__(self, value):
        result = super().__add__(value)

        if isinstance(value, Offset):
            # Coord + Offset = Coord
            return Coord(result)
        else:
            # Type is undefined for other combinations
            return result

class Offset(XY):
    ''' The offset between two XY coordinates '''

    def __sub__(self, value):
       #HELP math once, coerce many, right? less noisy
       result = super().__sub__(value)

       if isinstance(value, Offset):
           # Offset - Offset = Offset
           return Coord(result)
       else:
           # Type is undefined for other combinations
           return result

    def __add__(self, value):
       result = super().__add__(value)

       if isinstance(value, Offset):
           # Offset + Offset = Offset
           return Offset(result)
       elif isinstance(value, Coord):
           # Offset + Coord = Coord
           return Coord(result)
       else:
           # Type is undefined for other combinations
            return result
