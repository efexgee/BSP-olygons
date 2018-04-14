#!/usr/bin/env python

#TIDY check private attributes and methods in all modules
from termcolor import colored

from polytree.line import Line
from polytree.ext_label import label_loc_xy
from polytree.vertex import Vertex
#from PIL import Image, ImageDraw

class Edge():
    ''' Connects two Vertices and the Nodes shared by the Edge '''

    _DEFAULT_SHOW_LABELS = True
    _DEFAULT_LABEL_COLOR = "black"

    def __init__(self, tail, head, left_node, right_node):
        #Needed if we use the connect methods below?
        self._tail = None
        self._head = None

        self.connect_tail(tail)
        self.connect_head(head)
        # Forcing the user to explicitly specify None in the
        # case of an exterior edge by not providing defaults
        self._left_node = left_node      # should only be changed via replace()
        self._right_node = right_node    # should only be changed via replace()

    #HELP call it borders_node(node) or borders(node)
    def borders_node(self, node):
        ''' Check whether Edge is part of a Node '''
        return node in (self._left_node, self._right_node)

    def side_of_node(self, node):
        if node is self._left_node:
            return "left"
        elif node is self._right_node:
            return "right"
        else:
            assert False, f"{node} is not on {self}"

    def get_new_vertex(self, percentage):
        #TODO this needs some refinement to make sure the
        # point is actually on the line, not right next to it
        #TODO should this support relative to caller?

        new_point = Line(self._tail, self._head).find_point(percentage)

        return Vertex(new_point)

    def split(self, percentage):
        #TODO should this support relative to caller?
        ''' Insert a new vertex percentage of the way from tail
        to head and return two new edges '''

        new_vertex = self.get_new_vertex(percentage)
        #print(f"      Created new vertex: {new_vertex}")

        tail_segment = Edge(self._tail, new_vertex, self._left_node, self._right_node)
        head_segment = Edge(new_vertex, self._head, self._left_node, self._right_node)
        #print(f"      Created new segments: {tail_segment} & {head_segment}")

        #print(f"      Updated Vertex: {new_vertex}")

        return tail_segment, new_vertex, head_segment

    def disconnect(self):
        # Disconnects itself from its Vertices
        # It will usually also have to be deleted from
        # an Edge Registry
        self._tail.disconnect_from(self)
        self._head.disconnect_from(self)

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
        #print(f"Looking for {id(caller)} among {id(self._right_node)} and {id(self._left_node)}")
        if side == "right":
            #print(f"Comparing to {id(self._right_node)}")
            if caller is self._tail:
                return self._right_node
            else:
                return self._left_node
        elif side == "left":
            #print(f"Comparing to {id(self._left_node)}")
            if caller is self._tail:
                return self._left_node
            else:
                return self._right_node
        else:
            raise ValueError(f"{caller} {colored('is neither','red')}\n{self._tail} {colored('nor','red')}\n{self._head}")

    def vertices(self):
        #FEATURE use property if I want to fake an attribute ("descriptor")
        return self._tail, self._head

    def connect_tail(self, vertex):
        assert not self._tail, f"_tail of {self} is already set: {self._tail}"
        self._tail = vertex
        vertex.add_edge(self)

    def connect_head(self, vertex):
        assert not self._head, f"_head of {self} is already set: {self._head}"
        self._head = vertex
        vertex.add_edge(self)

    def add_to_draw(self, draw, labels=None, color=None, width=None):
        ''' Add Edge to the specified PIL draw object '''
        #TODO do we need to handle label colors?

        labels = Edge._DEFAULT_SHOW_LABELS if labels is None else labels
        #FEATURE This is here to support label colors in the future
        label_color = Edge._DEFAULT_LABEL_COLOR if color is None else color

        #print(f"Edge: adding {self} in {color}")
        line = Line(self._tail, self._head)

        line.add_to_draw(draw, color, width)

        if labels:
            #print(f"Labeling {self}")
            tail_coords = self._tail
            head_coords = self._head

            if self._right_node:
                #print(f"Labeling with {color} {self._right_node.id}")
                r_label = line.label_coords("right")
                draw.text(r_label.as_tuple(), str(self._right_node.id), label_color)
            if self._left_node:
                #print(f"Labeling with {color} {self._left_node.id}")
                l_label = line.label_coords("left")
                draw.text(l_label.as_tuple(), str(self._left_node.id), label_color)

    def show(self, labels=None, color=None, width=None):
        ''' Display the Edge '''

        img_size = XY(max(self._tail.x, self._head.x), max(self._tail.y, self._head.y)) + Edge._CANVAS_PADDING
        img = Image.new("RGBA", img_size.as_tuple(), Edge._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw, labels, color, width)

        img.show()

    #HELP is this OK imp of __eq__?
    #HELP this only exists so I can compare Sides : \
    def __eq__(self, other):
        # Using == on the vertices because we want to match coordinates
        if self._tail == other._tail and self._head == other._head:
            # Using "is" on the Nodes because... that's right
            if self._left_node is other._left_node and self._right_node is other._right_node:
                return True

        return False

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

        return f"{colored(str(near.as_tuple()),'magenta')}-{left_node}|{right_node}-{colored(str(far.as_tuple()),'magenta')}"

    def __repr__(self):

        left_node = None
        if self._left_node:
            left_node = self._left_node.id

        right_node = None
        if self._right_node:
            right_node = self._right_node.id

        return f"{colored(str(self._tail.as_tuple()),'magenta')}-{left_node}|{right_node}-{colored(str(self._head.as_tuple()),'magenta')}"
