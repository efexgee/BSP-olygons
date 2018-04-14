#!/usr/bin/env python

from termcolor import colored
from polytree.edge import Edge
from random import choice
from polytree.xy import XY
from polytree.functions import follow_edges, most_opposite_edge
from polytree.vertex import Vertex
#from statistics import mean

class Side(Edge):
    ''' One side of a polygon '''

    def __init__(self, tail, head, edges=None):
        # We're not using the side nodes so they're None
        super().__init__(tail, head, None, None)

        #HELP this makes them all have the same edges list :(
        #self.edges = edges

        self.edges = list(edges)

    def __repr__(self):
        return f"{colored(self._tail.as_tuple(),'cyan')} -> {colored(self._head.as_tuple(),'cyan')}: {self.edges}"

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
        # Pick an arbitrary Vertex on the Node
        starting_vertex = self.vertices[0]

        # We'll be returning this list of Sides
        sides = []

        # The Edges compromising the current Side we're building
        side_edges = []

        side_tail = None

        #HELP better name than thing?
        def build_sides(thing):
            # Visitor to send around the polygon
            #HELP scope dealing with
            nonlocal side_tail
            #nonlocal sides
            if isinstance(thing, Vertex):
                #print(f"Thing is a Vertex")
                if thing in self.vertices:
                    #print(f"Thing is a Vertex of Node")
                    if side_tail:
                        # We have completed a Side
                        sides.append(Side(side_tail, thing, side_edges))
                        #HELP dealing with scope
                        side_edges.clear()
                    side_tail = thing
            elif isinstance(thing, Edge):
                #print(f"Thing is an Edge")
                side_edges.append(thing)
                pass
            else:
                assert False, f"{thing} is of type {type(thing)}"

        follow_edges(starting_vertex, starting_vertex, self, build_sides)

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
        edges = self.get_edges()

        edges.remove(edge)

        return most_opposite_edge(edge, edges)

    def get_rnd_side(self, exclude=None):
        #TODO do I need exclusions anymore?
        sides = self.get_sides()

        if exclude:
            for exclusion in exclude:
                sides.remove(exclusion)

        return choice(sides)

    def get_opp_side(self, side):
        sides = self.get_sides()
        print(f"Source Side: {side}")

        sides.remove(side)
        print(f"Other Sides: {sides}")

        return most_opposite_edge(side, sides)

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
