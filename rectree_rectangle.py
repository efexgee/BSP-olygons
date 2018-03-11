#!/usr/bin/env python

from xy import *
from line import *

class Rectangle():
    _DEFAULT_COLOR = "white"
    _DEFAULT_BORDER = "magenta"
    _DEFAULT_TEXT = "black"

    def __init__(self, origin, dimensions, label=None, color=None, border=True):
        ''' origin: coodinates of upper left pixel (XY object or tuple)
            dimensions: width and height (XY object or tuple) '''

        #TODO check for blank args
        if isinstance(origin, tuple):
            self.orig = XY(origin[0], origin[1])
        else:
            self.orig = origin

        if isinstance(dimensions, tuple):
            self.dims = XY(dimensions[0], dimensions[1])
        else:
            self.dims = dimensions

        self.label = label

        if color:
            self.color = color
        else:
            self.color = Rectangle._DEFAULT_COLOR

        #TODO Why is this private? just because setter?
        self._border = border
        if border:
            self._border_color = Rectangle._DEFAULT_BORDER
        else:
            self._border_color = self.color

    def v_split(self):
        half_size = self.dims // XY(2,1)

        left = Rectangle(self.orig, half_size, color=self.color, border=self._border)
        right = Rectangle(self.orig + XY(half_size.x, 0), half_size, color=self.color, border=self._border)

        return left, right

    def h_split(self):
        half_size = self.dims // XY(1,2)

        top = Rectangle(self.orig, half_size, color=self.color, border=self._border)
        bottom = Rectangle(self.orig + XY(0, half_size.y), half_size, color=self.color, border=self._border)

        return top, bottom

    def set_border(self, setting):
        self._border = setting

    def get_edges(self):
        #TODO make part of structure and update on the fly?
        upper_right = self.orig + XY(self.dims.x, 0)
        lower_right = self.orig + self.dims
        #TODO making a new XY much better than (0,1) mult shenanigans, right?
        lower_left = self.orig + XY(0, self.dims.y)
        #lower_left = self.orig + self.dims * XY(0,1)

        north = Line(self.orig, upper_right)
        east = Line(upper_right, lower_right)
        south = Line(lower_left, lower_right)
        west = Line(self.orig, lower_left)

        return north, east, south, west

    def show(self):
        #TODO Does having to add 1 indicate a problem? are borders frames?

        img_size = self.orig + self.dims + 1

        img = Image.new("RGBA", img_size.as_tuple(), "black")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def add_to_draw(self, draw):
        top_left = self.orig.as_tuple()
        bottom_right = (self.orig + self.dims).as_tuple()

        if self._border:
            border = self._border_color
        else:
            border = self.color

        draw.rectangle([top_left, bottom_right], self.color, border)

        if not self.label is None:
            #ImageDraw needs text to be a string
            label = str(self.label)

            label_size = XY(draw.textsize(label))

            #Only print a label if it fits inside the rectangle
            if label_size.fitsin(self.dims):
                label_origin = self.orig + self.dims // 2 - label_size // 2

                draw.text(label_origin.as_tuple(), label, fill=Rectangle._DEFAULT_TEXT)

    def __repr__(self):
        return f"Rectangle({self.orig}, {self.dims}, {self.label}, {self.color}, {self._border})"
