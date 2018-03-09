#!/usr/bin/env python

from PIL import Image, ImageDraw
from line import *

#TODO inherit from Line
# .split() would be like Edge.split() but it
# would call super().split()

#TODO should Edge be "immutable"?
# use read-only properties

class Edge():
    ''' a Line and two Nodes '''

    def __init__(self, line, node_a, node_b):
        # Asking the user to explicitly specify None in the
        # case of am exterior edge
        self.line = line        # should be immutable
        self.node_a = node_a    # should only be changed via replace()
        self.node_b = node_b    # should only be changed via replace()

    def describes(self, node):
        ''' Check whether Edge is part of a Node '''
        return node == self.node_a or node == self.node_b

    def split(self, point):
        ''' Split Edge at point XY and return two new Edges
            which have the same associated Nodes '''
        try:
            line_a, line_b = edge.line.split(point)
        except KeyError:
            raise KeyError(f"{point} is not on {edge}")
        except ValueError as e:
            raise ValueError(e.message.replace("Line", "Edge"))

        edge_a = Edge(line_a, edge.node_a, edge.node_b)
        edge_b = Edge(line_b, edge.node_a, edge.node_b)

        return edge_a, edge_b

    def has_vertex(self, vertex):
        ''' Check whether Edge has XY as one of its vertices '''
        return self.line.has_vertex(vertex)

    def replace(self, old_node, new_node):
        ''' Replace a Node associated with an Edge
            This the only way Edges' Nodes should be
            changed '''
        if self.node_a == old_node:
            self.node_a = new_node
        elif self.node_b == old_node:
            self.node_b = new_node
        else:
            #TODO custom exception or ValueError as last resort
            raise KeyError("{} not attached to {}".format(old_node, self))

    def add_to_draw(self, draw, color=None, width=None):
        ''' Add Edge to the specified PIL draw object '''
        #TODO self.line.add_to_draw(**{arg: val})

        self.line.add_to_draw(draw)
        #TODO label with the two nodes
        # This is going to be a bit of a to-do

    def show(self):
        ''' Show the Line of the Edge '''
        img_size = self.line.get_canvas_size()

        img = Image.new("RGBA", img_size.astuple(), Line._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        return "{}: {}, {}".format(self.line, self.node_a, self.node_b)
