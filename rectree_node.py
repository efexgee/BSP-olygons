#!/usr/bin/env python

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

        #return "{} - p: ({}) a: ({}) b: ({}) rect: {}".format(self.id, parent, a, b, self.rect)
        #DEBUG - for readability
        return "Node {}".format(self.id)
