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

# registry for split testing
splitsies = EdgeRegistry()

node_m = Node("M", None, splitsies)
node_n = Node("N", None, splitsies)
node_o = Node("O", None, splitsies)

v_a = Vertex(50,50)
v_b = Vertex(150,75)
v_c = Vertex(250,200)
v_d = Vertex(100,150)

#TODO make everything consistent in checking left first
e_ab = Edge(v_a, v_b, None, node_m)
e_bc = Edge(v_b, v_c, None, node_m)
e_cd = Edge(v_c, v_d, None, node_m)
e_da = Edge(v_d, v_a, None, node_m)

splitsies.extend((e_ab, e_bc, e_cd, e_da))

e_db = Edge(v_d, v_b, node_o, node_n)
splitsies.extend((e_db,))

def update_edges_from_new_edge(new_edge, old_node):

    start_vertex = new_edge._head
    stop_vertex = new_edge._tail

    #TODO comma-separated or make tuple?
    #for side in "right", "left": 

    relabel_edges(start_vertex, stop_vertex, "right", old_node, new_edge._right_node)
    relabel_edges(start_vertex, stop_vertex, "left", old_node, new_edge._left_node)

def relabel_edges(start_vertex, stop_vertex, side, old_node, new_node):

    cur_vertex = start_vertex

    while True:
        cur_edge = track_next_edge(cur_vertex, side, old_node)

        cur_edge.replace(old_node, new_node)

        cur_vertex = cur_edge.get_other_vertex(cur_vertex)

        if cur_vertex is stop_vertex:
            break

def track_next_edge(vertex, side, node):
    #DEBUG this counter is for debugging only - should be removed
    found = 0

    next_edge = None

    for edge in vertex.edges:
        print(f"Looking at {edge._rel_repr(vertex)}")
        if node is edge.get_rel_side(side, vertex):
            print(f"Found edge with {node} on {side} side: {edge}")
            next_edge = edge
            #DEBUG only
            #TODO there would be a break somewhere around here
            found += 1

    assert found <= 1, f"Found more than 1 edge with {node} on the {side} side on {vertex}: {found} found"
    assert next_edge, f"Found no edges with {node} on the {side} side on {vertex}"

    return next_edge
