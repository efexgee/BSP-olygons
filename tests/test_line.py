#!/usr/bin/env python

from line import *
from random import randint

# XYs
ten = XY(10)
fifty = XY(50)
hundred = XY(100)

# LineSegments
la = LineSegment((10,10), (10,50))
lb = LineSegment((10,50), (50,50))
lc = LineSegment((100,100), (10,100))
ld = LineSegment((75,100), (20,100))
le = LineSegment((50,50), (50,75))
lf = LineSegment((80,100), (120,100))

def mkline(ax, ay, bx, by):
    return LineSegment(XY(ax, ay), XY(bx, by))

def drline(line):
    line_color = "lightgrey"
    line.add_to_draw(draw, line_color)

line_coords = {
    1:(80,50,175,211),
    2:(91,281,161,13),
    3:(49,13,49,101),
    4:(187,281,260,281),
    5:(199,240,199,58),
    6:(281,71,181,71),
    7:(230,130,140,220),
    8:(133,254,59,213)
}

image_size = 300

img = Image.new("RGBA", XY(image_size).as_tuple(), "white")
draw = ImageDraw.Draw(img)

lines = {}
for line in line_coords:
    lines[line] = mkline(*line_coords[line])
    drline(lines[line])

num_dots = 100000

for _ in range(num_dots):
    dot = XY(randint(1,image_size), randint(1,image_size))
    for line in lines.values():
        if dot in line:
            dot_color = "red"
            dot.add_to_draw(draw, dot_color)
        else:
            dot_color = "lightgrey"

img.show()

def probe(point=dot):
    for line_id in lines:
        line = lines[line_id]
        print(f"{point} on line {line_id} {line}: {point in line}")
        print("")


'''
for line in lines:
    print(line)
    len(line)
    line.slope()
    line.as_tuples()
    line.float_len()
    line.xy_slope()
    line.xy_len()

assert len(la) == 40
assert len(lc) == 90
assert len(lf) == 40

assert la.has_vertex(ten)
assert lb.has_vertex(fifty)
assert lc.has_vertex(hundred)

assert lb.shares_vertex(le)

print(lf.split(hundred))
print(le.split(XY(50,66)))
'''
