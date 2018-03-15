#!/usr/bin/env python

from rectree_edge import *
from rectree_vertex import *
from rectree_registry import *

butt = Vertex(50, 250)
face = Vertex(200, 150)
top = Vertex(100, 50)

arrow = Edge(butt, face, "L", "R")
spear = Edge(face, top, "L", "O")
poker = Edge(butt, top, "P", "L")

print(f"arrow: {arrow}")
print(f"spear: {spear}")
print(f"poker: {poker}")
print()

print(f"butt: {butt}")
print(f"face: {face}")
print(f"top: {top}")
print()

reg = EdgeRegistry((arrow, spear, poker))

print(f"reg:\n{reg}")
print()

bottom = Vertex(225, 280)
top_right = Vertex(275, 80)

four = Edge(butt, bottom, "R", "Q")
five = Edge(bottom, face, "S", "R")

six = Edge(top, top_right, "?", "?")
seven = Edge(face, top_right, "?", "?")

eight = Edge(top_right, bottom, "?", "?")

print(f"four: {four}")
print(f"five: {five}")
print(f"six: {six}")
print(f"seven: {seven}")
print(f"eight: {eight}")
print()

reg.extend((four, five, six, seven, eight))

print(f"reg:\n{reg}")
