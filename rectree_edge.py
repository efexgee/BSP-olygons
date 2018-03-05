#!/usr/bin/env python

class Edge():
    ''' a Line and two Nodes '''

    def __init__(self, line, node_a, node_b):
        # Asking the user to explicitly specify None in the
        # case of am exterior edge
        self.line = line        # should be immutable
        self.node_a = node_a    # should only be changed via replace()
        self.node_b = node_b    # should only be changed via replace()

    def __eq__(self, edge):
        #TODO does having to implement this mean I did something wrong?
        #No longer used, but question stands
        pass

    def describes(self, node):
        ''' Check whether Edge is part of a Node '''
        #TODO ORs like this seem weird. Is there something like
        # node == foo or bar, or maybe node in [foo, bar] would be
        # good?
        return node == self.node_a or node == self.node_b

    def split(self, point):
        ''' Split Edge at point XY and return two new Edges
            which have the same associated Nodes '''
        #TODO would maybe be cool to change the exceptions raised
        #by Line to say "Can't ... Edge .." instead of Line?
        #TODO am I supposed to use 'try' here and re-raise something?
        line_a, line_b = edge.line.split(point)

        edge_a = Edge(line_a, edge.node_a, edge.node_b)
        edge_b = Edge(line_b, edge.node_a, edge.node_b)

        return edge_a, edge_b

    def has_vertex(self, vertex):
        ''' Check whether Edge has XY as one of its vertices '''
        #TODO so, how do I catch this exception? try/raise?
        return self.line.has_vertex(vertex)

    def replace(self, old_node, new_node):
        ''' Replace a Node associated with an Edge
            This the only way Edges' Nodes should be
            changed '''
        if self.node_a == old_node:
            #TODO feel dumb about if A then A, if B then B
            self.node_a = new_node
        elif self.node_b == new_node:
            self.node_b = new_node
        else:
            #TODO OK to use KeyError here?
            raise KeyError("{} not attached to {}".format(old_node, self))

    def add_to_draw(self, draw, color=None, width=None):
        ''' Add Edge to the specified PIL draw object '''
        #TODO passing None is not the same as using defaults
        #so need to pass nothing in case of None. awkward
        #How do I do that?

        edge.line.add_to_draw(draw)
        #TODO label with the two nodes
        # This is going to be a bit of a to-do

    def show(self):
        ''' Show the line '''
        img_size = self.line.get_canvas_size()

        img = Image.new("RGBA", img_size.astuple(), Line._DEFAULT_BACKGROUND_COLOR)

        draw = ImageDraw.Draw(img)

        self.add_to_draw(draw)

        img.show()

    def __repr__(self):
        if self.twin:
            return "{}: {}, {}".format(self.line, self.node_a, self.node_b)
