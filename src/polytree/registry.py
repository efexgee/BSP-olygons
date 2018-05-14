#!/usr/bin/env python

from collections import UserList
from polytree.node import Node
from polytree.xy import XY
from polytree.edge import Edge
from polytree.globals import *

class EdgeRegistry(UserList):
    ''' A list of Edges that can be addressed by their LineSegments '''

    def _get_edges_by_node(self, node):
        ''' [Helper for .get_edges()] Return the Edges which contain the Node '''
        edges = []

        for edge in self:
            if edge.borders_node(node):
                edges.append(edge)

        if edges:
            return EdgeRegistry(edges)
        else:
            raise KeyError(f"Node {node} is not in registry {self}")

    def get_edges(self, value):
        ''' Return a list of Edges which contain a vertex or a Node '''
        #RELEASE Supports look-ups by other types, but is not used right now
        if isinstance(value, Node):
            return self._get_edges_by_node(value)
        else:
            raise TypeError(f"Can't retrieve Edges based on type of {value}: {type(value)}")

    def add_to_draw(self, draw, highlight=None, highlight_color=None, labels=None, color=None, label_color=None, width=None):
        ''' Add all Edges to a PIL Draw object '''

        highlight_color = DEFAULT_HIGHLIGHT_COLOR if highlight_color is None else highlight_color

        highlighted_edges = []

        if highlight:
            for highlighted in highlight: 
                #HELP how do I do this correctly?
                #TODO should have tuples of highlighted and colors
                if isinstance(highlighted, Edge):
                    highlighted_edges.append(highlighted)
                elif isinstance(highlighted, Node):
                    highlighted_edges += self._get_edges_by_node(highlighted)
                else:
                    raise TypeError(f"Can't highlight Edges by type {type(highlighted)}: {highlighted}")

        for edge in self:
            if edge in highlighted_edges:
                edge_color = highlight_color
            else:
                edge_color = color

            #print(f"EdgeRegistry: adding {edge} to {draw}: labels={labels} color={edge_color} width={width}")
            edge.add_to_draw(draw, labels, edge_color, width)

    #ASK on the fence on @property vs. method
    def canvas_size(self):
        ''' Return the size an Image has to be to fit all the Edges '''
        max_x = 0
        max_y = 0

        # This is a very inefficient traversal
        for edge in self:
            max_x = max(max_x, edge._tail.x, edge._head.x)
            max_y = max(max_y, edge._tail.y, edge._head.y)

        assert max_x * max_y > 0, f"Canvas size can't have a zero in it: ({max_x}, {max_y})"
            
        return XY(max_x, max_y)

    def __repr__(self):
        if len(self) > 10:
            return f"[Registry contains {len(self)} Edges]"
        else:
            return super().__repr__()
