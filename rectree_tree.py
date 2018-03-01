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
        self.registry = self.root.edges.copy()

        # Store the dimensions of the root node since we'll be
        # deleting its Rectangle
        #TODO reference 'rectangle' or 'self.root.rectangle'?
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
                    new_line = Line(last_vertex, vertex)
                    new_edge_a = None
                    new_edge_b = None

                    #TODO Creating an edge may warrant a method?
                    if new_line.issubset(edge_a.line):
                        new_edge_a = Edge(new_line, edge_a.node)
                        edge_a.node.edges.append(new_edge_a)
                        new_edges.append(new_edge_a)
                    if new_line.issubset(edge_b.line):
                        new_edge_b = Edge(new_line, edge_b.node)
                        edge_b.node.edges.append(new_edge_b)
                        new_edges.append(new_edge_b)

                    if new_edge_a and new_edge_b:
                        print("Cross-linking {} and {}".format(new_edge_a, new_edge_b))
                        new_edge_a.link(new_edge_b)

                last_vertex = vertex

            #print("Returning new segment(s): {}".format(new_segments))
            return new_edges


        for line in self.canvas.get_edges():
            if new_edge.line.issubset(line):
                # not storing edges on the border because they can't be shared edges
                #print("Discarding {} because it's on the border".format(new_edge))
                return

        print("\n> Registering Edge {}".format(new_edge))

        safe_adds = []
        iffy_adds = []

        for edge in self.registry:
            # if the registry has a twin for this Edge, link them, and we're done
            if new_edge.twins(edge):
                # going to assume it's not already linked
                print("Twinning {} with {} in registry".format(new_edge, edge))
                self.registry.append(new_edge)
                new_edge.link(edge)
                #print("self.registry={}\n".format(self.registry))
                # going to assume there isn't another twin
                #TODO how much checking for exception cases should I be doing?
                return

            # check for overlapping segments
            if new_edge.overlaps(edge):
                #TODO exploding an overlap changes the registry but we keep checking the loop
                print("{} overlaps with {}".format(new_edge, edge))

                assert edge.twin is None, "Edge should not have a twin: {}".format(edge)

                new_node = new_edge.node
                overlap_node = edge.node

                dovetails = dovetail(new_edge, edge)

                # delete the overlapped line
                # we know that this edge can't have a twin
                self.registry.remove(edge)
                print("Removed edge {} from registry".format(edge))
                #TODO well, this just seems wrong
                edge.node.edges.remove(edge)

                print("Processing dovetails: {}".format(dovetails))
                #TODO I'm running out of generic identifiers (edge, new_edge, etc.)
                for dovetail_edge in dovetails:
                    #print("Processing dovetail {}".format(dovetail_edge))
                    if dovetail_edge.touches(edge.node):
                        #any segment associated with the old node can be added safely
                        # because this segment can't have overlapped a line previously
                        safe_adds.append(dovetail_edge)
                        print("{} is safe to add".format(dovetail_edge))
                    else:
                        #this segment still needs to be added correctly
                        iiffy_adds.append(dovetail_edge)
                        print("{} requires care".format(dovetail_edge))

        # End of the for loop over existing segments
        print("End of loop for {}".format(new_edge))

        # if we had no overlaps, just plain add the new line, and we're done
        if not safe_adds:
            self.registry.append(new_edge)
            print("Added {} to registry".format(new_edge))
            return

        self.registry += safe_adds
        print("Added safe_adds to registry")

        if not iffy_adds:
            #TODO this is likely redundant but helps readability right now
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

        #TODO may be time to learn to implement exception handling
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
        #TODO I once thought that I was glad I made separate splits on the
        # Rectangle object, but I no longer remember why. It doesn't seem to
        # fit with future diagonal split support
        if direction.startswith("v"):
            rect_a, rect_b = cur.rect.v_split()
        elif direction.startswith("h"):
            rect_a, rect_b = cur.rect.h_split()
        else:
            print("Something went wrong. Direction has to start with 'v' or 'h' but is {}".format(direction))
            return

        '''
            Design Considerations
                Would like to allow for diagonal splits
        '''

        #                add Edges to tree's Edge registry

        print("Cleaning up edges of {}".format(cur))

        # Remove Node's Rectangle
        #TODO what is the good way to delete/remove/blank things in objects?
        cur.rect = None
        
        #print("cur.edges={}\n".format(cur.edges))
        #print("self.registry={}\n".format(self.registry))
        # Remove Node from Edges in the Tree's registry
        for edge in cur.edges:
            print("Cleaning up {}".format(edge))
            if edge in self.registry:
                # border edges won't be in the registry
                #TODO is there a "remove if you can"?
                #TODO this is NOT happening... but how to do it correctly?
                if edge.twin:
                    edge.twin.twin = None
                self.registry.remove(edge)
        
        cur.edges = None

        assert cur.edges is None, "Node {} should not have any edges but has {}".format(cur, cur.edges)

        #TODO Make an add_node() method or use Node.__init__()?
        # A method would keep Node agnostic of Tree's ID scheme
        cur.a = self.add_node(cur, rect_a)
        cur.b = self.add_node(cur, rect_b)

        return cur.a, cur.b

    def add_node(self, parent, rectangle):
        self.max_id += 1

        new_node = Node(self.max_id, parent, rectangle)

        # Add the edges to the Tree's registry
        for edge in new_node.edges:
            self.register_edge(edge)

        return new_node

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

        img = Image.new("RGBA", img_size.astuple(), "black")

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        for edge in self.registry:
            # All Edges are pink
            # Color all Edges tracked in the registry in green
            draw.line(edge.line.astuples(), fill="red", width=4)

            if edge.twin is not None:
                # Color all shared Edges blue
                draw.line(edge.line.astuples(), fill="lightgreen", width=2)
                # Connect the centroids of adjacent Rectangles
                print("Drawing line across edge {}".format(edge))
                centroid_a = edge.node.centroid()
                centroid_b = edge.twin.node.centroid()
                draw.line((centroid_a.astuple(), centroid_b.astuple()), fill="black")

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
