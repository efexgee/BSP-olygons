#!/usr/bin/env python

#from polytree.registry import EdgeRegistry
#from polytree.node import Node
#from polytree.vertex import Vertex
#from polytree.xy import XY
#from polytree.edge import Edge
#from PIL import Image, ImageDraw
#from random import sample

#TODO catchy name!
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
    #print(f"Entering track_next_edge with Vertex {vertex.as_tuple()} Side {side} Node {node.id}")

    assert side in ("left", "right"), f"Side is {side}"

    #DEBUG this counter is for debugging only - should be removed
    found = 0

    next_edge = None

    for edge in vertex.edges:
        #print(f"Looking at {edge._rel_repr(vertex)}")
        if edge.borders_node(node):
            #print(f"Found edge with {node}: {edge}")
            #print(f"Edge has vertices: {id(edge._tail)} and {id(edge._head)}")
            if node is edge.rel_side(side, vertex):
                #print(f"Found edge with {node} on {side} side: {edge}")
                next_edge = edge
                #DEBUG only
                #RELEASE there would be a break somewhere around here
                found += 1

    assert found <= 1, f"Found more than 1 edge with {node} on the {side} side on {vertex}: {found} found"
    assert next_edge, f"Found no edges with {node} on the {side} side on {vertex}"

    return next_edge

def visit_polygon(starting_vertex, node, visitor):
    # Establish an Edge side to follow (doesn't matter which one)
    #print(f"Entering visit_polygon with Vertex {starting_vertex.as_tuple()} Node {node.id} and a visitor")
    for edge in starting_vertex.edges:
        if edge.borders_node(node):
            handedness = edge.side_of_node(node)
            break

    cur_vertex = starting_vertex

    while True:
        cur_edge = track_next_edge(cur_vertex, handedness, node)

        #HELP visitor needs to be able to tell us to break, etc.
        #print(f"Calling visitor on {cur_edge}")
        visitor(cur_edge)

        cur_vertex = cur_edge.other_vertex(cur_vertex)

        visitor(cur_vertex)
        #print(f"Calling visitor on {cur_vertex}")

        if cur_vertex is starting_vertex:
            # We've circumscribed the polygon
            break

def split_edge(edge, percentage, registry):
    edge_a, vertex, edge_b = edge.split(percentage)
    print(f"    Split {edge} into {edge_a} & {edge_b} about {vertex.as_tuple()}")

    edge.disconnect()
    registry.remove(edge)
    registry.extend((edge_a, edge_b))

    return edge_a, vertex, edge_b
