#!/usr/bin/env python

from rectree_edge import *

class EdgeRegistry(list):
    #def __init__(self, edges=None):
        #TODO why does this work? why is 'edges=' not needed?

    def get_edge_by_line(self, line):
        for edge in self:
            if edge.line == line:
                if not result:
                    result = edge
                else:
                    raise UserWarning("Found another match for {} in {}: {}".format(line, self, edge))
        if result:
            return result
        else:
            raise KeyError("Line {} is not in {}".format(line, self))

    def get_edge_by_vertex(self, vertex):
        for edge in self:
            if edge.line.has_vertex(vertex):
                if not result:
                    result = edge
                else:
                    raise UserWarning("Found another match for {} in {}: {}".format(line, self, edge))
        if result:
            return result
        else:
            raise KeyError("Vertex {} is not in {}".format(line, self))

    def get_edge(self, value):
        #TODO is this OK?
        if isinstance(value, line):
            return self.get_edge_by_line(value)
        elif isinstance(value, XY):
            return self.get_edge_by_vertex(value)
        else:
            raise TypeError("Can't find an Edge based on {}: {}".format(type(value), value))

    def __contains__(self, line):
        found = False

        for edge in self:
            if edge.line == line:
                if not found:
                    found = True
                else:
                    raise UserWarning("Found another match for {} in {}: {}".format(line, self, edge))
        return found
