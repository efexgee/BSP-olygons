#!/usr/bin/env python

from polytree.xy import XY
from statistics import mean
from random import choice
from math import inf

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

        def edge_slope(edge):
            #TODO HELP Disaster kludge!!!
            rise_run = XY(edge._head.as_tuple()) - XY(edge._tail.as_tuple())
            print(f"Got rise_run of {rise_run}")

            #HELP no reason to make this a single if, right?
            if rise_run._x == 0:
                #print(f"    Assigning slope inf to vertical edge {edge}")
                # Vertical line
                # Using infinity as the slope of the LineSegment instead of
                # the correct undefined so I can compare the slopes of
                # two LineSegments
                return inf

            # Convert to positive X
            if rise_run._x < 0:
                print(f"    Converting {rise_run} to {rise_run * -1}")
                rise_run *= -1

            return rise_run._y / rise_run._x

        slope = edge_slope(edge)
        print(f"Matching {edge} {slope}")
        print()

        best_opp_edge = None
        best_slope_diff = None

        for other_edge in self.get_edges():
            #DEBUG could wait to calc this
            other_slope = edge_slope(other_edge)
            print(f"{other_edge} {other_slope}")

            if other_edge is edge:
                # Skip the edge we're trying to match
                print(f"    Skipping the edge we're trying to match: {other_edge}")
                continue

            if slope is inf and other_slope is inf:
                slope_diff = 0
            else:
                slope_diff = abs(other_slope - slope)
            print(f"    {other_edge} {other_slope} has slope diff of {slope_diff}")

            if best_opp_edge:
                if slope_diff < best_slope_diff:
                    print(f"    Found new best edge: {slope_diff} < {best_slope_diff}")
                    best_opp_edge = other_edge
                    best_slope_diff = slope_diff
            else:
                # Nothing to compare to
                print(f"    Initializing: {other_edge} {other_slope} has slope diff of {slope_diff}")
                #HELP any sane way to avoid repeating these two lines?
                best_opp_edge = other_edge
                best_slope_diff = other_slope

        print(f"Best opposite edge is {best_opp_edge} with slope {other_slope}")
        return best_opp_edge
            

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
