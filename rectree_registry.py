#!/usr/bin/env python

from collections import UserList
from rectree_edge import *

class EdgeRegistry(UserList):
    ''' A list of Edges that can be addressed by their LineSegments '''

    _DEFAULT_BACKGROUND_COLOR = "white"
    _DEFAULT_LINE_HIGHLIGHT_COLOR = "pink"
    _CANVAS_PADDING = 10

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
        #TODO this is too promiscuous? -- WTF?
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

    def add_node_to_draw(self, node, draw, color=None, width=None):
        ''' Add the polygon for a Node to a PIL draw object '''
        args = {}
        
        if color:
            args["color"] = color
        if width:
            args["width"] = width

        self._get_edges_by_node(node).add_to_draw(draw, **args)

    def show_node(self, node, color=None, width=None):
        ''' Draw the polygon for a Node '''
        args = {}
        
        if color:
            args["color"] = color
        if width:
            args["width"] = width

        img_size = self.get_canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        self.add_node_to_draw(node, draw, **args)

        img.show()

    def show_highlighted(self, targets, highlight=_DEFAULT_LINE_HIGHLIGHT_COLOR, color=None, width=None):
        ''' Show all the Edges but highlight specific Edges or those
            bounding a Node '''
        args = {}

        if color:
            args["color"] = color
        if width:
            args["width"] = width

        img_size = self.get_canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw all the Edges
        self.add_to_draw(draw, **args)

        # Overlay the highlighted elements
        #TODO this HAS to be like **** at least!
        if not isinstance(targets, list):
            targets = [targets]

        for target in targets:
            print(type(target))
            #TODO why does this type check not work?!
            if isinstance(target, Edge):
                print("got here")
                target.add_to_draw(draw, color=highlight)
            #XXX temp hack to reference nodes by ID
            elif isinstance(target, str):
                self.add_node_to_draw(target, draw, color=highlight)
            else:
                raise TypeError(f"Can't highlight Edges by {type(target)}: {target}")

        img.show()

    def add_to_draw(self, draw, color=None, width=None):
        ''' Add all Edges to a PIL Draw object '''
        args = {}

        if color:
            args["color"] = color
        if width:
            args["width"] = width

        for edge in self:
            #print(f"EdgeRegistry: adding {edge} to {draw}")
            edge.add_to_draw(draw, **args)

    def show(self, color=None, width=None):
        ''' Display all the Edges '''
        args = {}

        if color:
            args["color"] = color
        if width:
            args["width"] = width

        img_size = self.get_canvas_size()

        img = Image.new("RGBA", img_size.as_tuple(), EdgeRegistry._DEFAULT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw, **args)

        img.show()

    def get_canvas_size(self):
        ''' Return the size an Image has to be to fit all the Edges '''
        #TODO Maintain on the fly?
        max_x = 0
        max_y = 0

        # This is a very inefficient traversal
        #TODO using max here seems fine, but maybe build a set?
        for edge in self:
            max_x = max(max_x, edge._tail._x, edge._head._x)
            max_y = max(max_y, edge._tail._y, edge._head._y)

        assert max_x * max_y > 0, f"Canvas size can't have a zero in it: ({max_x}, {max_y})"
            
        return XY(max_x, max_y) + EdgeRegistry._CANVAS_PADDING

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
            #TODO list comprehension with a join
            output += f"{str(edge)} \n"

        return output
