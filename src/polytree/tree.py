#!/usr/bin/env python

#TODO how to pep8?

from polytree.registry import EdgeRegistry
from polytree.node import Node
from polytree.vertex import Vertex
from polytree.xy import XY
from polytree.edge import Edge
from PIL import Image, ImageDraw
from random import sample

### functions without a home ###

def update_edges_from_new_edge(new_edge, old_node):

    start_vertex = new_edge._head
    stop_vertex = new_edge._tail

    relabel_edges(start_vertex, stop_vertex, "right", old_node, new_edge._right_node)
    relabel_edges(start_vertex, stop_vertex, "left", old_node, new_edge._left_node)

def relabel_edges(start_vertex, stop_vertex, side, old_node, new_node):

    cur_vertex = start_vertex

    while True:
        cur_edge = track_next_edge(cur_vertex, side, old_node)

        cur_edge.replace(old_node, new_node)

        cur_vertex = cur_edge.other_vertex(cur_vertex)

        if cur_vertex is stop_vertex:
            break

def track_next_edge(vertex, side, node):
    #DEBUG this counter is for debugging only - should be removed
    found = 0

    next_edge = None

    for edge in vertex.edges:
        #print(f"Looking at {edge._rel_repr(vertex)}")
        if node is edge.rel_side(side, vertex):
            ##print(f"Found edge with {node} on {side} side: {edge}")
            next_edge = edge
            #DEBUG only
            #RELEASE there would be a break somewhere around here
            found += 1

    assert found <= 1, f"Found more than 1 edge with {node} on the {side} side on {vertex}: {found} found"
    assert next_edge, f"Found no edges with {node} on the {side} side on {vertex}"

    return next_edge

def split_edge(edge, percentage, registry):
    edge_a, vertex, edge_b = edge.split(percentage)
    print(f"    Split {edge} into {edge_a} & {edge_b} about {vertex.as_tuple()}")

    edge.disconnect()
    registry.remove(edge)
    registry.extend((edge_a, edge_b))

    return edge_a, vertex, edge_b

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
        cur = self.get(id)

        print(f"\n=== Splitting Node {id} {direction}-wise (probably into Node {self.max_id + 1} & Node {self.max_id + 2})")

        # Check if node exist
        #TODO should this be handled by .get()?
        if cur is None:
            #TIDY IndexError?
            raise IndexError(f"Could not find Node {id}")
            return

        # Check if node is a leaf node
        if not ( cur.child_a is None and cur.child_b is None ):
            #TODO maybe this implicitly checks whether the Node exists?
            raise ValueError(f"Can't split non-leaf nodes. Node {id} has children: {cur}")

        # Set default direction and check for valid direction
        if direction is None:
            # If no direction is specified, split across the short dimension or
            #TODO need to implement
            direction = "very not implemented!"
            # split randomly if it's a square

        if not direction.startswith(("v", "h")):
            raise ValueError(f"Direction has to start with 'v' or 'h' but is {direction}")

        #TODO this was a check splitting across the narrow dimension
        even = True
        if even:
            edge_a = cur.get_rnd_edge()
            edge_b = cur.get_opp_edge(edge_a)
        else:
            #TODO HELP I think responsibilities are split funny now
            edge_a, edge_b = sample(self.registry.get_edges(cur), 2)

        print(f"  Splitting on Edges {edge_a} & {edge_b}")

        _, vertex_a, _ = split_edge(edge_a, location, self.registry)
        _, vertex_b, _ = split_edge(edge_b, location, self.registry)

        print(f"  Created two new vertices: {vertex_a.as_tuple()} & {vertex_b.as_tuple()}")

        #TODO Find which of the ancestor Node's Vertices each Node inherits


        self.max_id += 1
        new_node_a = Node(self.max_id, cur, self.registry)
        self.max_id += 1
        new_node_b = Node(self.max_id, cur, self.registry)
        print(f"  Created two new nodes: {new_node_a} & {new_node_b}")

        cur.child_a = new_node_a
        cur.child_b = new_node_b
        print(f"  Updated child pointers on {cur}")

        new_edge = Edge(vertex_a, vertex_b, new_node_a, new_node_b)
        print(f"  Created a new edge: {new_edge}")

        self.registry.append(new_edge)

        update_edges_from_new_edge(new_edge, cur)

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
