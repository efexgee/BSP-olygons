#!/usr/bin/env python

from rectree_edge import *

#TODO use UserList
class EdgeRegistry(list):
    ''' A list of Edges that can be addressed by their Lines '''

    _DEFAULT_BACKGROUND_COLOR = "white"

    def get_canvas_size(self):
        ''' Return image size required to display all Lines '''

        if not self:
            return XY(0)
        x = set()
        y = set()

        for edge in self:
            x.add(edge.line.start.x)
            x.add(edge.line.end.x)
            y.add(edge.line.start.y)
            y.add(edge.line.end.y)

        return XY(max(x), max(y))

    def get_edge_by_line(self, line):
        ''' Return the Edge which contains a Line '''
        result = None

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

    def get_edges_by_vertex(self, vertex):
        ''' Return all Edges which contain the vertex '''
        edges = []

        for edge in self:
            if edge.line.has_vertex(vertex):
                edges.append(edge)

        if edges:
            return result
        else:
            raise KeyError("Vertex {} is not in {}".format(vertex, self))

    def get_edges_by_node(self, node):
        ''' Return the Edges which contain the Node '''
        edges = []

        for edge in self:
            if edge.describes(node):
                edges.append(edge)

        if edges:
            return result
        else:
            raise KeyError("Node {} is not in {}".format(node, self))

    def get_edge(self, value):
        ''' Return the Edge which contains a Line or vertex '''
        # This is toast but I like the question
        #TODO why is this toast? privatize the dispatchees
        if isinstance(value, line):
            return self.get_edge_by_line(value)
        elif isinstance(value, XY):
            return self.get_edge_by_vertex(value)
        else:
            raise TypeError("Can't find an Edge based on {}: {}".format(type(value), value))

    def add_node_to_draw(self, node, draw):
        ''' Add the polygon for a Node to a PIL draw object '''
        for edge in self:
            if edge.describes(node):
                edge.add_to_draw(draw)

    def show_node(self, node):
        ''' Draw the polygon for a Node '''
        img_size = self.get_canvas_size()

        if img_size == XY(0):
            #TODO this is a debugging error, maybe an assertion then
            raise UserWarning("Not drawing a zero-size image")

        img = Image.new("RGBA", img_size.astuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_node_to_draw(node, draw)

        img.show()

    def __contains__(self, line):
        #TODO in English, please
        ''' Check whether Line is any of the Edges '''
        found = False

        for edge in self:
            if edge.line == line:
                if not found:
                    found = True
                else:
                    raise UserWarning("Found another match for {} in {}: {}".format(line, self, edge))
        return found
