#!/usr/bin/env python

#TODO how to pep8?

from polytree.registry import EdgeRegistry
from polytree.node import Node
from polytree.vertex import Vertex
from polytree.xy import XY
from polytree.edge import Edge
from PIL import Image, ImageDraw
#from random import sample
from polytree.functions import split_edge, update_edges_from_new_edge, follow_edges

class Tree():
    ''' a binary tree of Rectangles '''

    def __init__(self, dimensions):
        self.registry = EdgeRegistry()

        self.root = Node(0, None, self.registry)

        v_ul = Vertex(0,0)
        v_ur = Vertex(dimensions * XY(1,0))
        v_br = Vertex(dimensions)
        v_bl = Vertex(dimensions * XY(0,1))

        e_ulur = Edge(v_ul, v_ur, None, self.root)
        e_urbr = Edge(v_ur, v_br, None, self.root)
        e_brbl = Edge(v_br, v_bl, None, self.root)
        e_blul = Edge(v_bl, v_ul, None, self.root)

        self.root.add_vertices([v_ul, v_ur, v_br, v_bl])
        self.registry.extend((e_ulur, e_urbr, e_brbl, e_blul))

        # the highest ID currently in the tree
        self.max_id = 0

        self.canvas = dimensions

    def get(self, id):
        ''' return the Node with the specified id '''
        #TODO what happens if the node doesn't exist?
        def walk(cur, id):
            if cur is None:
                return
            elif cur.id == id:
                return cur

            found = walk(cur.child_a, id)
            if found:
                return found

            found = walk(cur.child_b, id)
            if found:
                return found

        return walk(self.root, id)

    def split(self, id, direction=None, location=50, even=False):
        ''' Split a Node into two Nodes, in direction, at percentage.
            Default direction is to split across the shorter
            dimension (random for squares), and at 50%. '''
        split_node = self.get(id)

        print(f"\n=== Splitting Node {id} {direction}-wise (probably into Node {self.max_id + 1} & Node {self.max_id + 2})")

        # Check if node exist
        #TODO should this be handled by .get()?
        if split_node is None:
            #TIDY IndexError?
            raise IndexError(f"Could not find Node {id}")
            return

        # Check if node is a leaf node
        if not ( split_node.child_a is None and split_node.child_b is None ):
            #TODO maybe this implicitly checks whether the Node exists?
            raise ValueError(f"Can't split non-leaf nodes. Node {id} has children: {split_node}")

        # Set default direction and check for valid direction
        if direction is None:
            # If no direction is specified, split across the short dimension or
            #TODO need to implement
            direction = "very not implemented!"
            # split randomly if it's a square

        if not direction.startswith(("v", "h")):
            raise ValueError(f"Direction has to start with 'v' or 'h' but is {direction}")

        #TODO this was a check splitting across the narrow dimension
        if even:
            edge_a = split_node.get_rnd_edge()
            edge_b = split_node.get_opp_edge(edge_a)
        else:
            #TODO HELP I think responsibilities are split funny now
            edge_a, edge_b = sample(self.registry.get_edges(split_node), 2)

        #print(f"  Splitting on Edges {edge_a} & {edge_b}")

        _, vertex_a, _ = split_edge(edge_a, location, self.registry)
        _, vertex_b, _ = split_edge(edge_b, location, self.registry)

        #print(f"  Created two new vertices: {vertex_a.as_tuple()} & {vertex_b.as_tuple()}")

        self.max_id += 1
        new_node_a = Node(self.max_id, split_node, self.registry, vertices=[vertex_a, vertex_b])
        self.max_id += 1
        new_node_b = Node(self.max_id, split_node, self.registry, vertices=[vertex_a, vertex_b])
        #print(f"  Created two new nodes: {new_node_a} & {new_node_b}")

        split_node.child_a = new_node_a
        split_node.child_b = new_node_b
        #print(f"  Updated child pointers on {split_node}")

        new_edge = Edge(vertex_a, vertex_b, new_node_a, new_node_b)
        #print(f"  Created a new edge: {new_edge}")

        self.registry.append(new_edge)

        update_edges_from_new_edge(new_edge, split_node)

        # Define visitor to find Vertices for the new Nodes
        def inherit_vertices(thing):
            if isinstance(thing, Vertex):
                if Vertex in split_node.vertices:
                    vertex_inheritor.vertices.append(Vertex)

        # Give the new Nodes the rest of their Vertices
        vertex_inheritor = new_node_a
        follow_edges(vertex_a, vertex_b, vertex_inheritor, inherit_vertices)

        vertex_inheritor = new_node_b
        follow_edges(vertex_a, vertex_b, vertex_inheritor, inherit_vertices)

    def leaves(self, start_id=0):
        ''' List the ids of all the leaf Nodes in the Treer
            below Node start_id. (Default is the root Node) '''
        # This only shows the id, not the rectangles
        def walk(node):
            if node.child_a is None and node.child_b is None:
                return [node.id]
            else:
                return walk(node.child_a) + walk(node.child_b)

        return set(walk(self.get(start_id)))

    def add_to_draw(self, draw, highlight=None, highlight_color=None, labels=None, color=None, width=None):
        ''' Draw the Tree onto a provided PIL Draw object '''

        highlighted = []

        if highlight:
            for entry in highlight:
                if isinstance(entry, int):
                    highlighted.append(self.get(entry))
                else:
                    highlighted.append(entry)

        self.registry.add_to_draw(draw, highlighted, highlight_color, labels, color, width)

    def show(self, highlight=None, highlight_color=None, labels=None, color=None, width=None):
        ''' Display the Tree '''
        img_size = self.canvas + 1

        img = Image.new("RGBA", img_size.as_tuple(), "green")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw, highlight, highlight_color, labels, color, width)

        img.show()

    def __repr__(self):
        #TODO Use Cody's __repr__ for this

        return f"Leaves: {self.leaves()}"
