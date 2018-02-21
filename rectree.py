#!/usr/bin/env python

from PIL import Image, ImageDraw
from random import choice, randint
from drawtree import drawtree

COLORS=("red", "green", "blue", "cyan", "magenta", "yellow")

class XY():
    ''' a pair of x and y values which represent either a
        coordinate or a lengths in the x and y axes, which
        supports addition and subtraction '''

    #TODO try to implement iterator so XY can be used as a tuple

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
        if isinstance(value, XY):
            return XY(self.x + value.x, self.y + value.y)
        elif isinstance(value, int):
            return XY(self.x + value, self.y + value)

    def __sub__(self, value):
        if isinstance(value, XY):
            return XY(self.x - value.x, self.y - value.y)
        elif isinstance(value, int):
            return XY(self.x - value, self.y - value)

    def __mul__(self, value):
        if isinstance(value, XY):
            return XY(self.x * value.x, self.y * value.y)
        elif isinstance(value, int):
            return XY(self.x * value, self.y * value)

    def __floordiv__(self, value):
        if isinstance(value, XY):
            return XY(self.x // value.x, self.y // value.y)
        elif isinstance(value, int):
            return XY(self.x // value, self.y // value)

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        else:
            return False

    def fitsin(self, value):
        #TODO rename 'value' on all these
        #TODO should this be cancontain instead?
        # Both x and y are greater than value's x and y
        # i.e. a rectangle with dimensions 'value' could
        # fit inside a rectangle with our dimensions
        if self.x < value.x and self.y < value.y:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.astuple())

    def __gt__(self, value):
        # compare the non-shares dimension
        # A > B if A and B are on the same vertical or horizontal
        # line and A is further from the origin than B
        if self.x == value.x:
            return self.y > value.y
        elif self.y == value.y:
            return self.x > value.x
        else:
            print("XY objects don't share an axis: {} and {}".format(self, value))

    def __ge__(self, value):
        return self > value or self == value

    def astuple(self):
        return (self.x, self.y)

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

class Rectangle():
    _DEFAULT_COLOR = "white"
    _DEFAULT_BORDER = "magenta"
    _DEFAULT_TEXT = "black"

    def __init__(self, origin, dimensions, label=None, color=None, border=True):
        ''' origin: coodinates of upper left pixel (XY object or tuple)
            dimensions: width and height (XY object or tuple) '''

        #TODO check for blank args
        if isinstance(origin, tuple):
            self.orig = XY(origin[0], origin[1])
        else:
            self.orig = origin

        if isinstance(dimensions, tuple):
            self.dims = XY(dimensions[0], dimensions[1])
        else:
            self.dims = dimensions

        self.label = label

        if color:
            self.color = color
        else:
            self.color = Rectangle._DEFAULT_COLOR

        #TODO Why is this private? just because setter?
        self._border = border
        if border:
            self._border_color = Rectangle._DEFAULT_BORDER
        else:
            self._border_color = self.color

    def v_split(self):
        half_size = self.dims // XY(2,1)

        left = Rectangle(self.orig, half_size, color=self.color, border=self._border)
        right = Rectangle(self.orig + XY(half_size.x, 0), half_size, color=self.color, border=self._border)

        return left, right

    def h_split(self):
        half_size = self.dims // XY(1,2)

        top = Rectangle(self.orig, half_size, color=self.color, border=self._border)
        bottom = Rectangle(self.orig + XY(0, half_size.y), half_size, color=self.color, border=self._border)

        return top, bottom

    def set_border(self, setting):
        self._border = setting

    def get_edges(self):
        #TODO make part of structure and update on the fly?
        upper_right = self.orig + XY(self.dims.x, 0)
        lower_right = self.orig + self.dims
        #TODO making a new XY much better than (0,1) mult shenanigans, right?
        lower_left = self.orig + XY(0, self.dims.y)


        north = Line(self.orig, upper_right)
        east = Line(upper_right, lower_right)
        south = Line(lower_left, lower_right)
        west = Line(self.orig, lower_left)

        return north, east, south, west

    def show(self):
        #TODO Does having to add 1 indicate a problem? are borders frames?

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

            label_size = XY(draw.textsize(label))

            #Only print a label if it fits inside the rectangle
            if label_size.fitsin(self.dims):
                label_origin = self.orig + self.dims // 2 - label_size // 2

                draw.text(label_origin.astuple(), label, fill=Rectangle._DEFAULT_TEXT)

    def __repr__(self):
        return "Rectangle({}, {}, {}, {}, {})".format(self.orig, self.dims, self.label, self.color, self._border)

class Node():
    ''' node for a binary tree of Rectangles '''

    def __init__(self, id, parent, rectangle, a=None, b=None):
        self.id = id

        self.parent = parent
        self.a = a
        self.b = b

        self.rect = rectangle
        self.rect.label = id

    def centroid(self):
        return self.rect.orig + self.rect.dims // 2

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

class Tree():
    ''' a binary tree of Rectangles '''

    def __init__(self, rectangle):
        self.root = Node(0, None, rectangle)
        # the highest ID currently in the tree
        self.max_id = 0

        self.segments = {}
        for line in self.root.rect.get_edges():
            self.segments[line] = [self.root]

        self.canvas = rectangle.dims

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

    def split(self, id, direction=None):
        cur = self.get(id)

        if cur is None:
            print("Could not find Node {}".format(id))
            return

        if not ( cur.a is None and cur.b is None ):
            print("You can only split leaf nodes. This node has children: {}".format(cur))
            return

        if direction is None:
            if cur.rect.dims.x > cur.rect.dims.y:
                direction = "v"
            elif cur.rect.dims.x < cur.rect.dims.y:
                direction = "h"
            else:
                direction = choice(("v", "h"))

        if direction.startswith("v"):
            rect_a, rect_b = cur.rect.v_split()
        elif direction.startswith("h"):
            rect_a, rect_b = cur.rect.h_split()
        else:
            print("Something went wrong. Direction has to start with 'v' or 'h' but is {}".format(direction))
            return

        #TODO should there be an add_node method?
        self.max_id += 1
        new_a_id = self.max_id
        cur.a = Node(new_a_id, cur, rect_a)
        for line in cur.a.rect.get_edges():
            #TODO seems awkward but would "defaults" help?
            if line in self.segments:
                self.segments[line] += [cur.a]
            else:
                self.segments[line] = [cur.a]

        self.max_id += 1
        new_b_id = self.max_id
        cur.b = Node(new_b_id, cur, rect_b)
        for line in cur.b.rect.get_edges():
            #TODO seems awkward but would "defaults" help?
            if line in self.segments:
                self.segments[line] += [cur.b]
            else:
                self.segments[line] = [cur.b]

        for line in cur.rect.get_edges():
            self.segments[line].remove(cur)
            if self.segments[line] == []:
                del self.segments[line]

        #delete the rectangle from the parent node
        #if merging becomes a thing, this might not be smart
        cur.rect = None

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
        img_size = self.canvas + 1

        img = Image.new("RGBA", img_size.astuple(), "black")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        for segment in self.segments:
            assert len(self.segments[segment]) == 1 or len(self.segments[segment]) == 2, "Segment has an impossible number of associated rectangles: {}".format(len(self.segments[segment]))

            if len(self.segments[segment]) == 2:
                draw.line(segment.astuples(), fill="lightgreen", width=3)
                centroid_a = self.segments[segment][0].centroid()
                centroid_b = self.segments[segment][1].centroid()
                draw.line((centroid_a.astuple(), centroid_b.astuple()), fill="black")

        #draw.line([(10,10), (100,100)], fill="black", width=1)

        img.show()

    def add_to_draw(self, draw):
        def draw_all(cur):
            if cur is None:
                return
            if not cur.a and not cur.b:
                #only draw leaf nodes
                cur.rect.add_to_draw(draw)

            draw_all(cur.a)
            draw_all(cur.b)

        draw_all(self.root)

    def __repr__(self):
    # This only shows the id, not the rectangles

        #DEBUG - print a blank like to make output OK in iPython
        print("\n") #for ipython

        #draw_bst only prints to STDOUT so casting to str in order
        # to satisfy the __repr__ requirement causes it to also
        # print None after the tree
        #TODO Have to alter drawtree.py
        return str(drawtree(self.root))

class Line():
    # These assume to be vertical or horizontal lines
    def __init__(self, start, end):
        #TODO validate that these are XY objects
        #TODO validate length of > 1
        #TODO validate it is horizontal or vertical
        #TODO sort at init time
        if isinstance(start, tuple):
            self.start = XY(start)
        elif isinstance(start, XY):
            self.start = start
        else:
            print("What am I supposed to do with this? {} is type {}".format(start, type(start)))

        if isinstance(end, tuple):
            self.end = XY(end)
        elif isinstance(end, XY):
            self.end = end
        else:
            print("What am I supposed to do with this? {} is type {}".format(start, type(start)))

    def __contains__(self, point):
        assert isinstance(point, XY), "Argument must be an XY object: {} is type {}".format(point, type(point))

        if self.orientation() == "vertical" and self.start.x == point.x:
            if min(self.start.y, self.end.y) <= point.y <= max(self.start.y, self.end.y):
                return True
        elif self.orientation() == "horizontal" and self.start.y == point.y:
            if min(self.start.x, self.end.x) <= point.x <= max(self.start.x, self.end.x):
                return True
        else:
            return False

    def orientation(self):
        if self.start.x == self.end.x:
            return "vertical"
        elif self.start.y == self.end.y:
            return "horizontal"
        else:
            print("This line is diagonal: {}".format(self))

    def __eq__(self, line):
        return not {self.start, self.end}.symmetric_difference({line.start, line.end})

    def difference(self, line):
        # in this, but not other
        pass

    def intersection(self, line):
        # in both
        pass

    def isdisjoint(self, line):
        # null intersection
        pass

    def issubset(self, line):
        # other contains this
        pass

    def symmetric_difference(self, line):
        # in this XOR other
        pass

    def union(self, line):
        # in this OR other
        if not self.iscontiguous(line):
            #TODO maybe this would be a good place to catch exceptions
            print("Can't union non-contiguous lines: {} and {}".format(self, line))

        return Line(min(self.start, self.end, line.start, line.end), max(self.start, self.end, line.start, line.end))

    def iscontiguous(self, line):
        #TODO this is not symmetrical!?
        orientation = self.orientation

        if not orientation() == line.orientation():
            print("diff orientations")
            return False

        if not (line.start in self or line.end in self):
            print("arg vertices not on line")
            return False

        return True

    def shares_vertex(self, line):
        #TODO probably won't be used
        # this does not check for "touching" because that would include
        # adjacent vertices
        return bool({self.start, self.end}.intersection({line.start, line.end}))

    def astuples(self):
        return (self.start.astuple(), self.end.astuple())

    def __hash__(self):
        #TODO I don't see how hashing an equivalent data structure is any
        # safer than hashing the __repr__
        return hash(str(self))

    def __repr__(self):
        #return str((self.start, self.end))
        #DEBUG for readability
        return "{}-{}".format(self.start, self.end)

class Segment():
    #TODO I feel like I'm making too many classes

    def __init__(self, line, node):
        self.line = line
        self.node = node

    def __repr__(self):
        #TODO is this string cast the right way to do this?
        return str(self.line)

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
box = Rectangle(zero, eight_hundred)
root_box = Rectangle(zero, eight_hundred)

# something to draw on
paper=Image.new("RGBA", (500, 500), "black")
pic=ImageDraw.Draw(paper)
box.add_to_draw(pic)

# Rectangle trees
boxwood = Tree(root_box)
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

def splice(line_a, line_b):
    # this assertion is redundant with iscontiguous below
    assert line_a.orientation() == line_b.orientation(), "Lines are different orientations: {} and {}".format(line_a, line_b)

    assert line_a.iscontiguous(line_b), "Lines are not contiguous: {} and {}".format(line_a, line_b)

    last_vertex = None
    new_lines = []

    for vertex in sorted([line_a.start, line_a.end, line_b.start, line_b.end]):
        if last_vertex:
            new_lines += [Line(last_vertex, vertex)]
        last_vertex = vertex

    return new_lines
