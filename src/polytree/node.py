#!/usr/bin/env python

from termcolor import colored
from polytree.edge import Edge
from random import choice
from polytree.xy import Coord
from polytree.functions import follow_edges, most_opposite_edge
from polytree.vertex import Vertex
from polytree.line import Line
from polytree.side import Side
from polytree.globals import *
from statistics import mean

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

        def build_sides(item):
            # Visitor to send around the polygon
            nonlocal side_tail

            if isinstance(item, Vertex):
                #print(f"Thing is a Vertex")
                if item in self.vertices:
                    #print(f"Thing is a Vertex of Node")
                    if side_tail:
                        # We have completed a Side
                        sides.append(Side(side_tail, item, side_edges))
                        side_edges.clear()
                    side_tail = item
            elif isinstance(item, Edge):
                #print(f"Thing is an Edge")
                side_edges.append(item)
            else:
                raise TypeError(f"{item} is of type {type(item)}")

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
        #TODO Still used?
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
        #print(f"Source Side: {side}")

        sides.remove(side)
        #print(f"Other Sides: {sides}")

        return most_opposite_edge(side, sides)

    def centroid(self):
        ''' Return the centroid of a Node '''

        assert self.vertices is not None, "Node's vertices should never be None"

        x = []
        y = []

        for vertex in self.vertices:
            #print(f"processing vertex {vertex}")
            x.append(vertex.x)
            y.append(vertex.y)

        return Coord(round(mean(x)), round(mean(y)))

    def get_neighbors(self):
        neighbors = []

        for edge in self.registry.get_edges(self):
            for node in edge.nodes():
                if node is not None and node is not self and node not in neighbors:
                    neighbors.append(node)

        return neighbors

    def add_to_draw(self, draw, label=None, color=None, label_color=None, fill_color=None, width=None):

        color = DEFAULT_LINE_COLOR if color is None else color
        label = DEFAULT_SHOW_LABELS if label is None else label
        # Label color defaults to the line color
        label_color = color if label_color is None else label_color

        #HELP not smooth, I know, but only this one time!
        polygon_coords = [vertex.as_tuple() for vertex in self.vertices]
        print(polygon_coords)

        if fill_color is None:
            draw.polygon(polygon_coords, outline=color)
        else:
            draw.polygon(polygon_coords, outline=color, fill=fill_color)

        if label:
            #print(f"Labeling {self}")
            draw.text(self.centroid().as_tuple(), str(self.id), label_color)

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
            vertices = "\n".join([v.__repr__() for v in self.vertices])
        else:
            vertices = None
        return f"({parent}) <- ({self.id}) -> ({a}) ({b}) : {[v.coords() for v in self.vertices]}"
