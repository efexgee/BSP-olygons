#!/usr/bin/env python

from termcolor import colored
from polytree.edge import Edge
from polytree.line import Line

class Side(Edge):
    ''' One side of a polygon '''

    def __init__(self, tail, head, edges=None):
        # We're not using the side nodes so they're None
        super().__init__(tail, head, None, None)

        if edges is None:
            self.edges = []
        else:
            self.edges = list(edges)

    def edge_containing(self, xy):
        # Check which Edge's bounding box contains the coords

        #print(f"  Looking for Edge containing {xy}")

        #TODO bounding boxes share borders
        for edge in self.edges:
            #print(f"  Looking for {xy} on {edge}")
            if xy.is_in_box(edge._tail, edge._head):
                    # We found our Edge
                    return edge

    def find_point(self, percentage):
        return Line(self._tail, self._head).find_point(percentage)

    @property
    def vertices(self):
        vertices = []

        for edge in self.edges:
            for vertex in edge.vertices:
                if vertex not in vertices:
                    vertices.append(vertex)

        return vertices

    def __repr__(self):
        return f"{colored(self._tail.as_tuple(),'cyan')} -> {colored(self._head.as_tuple(),'cyan')}: {self.edges}"
