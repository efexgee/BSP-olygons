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

        #TODO reference the rect via self.rect or rectangle?
        self.edges = [self.rect.get_edges()]

    def centroid(self):
        ''' Return the centroid of a Node (floor division)
        Node.centroid -> XY object '''

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
