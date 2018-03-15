#!/usr/bin/env python

from PIL import Image, ImageDraw

class XY():
    ''' a pair of x and y values which represent either a
        coordinate or a lengths in the x and y axes '''

    # Add additional space beyond the location of the coordinates
    # when displaying XY on its own
    _CANVAS_PADDING = 10
    _DEFAULT_COLOR = "black"
    _DEFAULT_BACKGROUND_COLOR = "white"

    #TODO try to implement iterator so XY can be used as a tuple

    def __init__(self, x, y=None):
        #TODO Can I check for "isindexable"?
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
        else:
            raise TypeError(f"Arguments aren't int or tuple: x={x} y={y}")

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Value is not an integer: {value}")
        #TODO I can't ensure positive values if I'm going to use
        # XY to represent offsets / slopes
        #if not value >= 0:
            #raise ValueError("value is not positive: {}".format(value))
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

    def __sub__(self, value):
        #TODO make diff classes for coords and things that can be negative
        if isinstance(value, XY):
            #TODO split into lines
            x, y = (self.x - value.x, self.y - value.y)
        elif isinstance(value, int):
            x, y = (self.x - value, self.y - value)

        #TODO max()
        #TODO Will this ever come up?
        if x < 0:
            print(f"Warning: subtraction result {x} was replaced with 0")
            x = 0
        if y < 0:
            print(f"Warning: subtraction result {y} was replaced with 0")
            y = 0

        #if x < 0 or y < 0:
            #TODO custom exception name so I can handle it outside?
            #raise ValueError(f"{self} minus {value} is out of bounds: XY(x, y)")
        #else:
            #return XY(x, y)

        return XY(x, y)

    def __mul__(self, value):
        if isinstance(value, XY):
            return XY(self.x * value.x, self.y * value.y)
        elif isinstance(value, int):
            return XY(self.x * value, self.y * value)

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

    def __hash__(self):
        #TODO probably no point to having a hash since I can't use
        # this as a key
        return hash(self.as_tuple())

    def __gt__(self, xy):
        return self.x > xy.x and self.y > xy.y

    '''
    def __gt__(self, xy):
        # compare the non-equal dimensions
        # A > B if A and B are on the same vertical or horizontal
        # line and A is further from the origin than B
        if self.x == xy.x:
            return self.y > xy.y
        elif self.y == xy.y:
            return self.x > xy.x
        else:
            #TODO this should not be a warning-exception
            raise UserWarning("Shared axis required to order XY objects: {} and {}".format(self, xy))
    '''

    def __ge__(self, xy):
        ''' Greater than or equal to ( >= ) '''
        return self.x >= xy.x and self.y >= xy.y

    def __abs__(self):
        ''' Return absolute value of XY '''
        #TODO Not used currently
        return XY(abs(self.x), abs(self.y))

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
        return f"({self.x},{self.y})"
