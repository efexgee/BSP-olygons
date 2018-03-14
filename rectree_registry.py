#!/usr/bin/env python

from collections import UserList
from rectree_edge import *

class EdgeRegistry(UserList):
    ''' A list of Edges that can be addressed by their LineSegments '''

    _DEFAULT_BACKGROUND_COLOR = "white"

    def get_canvas_size(self):
        ''' Return image size required to display all LineSegments '''

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

    def _get_edge_by_line(self, line):
        ''' [Helper for .get_edge()] Return the Edge which contains a LineSegment '''
        result = None

        for edge in self:
            if edge.line == line:
                if not result:
                    result = edge
                else:
                    raise UserWarning(f"Found another match for {line} in {self}: {edge}")
        if result:
            return result
        else:
            raise KeyError(f"LineSegment {line} is not in {self}")

    def _get_edges_by_vertex(self, vertex):
        ''' [Helper for .get_edges()] Return all Edges which contain the vertex '''
        edges = []

        for edge in self:
            if edge.line.has_vertex(vertex):
                edges.append(edge)

        if edges:
            return result
        else:
            raise KeyError(f"Vertex {vertex} is not in {self}")

    def _get_edges_by_node(self, node):
        ''' [Helper for .get_edges()] Return the Edges which contain the Node '''
        edges = []

        for edge in self:
            if edge.describes(node):
                edges.append(edge)

        if edges:
            return EdgeRegistry(edges)
        else:
            raise KeyError(f"Node {node} is not in {self}")

    def get_edge(self, value):
        ''' Return the Edge which contains a LineSegment or vertex '''
        # This dispatch method allows for additional supported types
        # but I don't know what those would be
        if isinstance(value, line):
            return self._get_edge_by_line(value)
        else:
            raise TypeError(f"Can't retrieve an Edge based on type of {value}: {type(value)}")

    def get_edges(self, value):
        ''' Return a list of Edges which contain a vertex or a Node '''
        if isinstance(value, Node):
            return self._get_edges_by_node(value)
        elif isinstance(value, XY):
            return self._get_edges_by_vertex(value)
        else:
            raise TypeError(f"Can't retrieve Edges based on type of {value}: {type(value)}")

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

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_node_to_draw(node, draw)

        img.show()

    def add_to_draw(self, draw):
        for edge in self:
            print(f"EdgeRegistry: adding {edge} to {draw}")
            edge.add_to_draw(draw)

    def show(self):
        #XXX TEMPORARY HACK XXX
        #TODO image size needs to be calculated
        img_size = XY(300)

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __contains__(self, line):
        ''' Check whether LineSegment is in any of the Edges of the registry '''
        found = False

        for edge in self:
            if edge.line == line:
                if not found:
                    found = True
                else:
                    raise UserWarning(f"Found another match for {line} in {self}: {edge}")
        return found

    def __repr__(self):
        output = ""
        for edge in self:
            #TODO is this how this is done?
            output += f"{str(edge)} \n"

        return output
