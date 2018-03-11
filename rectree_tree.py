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
        self.root = Node(0, None, rectangle)
        # the highest ID currently in the tree
        self.max_id = 0

        # A registry of all Edges in the Tree
        self.registry = []
        for line in self.root.rect.get_edges():
            self.registry.append(Edge(line, self.root))

        # Store the dimensions of the root node since we'll be
        # deleting its Rectangle
        #TODO use self.rectagle (which doesn't exist here)
        self.canvas = Rectangle(rectangle.orig, rectangle.dims)

    def get(self, id):
        ''' return the Node with the specified id '''
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

    def register_edge(self, new_edge):
        ''' add a new line to the registry, making the appropriate changes '''
        def dovetail(edge_a, edge_b):
            print("\n>> Dovetailing edges {} and {}".format(edge_a, edge_b))

            last_vertex = None
            new_edges = []

            # remove duplicates so we don't get 0-length lines
            for vertex in sorted(set([edge_a.line.start, edge_a.line.end, edge_b.line.start, edge_b.line.end])):
                # if this is our second vertex, we can start making lines
                if last_vertex:
                    new_line = LineSegment(last_vertex, vertex)
                    new_edge_a = None
                    new_edge_b = None

                    if new_line.issubset(edge_a.line):
                        new_edge_a = Edge(new_line, edge_a.node)
                        new_edges.append(new_edge_a)
                    if new_line.issubset(edge_b.line):
                        new_edge_b = Edge(new_line, edge_b.node)
                        new_edges.append(new_edge_b)

                    if new_edge_a and new_edge_b:
                        print("Cross-linking {} and {}".format(new_edge_a, new_edge_b))
                        new_edge_a.link(new_edge_b)

                last_vertex = vertex

            return new_edges


        for line in self.canvas.get_edges():
            if new_edge.line.issubset(line):
                # not storing edges on the border because they can't be shared edges
                return

        print("\n> Registering Edge {}".format(new_edge))

        if new_edge in self.registry:
            print("{} already exists in registry".format(new_edge))
            return

        safe_adds = []
        iffy_adds = []
        removals = []

        for edge in self.registry:
            # if the registry has a twin for this Edge, link them, and we're done
            if new_edge.twins(edge):
                # going to assume it's not already linked
                print("Twinning {} with {} in registry".format(new_edge, edge))
                self.registry.append(new_edge)
                new_edge.link(edge)
                # going to assume there isn't another twin
                return

            # check for overlapping segments
            if new_edge.overlaps(edge):
                print("{} overlaps with {}".format(new_edge, edge))

                assert edge.twin is None, "Edge should not have a twin: {}".format(edge)

                new_node = new_edge.node
                overlap_node = edge.node

                dovetails = dovetail(new_edge, edge)

                # delete the overlapped line
                # we know that this edge can't have a twin
                #self.registry.remove(edge)
                removals.append(edge)
                print("Marked {} for removal from registry".format(edge))

                print("Processing dovetails")
                for dovetail_edge in dovetails:
                    #print("Processing dovetail {}".format(dovetail_edge))
                    if dovetail_edge.touches(edge.node):
                        #any segment associated with the old node can be added safely
                        # because this segment can't have overlapped a line previously
                        safe_adds.append(dovetail_edge)
                        print("{} is safe to add".format(dovetail_edge))
                    else:
                        #this segment still needs to be added correctly
                        iffy_adds.append(dovetail_edge)
                        print("{} requires care".format(dovetail_edge))

        # End of the for loop over existing segments
        print("End of loop for {}".format(new_edge))

        for deado in removals:
            self.registry.remove(deado)
            print("Removed edge {} from registry".format(deado))

        # if we had no overlaps, just plain add the new line, and we're done
        if not safe_adds:
            self.registry.append(new_edge)
            print("Added {} to registry".format(new_edge))
            return

        self.registry += safe_adds
        print("Added safe_adds to registry")

        print("iffy_adds={}".format(iffy_adds))

        if not iffy_adds:
            print("No iffy_adds. We're done.")
            return

        for iffy_add in iffy_adds:
            print("\n>>> Calling myself on {}".format(iffy_add))
            self.register_edge(iffy_add)

        '''
verlaps with {}".format(new_edge, edge))

        At this point:
            - we weren't trying to add a border edge
            - we did not find a twin
            - we did a plain add if we had no overlaps
            - we have exploded all the overlaps
            - any overlapped edges have been deleted
            - safe_adds have been added to replace the overlapped edges
            - new_edge no longer matters
            - iffy_adds need to be handle appropriately
                + iffy_adds contains 0 - 2 edges (I think)
        '''

    
    def split(self, id, direction=None):
        cur = self.get(id)

        print("\n=== Splitting id {}:{} {} (probably into Node {} and Node {})".format(id, cur, direction, self.max_id + 1, self.max_id + 2))

        # Check if node exist
        if cur is None:
            print("Could not find Node {}".format(id))
            return

        # Check if node is a leaf node
        if not ( cur.a is None and cur.b is None ):
            print("You can only split leaf nodes. This node has children: {}".format(cur))
            return

        # If no direction is specified, split across the short dimension or
        # split randomly if it's a square
        if direction is None:
            if cur.rect.dims.x > cur.rect.dims.y:
                direction = "v"
            elif cur.rect.dims.x < cur.rect.dims.y:
                direction = "h"
            else:
                direction = choice(("v", "h"))

        # Split the Rectangle in the matching direction
        if direction.startswith("v"):
            rect_a, rect_b = cur.rect.v_split()
        elif direction.startswith("h"):
            rect_a, rect_b = cur.rect.h_split()
        else:
            print("Something went wrong. Direction has to start with 'v' or 'h' but is {}".format(direction))
            return

        #                add Edges to tree's Edge registry


        # Remove Node's Rectangle
        cur.rect = None

        print("Cleaning up edges of {}".format(cur))

        # Remove Node from Edges in the Tree's registry
        self.reg_del(cur)
        
        # A method would keep Node agnostic of Tree's ID scheme
        cur.a = self.add_node(cur, rect_a)
        cur.b = self.add_node(cur, rect_b)

        return cur.a, cur.b

    def add_node(self, parent, rectangle):
        self.max_id += 1

        new_node = Node(self.max_id, parent, rectangle)

        # Add the edges to the Tree's registry
        for line in new_node.rect.get_edges():
            self.register_edge(Edge(line, new_node))

        return new_node

    def reg_del(self, node):
        nodes_edges = []

        for edge in self.registry:
            if node in edge:
                if edge.twin:
                    edge.twin.twin = None
                nodes_edges.append(edge)

        for edge in nodes_edges:
            self.registry.remove(edge)

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
