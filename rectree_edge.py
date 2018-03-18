#!/usr/bin/env python

#TODO check private attributes and methods in all modules

from PIL import Image, ImageDraw
from xy import *

class Edge():
    ''' Connects two Vertices and the Nodes shared by the Edge '''

    # Padding when displaying Edges on their own
    _CANVAS_PADDING = 10
    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_LINE_COLOR = "black"
    _DEFAULT_LINE_WIDTH = 2

    def __init__(self, tail, head, left_node, right_node):
        self._tail = None
        self._head = None

        tail.connect_outbound(self)
        self.connect_into(head)
        # Forcing the user to explicitly specify None in the
        # case of an exterior edge by not providing defaults
        self._left_node = left_node      # should only be changed via replace()
        self._right_node = right_node    # should only be changed via replace()

    def describes(self, node):
        ''' Check whether Edge is part of a Node '''
        return node in (self._left_node, self._right_node)

    def split(self, point):
        ''' Split Edge at point XY and return two new Edges
            which have the same associated Nodes '''

        raise NotImplemented(".split() is currently broken")

        try:
            rear_segment, front_segment = super().split(point)
        #TODO different ways to handle re-raising
        except KeyError:
            raise KeyError(f"{point} is not on {edge}")
        except ValueError as e:
            raise ValueError(e.message.replace("LineSegment", "Edge"))

        raise NotImplemented("split won't work now")
        rear_edge = Edge(rear_segment, edge._left_node, edge._right_node)
        front_edge = Edge(front_segment, edge._left_node, edge._right_node)

        return rear_edge, front_edge

    def replace(self, old_node, new_node):
        ''' Replace a Node associated with an Edge
            This the only way Edges' Nodes should be
            changed '''
        if self._left_node == old_node:
            self._left_node = new_node
        elif self._right_node == old_node:
            self._right_node = new_node
        else:
            #TODO custom exception or ValueError as last resort
            raise KeyError(f"{old_node} not attached to {self}")

    def get_rel_right(self, caller):
        ''' Return the right node as seen from the referrer POV '''
        if caller is self._tail:
            return self._right_node
        elif caller is self._head:
            return self._left_node
        else:
            #TODO double-check that this is an OK exception
            #TODO it feels like a KeyError but I'm told it's not, I think
            raise RuntimeError(f"{caller} is neither {self._tail} nor {self._head}")

    def vertices(self):
        #TODO just to avoid touching the privates. too many methods?
        return self._tail, self._head

    def get_rel_left(self, caller):
        #TODO get_rel_left or rel_left?
        #TODO methods masquerading as attributes? no! assignments, right?
        ''' Return the left node as seen from the referrer POV '''
        if caller is self._tail:
            return self._left_node
        elif caller is self._head:
            return self._right_node
        else:
            raise RuntimeError(f"{caller} is neither {self._tail} nor {self._head}")

    def _connect_from(self, vertex):
        ''' Connect to a vertex '''
        assert not self._tail, f"_tail of {self} is already set: {self._tail}"
        self._tail = vertex

    def _connect_to(self, vertex):
        #TODO this one should never get used, I think
        assert not self._head, f"_head of {self} is already set: {self._head}"
        self._head = vertex

    def connect_into(self, vertex):
        self._connect_to(vertex)
        vertex._connect(self)

    def add_to_draw(self, draw, color=_DEFAULT_LINE_COLOR, width=_DEFAULT_LINE_WIDTH):
        ''' Add Edge to the specified PIL draw object '''

        #print(f"Edge: adding ({self._tail._repr_coords()}-{self._head._repr_coords()}) to {draw} in {color}")
        draw.line((self._tail.as_tuple(), self._head.as_tuple()), fill=color, width=width)

        #TODO label with the two nodes, which is going to
        # be a bit of a big to-do
        #TODO I really don't want to write the code to find these points
        #midpoint = self._tail + (self._head - self._tail) // 2

    def show(self, color=None, width=None):
        ''' Display the Edge '''

        img_size = XY(max(self._tail.x, self._head.x), max(self._tail.y, self._head.y)) + Edge._CANVAS_PADDING
        img = Image.new("RGBA", img_size.as_tuple(), Edge._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        args = {}
        #TODO this doesn't feel right
        if color:
            args["color"] = color
        if width:
            args["width"] = width

        self.add_to_draw(draw, **args)

        img.show()

    def _rel_repr(self, vertex):
        #TODO how many stars?
        if vertex is self._tail:
            near = self._tail
            far = self._head
        elif vertex is self._head:
            near = self._head
            far = self._tail
        else:
            #TODO correct exception? need to find a reference on
            # python exception philosophy
            raise ValueError(f"{vertex} is not connected to {self}")
        #TODO should there be .get_rel_butt() and face?
        return f"{near._repr_coords()}-{self.get_rel_left(vertex)}|{self.get_rel_right(vertex)}-{far._repr_coords()}"

    def __repr__(self):
        return f"{self._tail._repr_coords()}-{self._left_node}|{self._right_node}-{self._head._repr_coords()}"
