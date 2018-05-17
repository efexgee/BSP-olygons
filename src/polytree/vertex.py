#!/usr/bin/env python

from polytree.xy import Coord
from termcolor import colored

class Vertex(Coord):
    def __init__(self, *args):
        super().__init__(*args)

        self.edges = []

    def disconnect_from(self, edge):
        # This is usually called from within Edge
        try:
            self.edges.remove(edge)
        except:
            raise ValueError(f"{edge} is not connected to {self}")
        
    def add_edge(self, edge):
        self.edges.append(edge)

    def connect_as_tail(self, edge):
        self.add_edge(edge)
        edge.connect_tail(self)

    def connect_as_head(self, edge):
        self.add_edge(edge)
        edge.connect_head(self)

    def coords(self):
        #TODO wtf? this should be a string. I can't do anything with a string
        return super().__repr__()

    def __repr__(self):
        #TODO \n in f-string works just fine
        #return "{}\n{}".format(super().__repr__(), '\n'.join(["\t{}".format(edge._rel_repr(self)) for edge in self.edges]))
        edges = " ".join([e._rel_repr(self) for e in self.edges])
        return f"{colored(super().__repr__(),'yellow')}: {edges}"
