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
        self.a = child_a
        self.b = child_b

    def add_polygon(self, vertices, edges):
        #TODO just for testing
        raise NotImplementedError("not sure I will even want this")

    def vertices(self):
        #TODO [] vs list()
        vertices = set()

        for edge in self.registry.get_edges(self):
            vertices.update(set(edge.vertices()))

        #TODO Don't return in special data types unless necessary?
        return tuple(vertices)

    def centroid(self):
        ''' Return the centroid of a Node '''

        #TODO lists or sets? I think lists
        x = []
        y = []

        #TODO map() or something?
        for vertex in self.vertices():
            x.append(vertex._x)
            y.append(vertex._y)

        return XY(round(mean(x)), round(mean(y)))

    def __repr__(self):
        #TODO there must be a saner way to do this
        if self.parent is None:
            parent = " "
        else:
            parent = self.parent.id

        if self.a is None:
            a = " "
        else:
            a = self.a.id

        if self.b is None:
            b = " "
        else:
            b = self.b.id

        return f"({parent}) <- ({self.id}) -> ({a}) ({b})"
