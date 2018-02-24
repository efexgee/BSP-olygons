#!/usr/bin/env python

from PIL import Image, ImageDraw
from random import choice

from xy import *
from line import *
from rectree_rectangle import *
from rectree_node import *
from rectree_tree import *

# TEST CODE #

# laziness
v = "vertical"
h = "horizontal"

# XY objects
zero = XY(0)
ten = XY(10)
fifty = XY(50)
hundred = XY(100)
two_hundred = hundred * 2
five_hundred = hundred * 5
eight_hundred = hundred * 8
thousand = XY(1000)

# Rectangles
big_box = Rectangle(zero, eight_hundred)
tiny_box = Rectangle(zero, ten)

# something to draw on
paper=Image.new("RGBA", (500, 500), "black")
pic=ImageDraw.Draw(paper)
big_box.add_to_draw(pic)

# Rectangle trees
boxwood = Tree(big_box)
boxwood.split(0, v)
boxwood.split(2, v)

# Lines
la = Line(ten, (10,50))
lb = Line((10,50), fifty)
lc = Line(hundred, (10,100))
ld = Line((75,100), (20,100))
le = Line(fifty, (50,75))
lf = Line((80,100), (120,100))

lines = (la, lb, lc, ld, le, lf)

# functions
def sprout(tree, num_splits, start_id=0, squarish=False):
    split_types = ["vert", "horiz"]
    leaves = tree.leaves(start_id)

    for _ in range(num_splits):
        split_id = leaves.pop()

        if squarish:
            split_type = None
        else:
            split_type = choice(split_types)

        leaves.update(tree.split(split_id, split_type))


sprout(boxwood, 5)

boxwood.show()
