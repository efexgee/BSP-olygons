#!/usr/bin/env python

from PIL import Image, ImageDraw
from random import choice

from polytree.xy import *
from polytree.node import *
from polytree.tree import *

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

# something to draw on
paper=Image.new("RGBA", (500, 500), "black")
pic=ImageDraw.Draw(paper)

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

        new_nodes = tree.split(split_id, split_type)
        for node in new_nodes:
            leaves.add(node.id)


#boxwood.split(0, v)
#boxwood.split(2, v)
#sprout(boxwood, 20)

#boxwood.show()
