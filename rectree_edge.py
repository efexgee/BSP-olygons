#!/usr/bin/env python

class Edge():
    ''' a Line and a Node '''

    def __init__(self, line, node, twin=None):
        self.line = line
        self.node = node
        self.twin = twin

    def twins(self, edge):
        ''' does the Edge have the same Line as another Edge '''
        return self.line == edge.line

    def link(self, edge):
        ''' cross-link two Edges '''
        self.twin = edge
        edge.twin = self

    #def __eq__(self, edge):
        ##TODO does having to implement this mean I did something wrong?
        #return self.line == edge.line and self.node == edge.node

    def __contains__(self, node):
        ''' check whether Edge contains Node '''
        return node == self.node

    def touches(self, node):
        ''' check whether Edge touches Node '''
        if node in self:
            return True
        else:
            # Check if the node is attached to the twin
            if self.twin:
                return node in self.twin
            else:
                return False

    def __repr__(self):
        # Don't print __repr__ of the twin to avoid infinite reflection
        if self.twin:
            return "{}: {} aka {}: {}".format(self.line, self.node, self.twin.line, self.twin.node)
        else:
            return "{}: {}".format(self.line, self.node)
