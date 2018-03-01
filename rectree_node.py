#!/usr/bin/env python

class Node():
    ''' node for a binary tree of Rectangles '''

    def __init__(self, id, parent, rectangle, child_a=None, child_b=None):
        self.id = id

        #TODO I don't think we ever use the parent pointer but
        # it doesn't cost much and can be super-useful
        self.parent = parent
        self.a = child_a
        self.b = child_b

        self.rect = rectangle
        self.rect.label = id

    def centroid(self):
        ''' Return the centroid of a Node (floor division)
        Node.centroid -> XY object '''
        #TODO should centroid be on Node or Rectangle?
        #TODO are convenience wrapper methods a thing? i.e.
        # Node.centroid() just calls Node.Rectangle.centroid()?

        return self.rect.orig + self.rect.dims // 2

    def __repr__(self):
        ''' DEBUG: Currently the format is: "Node <id>"

        Format: "<id> - p: (<parent>) a: (<child_a>) b: (<child_b>) rect: <rectangle>"'''

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

        #return "{} - p: ({}) a: ({}) b: ({}) rect: {}".format(self.id, parent, a, b, self.rect)
        #DEBUG - for readability
        return "Node {}".format(self.id)
