#!/usr/bin/env python

from math import hypot
#from PIL import Image, ImageDraw

class XY():
    ''' a pair of x and y values which represent either a
        coordinate or a lengths in the x and y axes '''

    # Add additional space beyond the location of the coordinates
    # when displaying XY on its own
    _CANVAS_PADDING = 10
    _DEFAULT_COLOR = "black"
    _DEFAULT_BACKGROUND_COLOR = "white"

    # Maximum number of digits in x or y (for printing)
    _COORD_PADDING = 4

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

            if y is None:
                self.y = x
            else:
                self.y = y
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

    def magnitude(self):
        return hypot(self._x, self._y)

    def dot_product(self, vector):
        return (self._x * vector._x) + (self._y * vector._y)

    def as_tuple(self):
        return (self.x, self.y)

    def add_to_draw(self, draw, color=_DEFAULT_COLOR):
        ''' Add a point at XY to a PIL draw object '''
        draw.point(self.as_tuple(), fill=color)

    def show(self, color=_DEFAULT_COLOR):
        ''' Show a point at XY '''
        img_size = self + XY._CANVAS_PADDING

        img = Image.new("RGBA", img_size.as_tuple(), XY._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        return f"({self.x: {XY._COORD_PADDING}},{self.y: {XY._COORD_PADDING}})"

#TODO both diffs and coords are subs of XY
# coord init setters enforce positive values
# neg will throw exception
# return on math methods depends on types:
# coord + diff = coord, coord - coord = diff

class XYCoord(XY):
    def __sub__(self, coord):
        ''' Subtract a XYCoord with a lower limit of 0 in the result ''' 
        result = super().__sub__(coord)

        x = max(0, result._x)
        y = max(0, result._y)

        return XY(x, y)
