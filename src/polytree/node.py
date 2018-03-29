#!/usr/bin/env python

from polytree.xy import XY
from statistics import mean
from random import choice
from math import degrees, acos
from polytree.edge import Edge

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
            #print(f"processing edge {edge}")
            for vertex in edge.vertices():
                if vertex not in vertices:
                    #print(f"adding edge {edge}")
                    vertices += edge.vertices()

        return vertices

    def get_edges(self):
        return self.registry.get_edges(self)

    #HELP how about this bizarre exclusion option?
    #HELP do I make the default an empty list to convey it's a list?
    def get_rnd_edge(self, exclude=[]):
        edges = self.get_edges()

        #print(f"edges = {edges}")

        for exclusion in exclude:
            #print(f"removing {edge}")
            edges.remove(exclusion)

        #print(f"edges = {edges}")
        return choice(edges)

    def get_opp_edge(self, edge):

        def angle_between(edge_a, edge_b):
            #print(f"Getting angle between edges {edge_a} and {edge_b}")
            #TODO HELP XY-casting is hack for hilarious XYCoord disaster
            vector_a = XY(edge_a._head) - XY(edge_a._tail)
            vector_b = XY(edge_b._head) - XY(edge_b._tail)
            #print(f"Getting angle between vectors {vector_a} (mag={vector_a.magnitude()}) and {vector_b} (mag={vector_b.magnitude()})")
            #print(f"Dot product of {vector_a} and {vector_b} is {vector_a.dot_product(vector_b)}")

            dp = vector_a.dot_product(vector_b)
            mags = vector_a.magnitude() * vector_b.magnitude()
            bloop = dp / mags
            rads = acos(bloop)
            angle = degrees(rads)
            #angle = degrees(acos(vector_a.dot_product(vector_b)/vector_a.magnitude() * vector_b.magnitude()))
            return angle


        edge_midpoint = edge.get_new_vertex(50)

        #print(f"Matching {edge} with midpoint {edge_midpoint}")

        best_angle = 0
        best_edge = None

        for other_edge in self.get_edges():
            # Skip the edge itself
            if other_edge is edge:
                #print(f"Skipping the edge to be matched: {other_edge}")
                continue

            other_midpoint = other_edge.get_new_vertex(50)
            #print(f"Considering {edge} with midpoint {edge_midpoint._repr_coords()}")

            angle = angle_between(edge, Edge(edge_midpoint, other_midpoint, None, None))

            if abs(90 - angle) < abs(90 - best_angle):
                best_angle = angle
                best_edge = other_edge

        return best_edge

    def centroid(self):
        ''' Return the centroid of a Node '''

        x = []
        y = []

        for vertex in self.vertices():
            #print(f"processing vertex {vertex}")
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
