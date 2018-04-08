#!/usr/bin/env python

from termcolor import colored
from polytree.edge import Edge
from random import choice
from polytree.xy import XY
from math import degrees, acos
from polytree.functions import visit_polygon
from polytree.vertex import Vertex
#from statistics import mean
#from collections import UserList

class Side(Edge):
    ''' One side of a polygon '''

    def __init__(self, tail, head, edges=None):
        # We're not using the side nodes so they're None
        super().__init__(tail, head, None, None)

        self.edges = edges

    def __repr__(self):
        return f" Tail: {colored(self._tail.as_tuple(),'cyan')} Head: {colored(self._head.as_tuple(),'cyan')}\nEdges: {super().__repr__()}"

class Node():
    ''' node for a binary tree of Rectangles '''

    def __init__(self, id, parent, registry, child_a=None, child_b=None, vertices=None):
        self.id = id

        #I don't think we ever use the parent pointer but
        # it doesn't cost much and can be super-useful
        self.parent = parent
        self.registry = registry
        self.child_a = child_a
        self.child_b = child_b
        self.vertices = vertices

    def add_vertices(self, vertices):
        # Need to handle root Node creation at which point
        # the Vertices are not defined yet
        self.vertices = vertices

    def get_edges(self):
        return self.registry.get_edges(self)

    def get_sides(self):
        starting_vertex = self.vertices[0]

        sides = []

        side_tail = starting_vertex
        side_edges = []

        #HELP better name than thing?
        def build_sides(thing):
            # Visitor to send around the polygon
            #HELP scope dealing with
            nonlocal side_tail
            if isinstance(thing, Vertex):
                #print(f"Thing is a Vertex")
                if thing in self.vertices:
                    #print(f"Thing is a Vertex of Node")
                    sides.append(Side(side_tail, thing, side_edges))
                    side_tail = thing
                    #HELP dealing with scope
                    side_edges.clear()
            elif isinstance(thing, Edge):
                #print(f"Thing is an Edge")
                side_edges.append(thing)
            else:
                assert False, f"{thing} is of type {type(thing)}"


        visit_polygon(starting_vertex, self, build_sides)

        return sides

    #HELP how about this bizarre exclusion option?
    def get_rnd_edge(self, exclude=None):
        edges = self.get_edges()

        #print(f"edges = {edges}")

        if exclude:
            for exclusion in exclude:
                #print(f"removing {edge}")
                edges.remove(exclusion)

        #print(f"edges = {edges}")
        return choice(edges)

    def get_opp_edge(self, edge):
        # The "intuitively opposing" edge doesn't always
        # make for the most right angle

        def angle_between(edge_a, edge_b):
            #print(f"Getting angle between edges {edge_a} and {edge_b}")
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

        assert self.vertices is not None, "Node's vertices should never be None"

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

        if self.vertices:
            vertices = "\n ".join([v.__repr__() for v in self.vertices])
        else:
            vertices = None
        return f"({parent}) <- ({self.id}) -> ({a}) ({b}) :\n {vertices}"
