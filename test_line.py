from line import *

assert 3 == 3

# XYs
ten = XY(10)
fifty = XY(50)
hundred = XY(100)

# Lines
la = Line((10,10), (10,50))
lb = Line((10,50), (50,50))
lc = Line((100,100), (10,100))
ld = Line((75,100), (20,100))
le = Line((50,50), (50,75))
lf = Line((80,100), (120,100))

lines = (la, lb, lc, ld, le, lf)

for line in lines:
    print(line)
    len(line)
    line.slope()
    line.astuples()
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

# Edges
