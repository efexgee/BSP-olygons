#!/usr/bin/env python

from rectree_edge import *
from rectree_vertex import *
from rectree_registry import *
from rectree_node import *

img = Image.new("RGBA", (300, 300), "white")
draw = ImageDraw.Draw(img)

reg = EdgeRegistry()
tri_L = Node("L", None, reg)
tri_R = Node("R", None, reg)
tri_O = Node("O", None, reg)
tri_P = Node("P", None, reg)

v_butt = Vertex(50, 250)
v_face = Vertex(200, 150)
v_top = Vertex(100, 50)

e_arrow = Edge(v_butt, v_face, tri_L, tri_R)
e_spear = Edge(v_face, v_top, tri_L, tri_O)
e_poker = Edge(v_butt, v_top, None, tri_L)

reg.extend((e_arrow, e_spear, e_poker))

print(f"e_arrow: {e_arrow}")
print(f"e_spear: {e_spear}")
print(f"e_poker: {e_poker}")
print()

print(f"v_butt: {v_butt}")
print(f"v_face: {v_face}")
print(f"v_top: {v_top}")
print()

print(f"reg:\n{reg}")
print()

v_bottom = Vertex(225, 280)
v_top_right = Vertex(275, 80)

e_four = Edge(v_butt, v_bottom, tri_R, None)
e_five = Edge(v_bottom, v_face, tri_R, tri_P)

e_six = Edge(v_top, v_top_right, None, tri_O)
e_seven = Edge(v_face, v_top_right, tri_O, tri_P)

e_eight = Edge(v_top_right, v_bottom, None, tri_P)

print(f"e_four: {e_four}")
print(f"e_five: {e_five}")
print(f"e_six: {e_six}")
print(f"e_seven: {e_seven}")
print(f"e_eight: {e_eight}")
print()

reg.extend((e_four, e_five, e_six, e_seven, e_eight))

print(f"reg:\n{reg}")

print(f"tri_L: {tri_L}")

reg.add_to_draw(draw)
tri_L.centroid().add_to_draw(draw)

def trace_node(starting_edge, node):

    #TODO Ok, how do I do dynamically chose which method to call?
    #TODO need a relative follow on the edge

    edges = [starting_edge]

    #TODO 'is' appropriate here? where else?

    # Determine which side of the edges we're following
    if node is starting_edge._right_node:
        # Keeping our left hand on the wall
        follow = "right"
    elif node is starting_edge._left_node:
        # Right hand
        follow = "left"
    else:
        raise KeyError(f"{node} is not on {starting_edge}")

    print(f"We are checking {follow} sides for {node}")

    cur_edge = starting_edge
    cur_vertex = starting_edge._tail
    
    # Begin traversal
    while True:
        cur_vertex = cur_edge.get_other_vertex(cur_vertex)
        cur_edge = None

        print(f"We are at vertex {cur_vertex}")

        #DEBUG this counter is for debugging only - should be removed
        found = 0

        for edge in cur_vertex.edges:
            print(f"Looking at {edge._rel_repr(cur_vertex)}")
            if node is edge.get_rel_side(follow, cur_vertex):
                print(f"Found edge with {node} on {follow} side: {edge}")
                cur_edge = edge
                #TODO there would be a break somewhere around here
                found += 1

        assert found <= 1, f"Found more than 1 edge with {node} on the {follow} side on {cur_vertex}: {found}"

        if cur_edge is starting_edge:
            print(f"Going to follow {edge}")
            break

        edges.append(cur_edge)

    return tuple(edges)
