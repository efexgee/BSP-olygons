#!/usr/bin/env python

from polytree.xy import *

class Vertex(XYCoord):
    def __init__(self, *args):
        super().__init__(*args)

        self.edges = []

    def _connect(self, edge):
        ''' Connect to an Edge '''
        self.edges.append(edge)

    def disconnect(self, edge):
        try:
            self.edges.remove(edge)
        except:
            raise ValueError(f"{edge} is not connected to {self}")
        
    def connect_outbound(self, edge):
        ''' Connect to an Edge and have it connect to Vertex '''
        self._connect(edge)
        edge._connect_from(self)

    def connect_inbound(self, edge):
        self._connect(edge)
        edge._connect_to(self)

    def _repr_coords(self):
        #TODO use a .coords() method?
        #TODO make castable to XY?
        return super().__repr__()

    def __repr__(self):
        #TODO \n in f-string works just fine
        return "{}\n{}".format(super().__repr__(), '\n'.join(["\t{}".format(edge._rel_repr(self)) for edge in self.edges]))
