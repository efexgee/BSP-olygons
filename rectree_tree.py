#!/usr/bin/env python

from rectree_node import *
from line import *

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

    def add_segment(self, line, node):
        print("Been asked to add line {}".format(line))

        def smush(line_a, node_a, line_b):
            print("Smushing {} and {}".format(line_a, line_b))
            # We can assume that there is only a single rectangle
            # associated with this line
            assert len(self.segments[line_b]) == 1, "Line {} doesn't have exactly 1 associated rectangle: {} values={}".format(line_b, len(self.segments[line_b]), self.segments[line_b])

            node_b = self.segments[line_b][0]
            last_vertex = None
            new_segments = set()

            # remove duplicates so we don't get 0-length lines
            for vertex in sorted(set([line_a.start, line_a.end, line_b.start, line_b.end])):
                if last_vertex:
                    new_line = Line(last_vertex, vertex)
                    #print("Generated new line: {}".format(new_line))
                    if new_line.issubset(line_a):
                        #print("New segment: line {} node {}".format(new_line, node_a))
                        new_segments.add((new_line, node_a))
                    if new_line.issubset(line_b):
                        #print("New segment: line {} node {}".format(new_line, node_b))
                        new_segments.add((new_line, node_b))
                last_vertex = vertex

            #TODO new_segments needs to be de-duped!

            #del self.segments[line_b]

            #print("Returning new segment(s): {}".format(new_segments))
            return new_segments

        if line in self.segments:
            self.segments[line] += [node]
            print("Added node {} to segment {}".format(node, line))
            return

        #print("Dealing with complicated addition of {}".format(line))

        overlapping_segments = []
        
        # check for overlapping segments
        #TODO should this sort of thing be a comprehension?
        for entry in self.segments:
            #print("Checking entry {} for contiguity".format(entry))
            if line.overlaps(entry):
                print("Found overlapping segment {}".format(entry))
                overlapping_segments += [entry]

        if overlapping_segments:
            while overlapping_segments:
                new_segments = smush(line, node, overlapping_segments.pop())
                print("Inserting new segments: {}".format(new_segments))
                for line, node in new_segments:
                    if line in self.segments:
                        print("Added node {} to segment {}".format(node, line))
                        self.segments[line] += [node]
                    else:
                        print("Created segment {} with node {}".format(line, node))
                        self.segments[line] = [node]
            return

        self.segments[line] = [node]
        print("Added segment {} with {}".format(line, node))
        return
    
    def split(self, id, direction=None):
        cur = self.get(id)

        print("=== Splitting {}".format(cur))

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

        # remove the split node's segments from the Tree
        print("Cleaning up edges of {}".format(cur))
        for line in cur.rect.get_edges():
            #print("Removing {} from {}".format(cur, self.segments[line]))
            self.segments[line].remove(cur)
            if self.segments[line] == []:
                #print("Deleting empty segment {}".format(line))
                del self.segments[line]

        #TODO should there be an add_node method?
        self.max_id += 1
        new_a_id = self.max_id
        cur.a = Node(new_a_id, cur, rect_a)
        for line in cur.a.rect.get_edges():
            self.add_segment(line, cur.a)

        self.max_id += 1
        new_b_id = self.max_id
        cur.b = Node(new_b_id, cur, rect_b)
        for line in cur.b.rect.get_edges():
            self.add_segment(line, cur.b)

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
