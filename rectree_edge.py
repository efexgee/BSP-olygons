#!/usr/bin/env python

from PIL import Image, ImageDraw

#TODO How do I import this cleanly?
#from line import *
# star-imports are gross
#import line
# have to reference with module name
#from line import LineSegment as LineSegment, XY as XY
from line import *
#TODO assume I should not import XY unless I use XY in this file

#TODO inherit from LineSegment
# .split() would be like Edge.split() but it
# would call super().split()

#TODO should Edge be "immutable"?
# use read-only properties

class Edge(LineSegment):
    ''' a LineSegment and two Nodes '''

    def __init__(self, tail, head, left_node, right_node):
        # Asking the user to explicitly specify None in the
        # case of an exterior edge
        super().__init__(tail, head)    # should be immutable
        self.left_node = left_node      # should only be changed via replace()
        self.right_node = right_node    # should only be changed via replace()

    def describes(self, node):
        ''' Check whether Edge is part of a Node '''
        return node in (self.left_node, self.right_node)

    def split(self, point):
        ''' Split Edge at point XY and return two new Edges
            which have the same associated Nodes '''
        try:
            #TODO does the exception handling change now that I am a subclass?
            rear_segment, front_segment = super().split(point)
        #TODO different ways to handle re-raising
        except KeyError:
            raise KeyError(f"{point} is not on {edge}")
        except ValueError as e:
            raise ValueError(e.message.replace("LineSegment", "Edge"))

        rear_edge = Edge(rear_segment, edge.left_node, edge.right_node)
        front_edge = Edge(front_segment, edge.left_node, edge.right_node)

        return rear_edge, front_edge

    def replace(self, old_node, new_node):
        ''' Replace a Node associated with an Edge
            This the only way Edges' Nodes should be
            changed '''
        if self.left_node == old_node:
            self.left_node = new_node
        elif self.right_node == old_node:
            self.right_node = new_node
        else:
            #TODO custom exception or ValueError as last resort
            raise KeyError(f"{old_node} not attached to {self}")

    def get_rel_right(self, caller):
        ''' Return the right node as seen from the referrer POV '''
        #TODO should this have default behavior for None?
        # I think that's just messy
        if caller is self.tail:
            return self.right_node
        elif caller is self.head:
            return self.left_node
        else:
            raise RuntimeError(f"{caller} is neither {self.tail} nor {self.head}")

    def get_rel_left(self, caller):
        ''' Return the left node as seen from the referrer POV '''
        if caller is self.tail:
            return self.left_node
        elif caller is self.head:
            return self.right_node
        else:
            raise RuntimeError(f"{caller} is neither {self.tail} nor {self.head}")

    def _connect(self, vertex):
        ''' Connect to a vertex '''
        self.tail = vertex

    #TODO something not right here

    def couple(self, vertex):
        ''' '''
        self.head = vertex
        vertex._connect(self)

    def add_to_draw(self, draw, color=None, width=None):
        ''' Add Edge to the specified PIL draw object '''
        #TODO self.line.add_to_draw(**{arg: val})

        #TODO wouldn't need super() if I weren't planning on adding
        # the node labels, right?
        super().add_to_draw(draw)
        #TODO label with the two nodes
        # This is going to be a bit of a to-do

    def show(self):
        ''' Show the LineSegment of the Edge '''
        #TODO support colors
        img_size = self.get_canvas_size()

        #TODO how do class attributes work now?
        img = Image.new("RGBA", img_size.as_tuple(), LineSegment._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        #TODO is this how __repr__ with class inheritance is done?
        return f"{super().__repr__()}: {self.left_node}, {self.right_node}"
