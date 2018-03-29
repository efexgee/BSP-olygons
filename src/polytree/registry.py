#!/usr/bin/env python

from collections import UserList
from polytree.edge import *
from polytree.node import *

class EdgeRegistry(UserList):
    ''' A list of Edges that can be addressed by their LineSegments '''

    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_HIGHLIGHT_COLOR = "pink"

    def _get_edges_by_vertex(self, vertex):
        ''' [Helper for .get_edges()] Return all Edges which contain the vertex '''
        edges = []

        for edge in self:
            if edge.line.has_vertex(vertex):
                edges.append(edge)

        if edges:
            return result
        else:
            raise KeyError(f"Vertex {vertex} is not in {self}")

    def _get_edges_by_node(self, node):
        ''' [Helper for .get_edges()] Return the Edges which contain the Node '''
        edges = []

        for edge in self:
            if edge.describes(node):
                edges.append(edge)

        if edges:
            return EdgeRegistry(edges)
        else:
            raise KeyError(f"Node {node} is not in {self}")

    def get_edges(self, value):
        ''' Return a list of Edges which contain a vertex or a Node '''
        if isinstance(value, Node):
            return self._get_edges_by_node(value)
        elif isinstance(value, XY):
            return self._get_edges_by_vertex(value)
        else:
            raise TypeError(f"Can't retrieve Edges based on type of {value}: {type(value)}")

    def add_node_to_draw(self, node, draw, color=None, width=None):
        ''' Add the polygon for a Node to a PIL draw object '''
        args = {}
        
        if color:
            args["color"] = color
        if width:
            args["width"] = width

        self._get_edges_by_node(node).add_to_draw(draw, **args)

    def show_node(self, node, color=None, width=None):
        ''' Draw the polygon for a Node '''
        args = {}
        
        if color:
            args["color"] = color
        if width:
            args["width"] = width

        img_size = self.canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        self.add_node_to_draw(node, draw, **args)

        img.show()

    def add_to_draw(self, draw, highlight=None, highlight_color=None, labels=None, color=None, width=None):
        ''' Add all Edges to a PIL Draw object '''

        highlight_color = EdgeRegistry._DEFAULT_HIGHLIGHT_COLOR if highlight_color is None else highlight_color

        highlighted_edges = []

        #HELP is this if, for goofy?
        if highlight:
            #HELP [*var] or list(var)?
            #HELP still don't know how to expand this
            for highlighted in [*highlight]:
                if isinstance(highlighted, Edge):
                    #HELP did we just say not to use .append? I think not
                    highlighted_edges.append(highlighted)
                elif isinstance(highlighted, Node):
                    highlighted_edges += self._get_edges_by_node(highlighted)
                else:
                    raise TypeError(f"Can't highlight Edges by type {type(highlighted)}: {highlighted}")

        for edge in self:
            #print(f"EdgeRegistry: adding {edge} to {draw}")
            if edge in highlighted_edges:
                color = highlight_color
            else:
                color = None

            edge.add_to_draw(draw, labels, color, width)

    def show(self, highlight=None, highlight_color=None, labels=None, color=None, width=None):
        ''' Display all the Edges '''

        img_size = self.canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw, highlight, highlight_color, labels, color, width)

        img.show()

    def canvas_size(self):
        ''' Return the size an Image has to be to fit all the Edges '''
        max_x = 0
        max_y = 0

        # This is a very inefficient traversal
        #HELP using max here seems fine, but maybe build a set?
        for edge in self:
            max_x = max(max_x, edge._tail._x, edge._head._x)
            max_y = max(max_y, edge._tail._y, edge._head._y)

        assert max_x * max_y > 0, f"Canvas size can't have a zero in it: ({max_x}, {max_y})"
            
        return XY(max_x, max_y)

    def __repr__(self):
        output = ""
        for edge in self:
            #TODO list comprehension with a join
            output += f"{str(edge)} \n"

        return output
