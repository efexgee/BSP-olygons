#!/usr/bin/env python

#TODO how to pep8?

from rectree_node import *
from rectree_edge import *
from rectree_rectangle import *
from line import *
from PIL import Image, ImageDraw

class Tree():
    ''' a binary tree of Rectangles '''

    def __init__(self, rectangle):
        #TODO have __init__ call add_node()?
        self.root = Node(0, None, rectangle)
        # the highest ID currently in the tree
        self.max_id = 0

        # A registry of all Edges in the Tree
        #TODO put root edges in there
        self.registry = EdgeRegistry()
        for line in self.root.rect.get_edges():
            self.registry.append(Edge(line, self.root))

        # Store the dimensions of the root node since we'll be
        # deleting its Rectangle
        #TODO use self.rectangle (which doesn't exist here)
        self.canvas = Rectangle(rectangle.orig, rectangle.dims)

    def get(self, id):
        ''' return the Node with the specified id '''
        #TODO what happens if the node doesn't exist?
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

    def split(self, id, direction=None, location=50):
        ''' Split a Node into two Nodes, in direction, at percentage.
            Default direction is to split across the shorter
            dimension (random for squares), and at 50%. '''
        cur = self.get(id)

        print(f"\n=== Splitting id {id}:{cur} {direction} (probably into Node {self.max_id + 1} and Node {self.max_id + 2})")

        # Check if node exist
        #TODO should this be handled by .get()?
        if cur is None:
            #TODO IndexError?
            raise IndexError(f"Could not find Node {id}")
            return

        # Check if node is a leaf node
        if not ( cur.a is None and cur.b is None ):
            #TODO maybe this implicitly checks whether the Node exists?
            raise ValueError(f"Can't split non-leaf nodes. Node {id} has children: {cur}")

        # Set default direction and check for valid direction
        if direction is None:
            # If no direction is specified, split across the short dimension or
            # split randomly if it's a square
            if cur.rect.dims.x > cur.rect.dims.y:
                direction = "v"
            elif cur.rect.dims.x < cur.rect.dims.y:
                direction = "h"
            else:
                direction = choice(("v", "h"))
        elif not direction.startswith(("v", "h")):
            raise ValueError(f"Direction has to start with 'v' or 'h' but is {direction}")

        # Tell the Node to split
        node_a, node_b = cur.split(direction, location)

        self.add_node(cur, node_a)
        self.add_node(cur, node_b)

    def add_node(self, parent, node):
        ''' Add a Node to the Tree under parent'''
        self.max_id += 1

        if parent.child_a is None:
            parent.child_a = node
        elif parent.child_b is None:
            parent.child_b = node
        else:
            raise RuntimeError(f"Can't add to full Node: {parent}")

        #TODO deal with edges

    def leaves(self, start_id=0):
        ''' List the ids of all the leaf Nodes in the Treer
            below Node start_id. (Default is the root Node) '''
        # This only shows the id, not the rectangles
        def walk(node):
            if node.a is None and node.b is None:
                return [node.id]
            else:
                return walk(node.a) + walk(node.b)

        return set(walk(self.get(start_id)))

    def show(self):
        ''' Display the Tree '''
        img_size = self.canvas.dims + 1

        img = Image.new("RGBA", img_size.as_tuple(), "black")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        for edge in self.registry:
            # All Edges are pink
            # Color all Edges tracked in the registry in green
            draw.line(edge.line.as_tuples(), fill="red", width=4)

            if edge.twin is not None:
                # Color all shared Edges blue
                draw.line(edge.line.as_tuples(), fill="lightgreen", width=2)
                # Connect the centroids of adjacent Rectangles
                #print("Drawing line across edge {}".format(edge))
                centroid_a = edge.node.centroid()
                centroid_b = edge.twin.node.centroid()
                draw.line((centroid_a.as_tuple(), centroid_b.as_tuple()), fill="black")

        img.show()

    def add_to_draw(self, draw):
        ''' Draw the Tree onto a provided PIL Draw object '''
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
        #TODO Use Cody's __repr__ for this
        # This only shows the id, not the rectangles

        #DEBUG - print a blank like to make output OK in iPython
        print("\n") #for ipython

        #draw_bst only prints to STDOUT so casting to str in order
        # to satisfy the __repr__ requirement causes it to also
        # print None after the tree
        #TODO Have to alter drawtree.py
        return str(drawtree(self.root))
