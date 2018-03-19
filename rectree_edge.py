#!/usr/bin/env python

#TODO check private attributes and methods in all modules

from PIL import Image, ImageDraw
from xy import *
from label import *

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

    def get_other_vertex(self, caller):
        #TODO get_blah() vs. plain blah()?
        if caller is self._tail:
            return self._head
        elif caller is self._head:
            return self._tail
        else:
            #TODO wrong exception type; see above
            raise KeyError(f"{caller} is not part of {self}")

    def get_rel_side(self, side, caller):
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
        #TODO just to avoid touching the privates. too many methods?
        return self._tail, self._head

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

    def add_to_draw(self, draw, labels=False, color=_DEFAULT_LINE_COLOR, width=_DEFAULT_LINE_WIDTH):
        ''' Add Edge to the specified PIL draw object '''

        #print(f"Edge: adding {self} in {color}")
        draw.line((self._tail.as_tuple(), self._head.as_tuple()), fill=color, width=width)

        if labels:
            #print(f"Labeling {self}")
            tail_coords = self._tail
            head_coords = self._head

            if self._right_node:
                #print(f"Labeling with {color} {self._right_node.id}")
                r_label = label_loc_xy(tail_coords, head_coords, 10)
                draw.text(r_label.as_tuple(), self._right_node.id, color)
            if self._left_node:
                #print(f"Labeling with {color} {self._left_node.id}")
                l_label = label_loc_xy(tail_coords, head_coords, -10)
                draw.text(l_label.as_tuple(), self._left_node.id, color)

    def show(self, labels=None, color=None, width=None):
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
        if labels:
            #TODO defaulting labels to None to keep only one default
            args["labels"] = labels

        self.add_to_draw(draw, **args)

        img.show()

    def _rel_repr(self, vertex):
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

        left_node = None
        right_node = None

        if self.get_rel_side("left", vertex):
            left_node = self.get_rel_side("left", vertex).id
        if self.get_rel_side("right", vertex):
            right_node = self.get_rel_side("right", vertex).id

        return f"{near._repr_coords()}-{left_node}|{right_node}-{far._repr_coords()}"

    def __repr__(self):
        #TODO how do I deal with this?
        left_node = None
        right_node = None

        if self._left_node:
            left_node = self._left_node.id
        if self._right_node:
            right_node = self._right_node.id

        return f"{self._tail._repr_coords()}-{left_node}|{right_node}-{self._head._repr_coords()}"
