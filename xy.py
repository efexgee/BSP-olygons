#!/usr/bin/env python

class XY():
    ''' a pair of x and y values which represent either a
        coordinate or a lengths in the x and y axes, which
        supports addition and subtraction '''

    #TODO try to implement iterator so XY can be used as a tuple

    def __init__(self, x, y=None):
        #TODO Can I check for "isindexable"?
        # is container? from abstract classes (wwad)
        # hasattr getitem - would allow dicts
        # or catch exception on index
        # *var on call unpacks the doodad (WWAD)
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        elif isinstance(x, int):
            self.x = x

            if y is None:
                self.y = x
            else:
                self.y = y
        else:
            raise TypeError("Arguments aren't int or tuple: x={} y={}".format(x, y))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, int):
            raise TypeError("value is not an integer: {}".format(value))
        #TODO I can't ensure positive values if I'm going to use
        # XY to represent offsets / slopes
        #if not value >= 0:
            #TODO is there a check for positive I should be using?
            #raise ValueError("value is not positive: {}".format(value))
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, int):
            raise TypeError("value is not an integer: {}".format(value))
        #if not value >= 0:
            #raise ValueError("value is not positive: {}".format(value))
        self._y = value

    def __add__(self, value):
        if isinstance(value, XY):
            return XY(self.x + value.x, self.y + value.y)
        elif isinstance(value, int):
            return XY(self.x + value, self.y + value)

    def __sub__(self, value):
        if isinstance(value, XY):
            return XY(self.x - value.x, self.y - value.y)
        elif isinstance(value, int):
            return XY(self.x - value, self.y - value)

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

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        else:
            return False

    def fitsin(self, value):
        #TODO rename 'value' on all these
        #TODO should this be cancontain instead?
        # Both x and y are greater than value's x and y
        # i.e. a rectangle with dimensions 'value' could
        # fit inside a rectangle with our dimensions
        if self.x < value.x and self.y < value.y:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.astuple())

    def __gt__(self, value):
        # compare the non-shares dimension
        # A > B if A and B are on the same vertical or horizontal
        # line and A is further from the origin than B
        if self.x == value.x:
            return self.y > value.y
        elif self.y == value.y:
            return self.x > value.x
        else:
            #TODO what should be raised here?
            raise UserWarning("Shared axis required to order XY objects: {} and {}".format(self, value))

    def __ge__(self, value):
        return self > value or self == value

    def astuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)
