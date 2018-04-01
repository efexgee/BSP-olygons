#!/usr/bin/env python

#:TIDY check private attributes and methods in all modules

from PIL import Image, ImageDraw
from polytree.vertex import *
from polytree.ext_label import *

class Edge():
    ''' Connects two Vertices and the Nodes shared by the Edge '''

    # Padding when displaying Edges on their own
    _CANVAS_PADDING = 10
    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_LINE_COLOR = "black"
    _DEFAULT_LINE_WIDTH = 2
    _DEFAULT_SHOW_LABELS = True

    def __init__(self, tail, head, left_node, right_node):
        self._tail = None
        self._head = None

        tail.connect_outbound(self)
        self.connect_into(head)
        # Forcing the user to explicitly specify None in the
        # case of an exterior edge by not providing defaults
        self._left_node = left_node      # should only be changed via replace()
        self._right_node = right_node    # should only be changed via replace()

    def borders_node(self, node):
        ''' Check whether Edge is part of a Node '''
        if node is self._left_node:
            return "left"
        elif node is self._right_node:
            return "right"
        else:
            return False

    def get_new_vertex(self, percentage):
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
            new_vertex = Vertex(start._x, new_y)
        else:
            # Cast to XY so we can get negative values
            rise_run = XY(end.as_tuple()) - XY(start.as_tuple())
            new_vertex = Vertex(start + (rise_run * multiplier))
            #print(f"{start} + ({rise_run} * {multiplier}) = {new_vertex}")

        return new_vertex

    def split(self, percentage):
        #TODO should this support relative to caller?
        ''' Insert a new vertex percentage of the way from tail
        to head and return two new edges '''

        new_vertex = self.get_new_vertex(percentage)

        tail_segment = Edge(self._tail, new_vertex, self._left_node, self._right_node)
        head_segment = Edge(new_vertex, self._head, self._left_node, self._right_node)

        return tail_segment, new_vertex, head_segment

    def disconnect(self):
        self._tail.disconnect(self)
        self._head.disconnect(self)

    def replace(self, old_node, new_node):
        ''' Replace a Node associated with an Edge
            This the only way Edges' Nodes should be
            changed '''
        if self._left_node == old_node:
            self._left_node = new_node
        elif self._right_node == old_node:
            self._right_node = new_node
        else:
            #TIDY custom exception or ValueError as last resort
            raise KeyError(f"{old_node} not attached to {self}")

    def other_vertex(self, caller):
        if caller is self._tail:
            return self._head
        elif caller is self._head:
            return self._tail
        else:
            #TIDY wrong exception type; see above
            raise KeyError(f"{caller} is not part of {self}")

    def rel_side(self, side, caller):
        ''' Return a node as seen from the referrer POV '''
        if side == "right":
            if caller is self._tail:
                return self._right_node
            else:
                return self._left_node
        elif side == "left":
            if caller is self._tail:
                return self._left_node
            else:
                return self._right_node
        else:
            raise ValueError(f"{caller} is neither {self._tail} nor {self._head}")

    def vertices(self):
        #FEATURE use property if I want to fake an attribute ("descriptor")
        return self._tail, self._head

    def _connect_from(self, vertex):
        ''' Connect to a vertex '''
        assert not self._tail, f"_tail of {self} is already set: {self._tail}"
        self._tail = vertex

    def _connect_to(self, vertex):
        assert not self._head, f"_head of {self} is already set: {self._head}"
        self._head = vertex

    def connect_into(self, vertex):
        self._connect_to(vertex)
        vertex._connect(self)

    def add_to_draw(self, draw, labels=None, color=None, width=None):
        ''' Add Edge to the specified PIL draw object '''

        #HELP wait, is this how this goes? this is hideous
        labels = Edge._DEFAULT_SHOW_LABELS if labels is None else labels
        color = Edge._DEFAULT_LINE_COLOR if color is None else color
        width = Edge._DEFAULT_LINE_WIDTH if width is None else width

        #print(f"Edge: adding {self} in {color}")
        draw.line((self._tail.as_tuple(), self._head.as_tuple()), fill=color, width=width)

        if labels:
            #print(f"Labeling {self}")
            tail_coords = self._tail
            head_coords = self._head

            if self._right_node:
                #print(f"Labeling with {color} {self._right_node.id}")
                r_label = label_loc_xy(tail_coords, head_coords, 10)
                draw.text(r_label.as_tuple(), str(self._right_node.id), color)
            if self._left_node:
                #print(f"Labeling with {color} {self._left_node.id}")
                l_label = label_loc_xy(tail_coords, head_coords, -10)
                draw.text(l_label.as_tuple(), str(self._left_node.id), color)

    def show(self, labels=None, color=None, width=None):
        ''' Display the Edge '''

        img_size = XY(max(self._tail.x, self._head.x), max(self._tail.y, self._head.y)) + Edge._CANVAS_PADDING
        img = Image.new("RGBA", img_size.as_tuple(), Edge._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw, labels, color, width)

        img.show()

    def _rel_repr(self, vertex):
        if vertex is self._tail:
            near = self._tail
            far = self._head
        elif vertex is self._head:
            near = self._head
            far = self._tail
        else:
            #TIDY correct exception? need to find a reference on
            # python exception philosophy
            raise ValueError(f"{vertex} is not connected to {self}")

        left_node = None
        right_node = None

        if self.rel_side("left", vertex):
            left_node = self.rel_side("left", vertex).id
        if self.rel_side("right", vertex):
            right_node = self.rel_side("right", vertex).id

        return f"{near._repr_coords()}-{left_node}|{right_node}-{far._repr_coords()}"

    def __repr__(self):

        left_node = None
        if self._left_node:
            left_node = self._left_node.id

        right_node = None
        if self._right_node:
            right_node = self._right_node.id

        return f"{self._tail._repr_coords()}-{left_node}|{right_node}-{self._head._repr_coords()}"
