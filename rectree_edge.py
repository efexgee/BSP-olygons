#!/usr/bin/env python

class Edge():
    ''' a Line and up to 2 Nodes '''
    def __init__(self, line, node, twin=None):
        self.line = line
        self.nodes = node
        self.twin = twin

    def twins(self, edge):
    ''' does the Edge have the same Line as another Edge '''
        return self.line == edge.line

    def link(self, edge):
    ''' cross-link two Edges '''
        self.twin = edge
        edge.twin = self

    def __repr__(self):
        # Don't print __repr__ of the linked Edge to avoid
        # infinite reflection
        return "{}: {} aka {}: {}".format(self.line, self.node, self.twin.line, self.twin.node)
