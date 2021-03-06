#!/usr/bin/env python

from polytree.edge import Edge
from polytree.line import Line

def most_opposite_edge(edge, edges):
    # The "intuitively opposing" Edge doesn't always
    # make for the most right angle

    #print(f"    Finding opposite of {type(edge)} {edge}")

    # 50% is hard-coded here because we compare midpoints (for now)
    edge_midpoint = edge.locate_point(50)

    #print(f"    Source Edge's midpoint: {edge_midpoint}")

    best_angle = 0
    best_edge = None

    for other_edge in edges:
        other_midpoint = other_edge.locate_point(50)

        #TODO why does Edge not inherit from Line?
        angle = Line(edge._tail, edge._head).angle_between(Line(edge_midpoint, other_midpoint))
        #print(f"     Considering {other_edge} at midpoint {other_midpoint.as_tuple()} makes angle {int(angle)}")

        if abs(90 - angle) < abs(90 - best_angle):
            best_angle = angle
            best_edge = other_edge

    #print(f"     Best edge is {best_edge} with angle {int(best_angle)}")
    return best_edge

def update_edges_from_new_edge(new_edge, old_node):
    start_vertex = new_edge._head
    stop_vertex = new_edge._tail

    relabel_edges(start_vertex, stop_vertex, "right", old_node, new_edge._right_node)
    relabel_edges(start_vertex, stop_vertex, "left", old_node, new_edge._left_node)

def relabel_edges(start_vertex, stop_vertex, side, old_node, new_node):
    ''' Starting at start_vertex, reassign all the Edges which have old_node
    to their (relative) right to new_node, until stop_vertex is reached '''

    # The purpose of this function is to relabel half of all the Edges of
    # a Node which has just been split. E.g. Node A is split into B and C,
    # by new Edge M, with B on its left side and C on its right. Relabel
    # all Edges which have A on their (relative) left side from A to B, starting
    # at the head of M and stopping at M's tail. Then relabel from A to C
    # on (relative) right.

    def relabel_edge(thing):
        if isinstance(thing, Edge):
            thing.replace(old_node, new_node)

    follow_edges(start_vertex, stop_vertex, old_node, relabel_edge, side=side)

def track_next_edge(vertex, side, node):
    ''' Return the Edge on a Vertex which has Node on
    its (relative) side '''

    #print(f"Entering track_next_edge with Vertex {vertex.as_tuple()} Side {side} Node {node.id}")

    assert side in ("left", "right"), f"Side is {side}"

    for edge in vertex.edges:
        #print(f"Looking at {edge._rel_repr(vertex)}")
        if node is edge.rel_side(side, vertex):
            #print(f"Found edge with {node} on {side} side: {edge}")
            return edge

    raise RuntimeError(f"Found no edges with {node} on the {side} side on {vertex}")

def the_raven(nevermore):
    print(f"Quoth the raven: {nevermore}")

def follow_edges(starting_vertex, ending_vertex, node, visitor, side=None):
    # Pick an arbitrary "handedness" if none is specified
    if side is None:
        side = "right"

    cur_vertex = starting_vertex
    visitor(cur_vertex)

    while True:
        cur_edge = track_next_edge(cur_vertex, side, node)

        #print(f"    Considering {cur_edge} and {cur_vertex}")

        #print(f"Calling visitor on {cur_edge}")
        #TODO if True, stop <- support that!
        visitor(cur_edge)

        cur_vertex = cur_edge.other_vertex(cur_vertex)

        visitor(cur_vertex)
        #print(f"Calling visitor on {cur_vertex}")

        if cur_vertex is ending_vertex:
            #print(f"    Reached stop vertex {ending_vertex}")
            break

def split_edge(edge, percentage, registry):
    edge_a, vertex, edge_b = edge.split(percentage)
    #print(f"    Split {edge} into {edge_a} & {edge_b} about {vertex.as_tuple()}")

    edge.disconnect()
    registry.remove(edge)
    registry.extend((edge_a, edge_b))

    return edge_a, vertex, edge_b

#TODO not "place"... 
def place_door_on_edge(registry, edge, percentage, door_width):

    print(f"Placing {door_width}-pixel door in {edge} at {percentage}%")

    #TODO catchy variable names!
    # Calculate door width as a percentage of Edge length
    door_width_as_pct = door_width / edge.length() * 100
    print(f"Door is {door_width_as_pct}% as wide as {edge} (length = {edge.length()})")
    half_door_width_as_pct = door_width_as_pct / 2

    #TODO declutter all the head/tail/a/b stuff (don't call things a/b)
    door_jamb_pct_a = percentage + half_door_width_as_pct
    door_jamb_pct_b = percentage - half_door_width_as_pct

    #TODO implement this
    if door_jamb_pct_a >= 100:
        pass

    if door_jamb_pct_b <= 0:
        pass

    # Find endpoints of the door
    door_jamb_coord_a = edge.locate_point(percentage + half_door_width_as_pct)
    door_jamb_coord_b = edge.locate_point(percentage - half_door_width_as_pct)

    print(f"Door jambs are at {door_jamb_coord_a} and {door_jamb_coord_b}")

    # Insert Vertices
    # The door will be the tail segment of the second split
    # T==========A=============H
    # T==========A-----B=======H

    #TODO confusing. make function?
    tail_to_A, _, A_to_head = edge.insert_vertex(door_jamb_coord_a)
    door, _ , B_to_head = A_to_head.insert_vertex(door_jamb_coord_b)

    #TODO do this whole thing as a .replace(old, [new,new,new])
    registry.remove(edge)

    registry.append(tail_to_A)
    registry.append(door)
    registry.append(B_to_head)

    # Make door transparent
    door.transparent = True

    print(f"Created door {door}")
