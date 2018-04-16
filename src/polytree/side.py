#!/usr/bin/env python

from termcolor import colored
from polytree.edge import Edge
from polytree.line import Line

class Side(Edge):
    ''' One side of a polygon '''

    def __init__(self, tail, head, edges=None):
        # We're not using the side nodes so they're None
        super().__init__(tail, head, None, None)

        #HELP having to do this is just a fact of life, right?
        self.edges = list(edges)

    def edge_containing(self, xy):
        # Check which Edge's bounding box contains the coords

        print(f"  Looking for Edge containing {xy}")

        #TODO bounding boxes share borders
        for edge in self.edges:
            print(f"  Looking for {xy} on {edge}")
            
            #HELP how to check for "between"?
            if min(edge._tail._x, edge._head.x) <= xy._x <= max(edge._tail._x, edge._head._x) and \
                min(edge._tail._y, edge._head._y) <= xy._y <= max(edge._tail._y, edge._head._y):
                    # We found our Edge
                    print(f"  {edge} contains {xy}")
                    return edge

    def find_point(self, percentage):
        return Line(self._tail, self._head).find_point(percentage)

    def vertices(self):
        vertices = []

        for edge in self.edges:
            for vertex in edge.vertices():
                if vertex not in vertices:
                    vertices.append(vertex)

        return vertices

    def __repr__(self):
        return f"{colored(self._tail.as_tuple(),'cyan')} -> {colored(self._head.as_tuple(),'cyan')}: {self.edges}"
