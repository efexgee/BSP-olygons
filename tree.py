#!/usr/bin/env python

#TODO camelcase for class names

from PIL import Image, ImageDraw
from random import choice, randint
from drawtree import drawtree

COLORS=("red", "green", "blue", "cyan", "magenta", "yellow") 

class xy():
    ''' a pair of x and y values which represent either a
        coordinate or a lengths in the x and y axes, which
        supports addition and subtraction '''

    #TODO try to implement iterator to be used as a tuple

    def __init__(self, x, y=None):
        #TODO Can I check for "isindexable"?
        # is container? from abstract classes (wwad)
        # hasattr getitem - would allow dicts
        # or catch exception on index
        # *var on call unpacks the doodad (WWAD)
        if isinstance(x, tuple):
            self.x = x[0]
            self.y = x[1]
        elif isinstance(x, int):
            self.x = x

            if y is None:
                self.y = x
            else:
                self.y = y
        else:
            print("Arguments aren't int or tuple: x={} y={}".format(x, y))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        assert isinstance(value, int), "value is not an integer: {}".format(value)
        assert value >= 0, "value is not positive: {}".format(value)
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        assert isinstance(value, int), "value is not an integer: {}".format(value)
        assert value >= 0, "value is not positive: {}".format(value)
        self._y = value

    def __add__(self, value):
        if isinstance(value, xy):
            return xy(self.x + value.x, self.y + value.y)
        elif isinstance(value, int):
            return xy(self.x + value, self.y + value)

    def __sub__(self, value):
        if isinstance(value, xy):
            return xy(self.x - value.x, self.y - value.y)
        elif isinstance(value, int):
            return xy(self.x - value, self.y - value)

    def __mul__(self, value):
        if isinstance(value, xy):
            return xy(self.x * value.x, self.y * value.y)
        elif isinstance(value, int):
            return xy(self.x * value, self.y * value)

    def __floordiv__(self, value):
        if isinstance(value, xy):
            return xy(self.x // value.x, self.y // value.y)
        elif isinstance(value, int):
            return xy(self.x // value, self.y // value)

    def astuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

class rectangle():
    _DEFAULT_COLOR = "white"
    _DEFAULT_BORDER = "magenta"
    _DEFAULT_TEXT = "black"

    def __init__(self, origin, dimensions, label=None, color=None, border=True):
        ''' origin: coodinates of upper left pixel (xy object or tuple)
            dimensions: width and height (xy object or tuple) '''

        #TODO check for blank args
        if isinstance(origin, tuple):
            self.orig = xy(origin[0], origin[1])
        else:
            self.orig = origin

        if isinstance(dimensions, tuple):
            self.dims = xy(dimensions[0], dimensions[1])
        else:
            self.dims = dimensions

        self.label = label

        if color:
            self.color = color
        else:
            self.color = rectangle._DEFAULT_COLOR

        self._border = border
        if border:
            self._border_color = rectangle._DEFAULT_BORDER
        else:
            self._border_color = self.color

    def v_split(self):
        half_size = self.dims // xy(2,1)

        left = rectangle(self.orig, half_size)
        right = rectangle(self.orig + xy(half_size.x, 0), half_size)

        return left, right

    def h_split(self):
        half_size = self.dims // xy(1,2)

        top = rectangle(self.orig, half_size)
        bottom = rectangle(self.orig + xy(0, half_size.y), half_size)

        return top, bottom

    def set_border(self, setting):
        self._border = setting

    def show(self):
        #TODO Does having to add 1 indicate a problem?

        img_size = self.orig + self.dims + 1

        img = Image.new("RGBA", img_size.astuple(), "black")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def add_to_draw(self, draw):
        top_left = self.orig.astuple()
        bottom_right = (self.orig + self.dims).astuple()

        if self._border:
            border = self._border_color
        else:
            border = self.color

        draw.rectangle([top_left, bottom_right], self.color, border)

        if not self.label is None:
            #ImageDraw needs text to be a string
            label = str(self.label)

            label_size = xy(draw.textsize(label))

            label_origin = self.orig + self.dims // 2 - label_size // 2

            draw.text(label_origin.astuple(), label, fill=rectangle._DEFAULT_TEXT)

    def __repr__(self):
        return "rectangle({}, {}, {}, {}, {})".format(self.orig, self.dims, self.label, self.color, self._border)

class node():
    ''' node for a binary tree of rectangles '''

    def __init__(self, id, parent, rectangle, a=None, b=None):
        self.id = id

        self.parent = parent
        self.a = a
        self.b = b

        self.rect = rectangle
        self.rect.label = id

    def __repr__(self):
        if self.parent is None:
            parent = None
        else:
            parent = self.parent.id

        if self.a is None:
            a = None
        else:
            a = self.a.id

        if self.b is None:
            b = None
        else:
            b = self.b.id

        return "{} - p: ({}) a: ({}) b: ({}) rect: {}".format(self.id, parent, a, b, self.rect)

class tree():
    ''' a binary tree of rectangles '''

    def __init__(self, rectangle):
        self.root = node(0, None, rectangle) 
        self.max_id = 0

    def get(self, id):
        def walk(cur, id):
            if cur is None:
                return
            elif cur.id == id:
                return cur

            found = walk(cur.a, id)
            if found:
                return found

            found = walk(cur.b, id)
            if found:
                return found

        return walk(self.root, id)

    def split(self, id, direction):
        cur = self.get(id)

        if cur is None:
            print("Could not find node {}".format(id))
            return

        if not ( cur.a is None and cur.b is None ):
            print("You can only split leaf nodes. This node has children: {}".format(cur))
            return

        if direction.startswith("v"):
            rect_a, rect_b = cur.rect.v_split()
        elif direction.startswith("h"):
            rect_a, rect_b = cur.rect.h_split()
        else:
            print("Something went wrong. Direction has to start with 'v' or 'h' but is {}".format(direction))
            return

        new_a_id = self.max_id + 1
        cur.a = node(new_a_id, cur, rect_a)
        self.max_id += 1
        new_b_id = self.max_id + 1
        cur.b = node(new_b_id, cur, rect_b)
        self.max_id += 1

        return new_a_id, new_b_id

    def leaves(self, start_id=0):
    # This only shows the id, not the rectangles
        def walk(node):
            if node.a is None and node.b is None:
                return [node.id]
            else:
                return walk(node.a) + walk(node.b)

        #return set(walk(self.root))
        return set(walk(self.get(start_id)))


    def show(self):
        img_size = self.root.rect.orig + self.root.rect.dims + 1

        img = Image.new("RGBA", img_size.astuple(), "black")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def add_to_draw(self, draw):
        def draw_all(cur, draw):
        #TODO don't pass draw every time
            if cur is None:
                return
            else:
                cur.rect.add_to_draw(draw)
                draw_all(cur.a, draw)
                draw_all(cur.b, draw)

        draw_all(self.root, draw)

    def __repr__(self):
    # This only shows the id, not the rectangles

    #TODO Why does this spam when I tab-complete in iPython?

        #DEBUG - print a blank like to make output OK in iPython
        print("\n") #for ipython

        #draw_bst only prints to STDOUT so casting to str in order
        # to satisfy the __repr__ requirement causes it to also
        # print None after the tree
        return str(drawtree(self.root))

# TEST CODE #

# laziness
v = "vertical"
h = "horizontal"

# xy objects
zero = xy(0)
ten = xy(10)
fifty = xy(50)
hundred = xy(100)
two_hundred = hundred * 2
five_hundred = hundred * 5
thousand = xy(1000)

# rectangles
box = rectangle(ten, two_hundred, label="a box")
root_box = rectangle(zero, five_hundred)

# something to draw on
paper=Image.new("RGBA", (500, 500), "black")
pic=ImageDraw.Draw(paper)
box.add_to_draw(pic)

# rectangle trees
boxwood = tree(root_box)
boxwood.split(0, v)
boxwood.split(2, v)

# functions
def spring(tree, num_splits, start_id=0):
    split_types = ["vert", "horiz"]
    leaves = tree.leaves(start_id)

    for _ in range(num_splits):
        split_id = leaves.pop()
        split_type = choice(split_types)

        leaves.update(tree.split(split_id, split_type))
