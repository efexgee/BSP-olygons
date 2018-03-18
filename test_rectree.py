#!/usr/bin/env python

from rectree_edge import *
from rectree_vertex import *
from rectree_registry import *
from rectree_node import *

img = Image.new("RGBA", (300, 300), "white")
draw = ImageDraw.Draw(img)

reg = EdgeRegistry()
triangle_L = Node("L", None, reg)

v_butt = Vertex(50, 250)
v_face = Vertex(200, 150)
v_top = Vertex(100, 50)

e_arrow = Edge(v_butt, v_face, triangle_L, "R")
e_spear = Edge(v_face, v_top, triangle_L, "O")
e_poker = Edge(v_butt, v_top, "P", triangle_L)

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

e_four = Edge(v_butt, v_bottom, "R", "Q")
e_five = Edge(v_bottom, v_face, "S", "R")

e_six = Edge(v_top, v_top_right, "?", "?")
e_seven = Edge(v_face, v_top_right, "?", "?")

e_eight = Edge(v_top_right, v_bottom, "?", "?")

print(f"e_four: {e_four}")
print(f"e_five: {e_five}")
print(f"e_six: {e_six}")
print(f"e_seven: {e_seven}")
print(f"e_eight: {e_eight}")
print()

reg.extend((e_four, e_five, e_six, e_seven, e_eight))

print(f"reg:\n{reg}")

#triangle_L.add_polygon([v_butt, v_face, top], [e_arrow, e_spear, e_poker])

print(f"triangle_L: {triangle_L}")

reg.add_to_draw(draw)
triangle_L.centroid().add_to_draw(draw)
