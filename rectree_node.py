#!/usr/bin/env python

from xy import XY
from statistics import mean

class Node():
    ''' node for a binary tree of Rectangles '''

    def __init__(self, id, parent, registry, child_a=None, child_b=None):
        self.id = id

        #I don't think we ever use the parent pointer but
        # it doesn't cost much and can be super-useful
        self.parent = parent
        self.registry = registry
        self.child_a = child_a
        self.child_b = child_b

    def vertices(self):
        #HELP switched to list so I didn't have to hash a mutable
        vertices = []

        for edge in self.registry.get_edges(self):
            print(f"processing edge {edge}")
            for vertex in edge.vertices():
                if vertex not in vertices:
                    print(f"adding edge {edge}")
                    vertices += edge.vertices()

        return vertices

    def centroid(self):
        ''' Return the centroid of a Node '''

        x = []
        y = []

        for vertex in self.vertices():
            print(f"processing vertex {vertex}")
            x.append(vertex._x)
            y.append(vertex._y)

        return XY(round(mean(x)), round(mean(y)))

    def __repr__(self):
        if self.parent is None:
            parent = " "
        else:
            parent = self.parent.id

        if self.child_a is None:
            a = " "
        else:
            a = self.child_a.id

        if self.child_b is None:
            b = " "
        else:
            b = self.child_b.id

        return f"({parent}) <- ({self.id}) -> ({a}) ({b})"
