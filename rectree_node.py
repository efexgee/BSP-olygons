#!/usr/bin/env python

from xy import XY
from statistics import mean

class Node():
    ''' node for a binary tree of Rectangles '''

    def __init__(self, id, parent, child_a=None, child_b=None):
        self.id = id

        #I don't think we ever use the parent pointer but
        # it doesn't cost much and can be super-useful
        self.parent = parent
        self.a = child_a
        self.b = child_b

        self.vertices = []
        self.edges = []

    def add_polygon(self, vertices, edges):
        #TODO just for testing
        self.vertices = vertices
        self.edges = edges

    def centroid(self):
        ''' Return the centroid of a Node '''

        #TODO lists or sets? I think lists
        x = []
        y = []

        for vertex in self.vertices:
            x.append(vertex._x)
            y.append(vertex._y)

        return XY(round(mean(x)), round(mean(y)))

    def __repr__(self):
        ''' DEBUG: Currently the format is: "Node <id>"

        Format: "<id> - p: (<parent>) a: (<child_a>) b: (<child_b>) rect: <rectangle>"'''

        #DEBUG - enable using dummy nodes (i.e. ints)
        if hasattr(self.parent, "id"):
            parent = self.parent.id
        else:
            parent = self.parent

        #TODO there must be a saner way to do this
        if self.a is None:
            a = " "
        else:
            a = self.a.id

        if self.b is None:
            b = " "
        else:
            b = self.b.id

        return f"({parent}) <- ({self.id}) -> ({a}) ({b}) [{len(self.edges)} edges, {len(self.vertices)} vertices]"
        #DEBUG - for readability
        #return f"Node {self.id}"
