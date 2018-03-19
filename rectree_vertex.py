#!/usr/bin/env python

from xy import *

class Vertex(XY):
    def __init__(self, x, y=None):
        #TODO args should be *coords
        self.edges = []

        if y:
            coords = (x, y)
        else:
            coords = (x,)

        #TODO super init first to get a blank ancestor
        super().__init__(*coords)

    def _connect(self, edge):
        ''' Connect to an Edge '''
        #TODO WDYT? *
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
        #TODO should not be used?
        self._connect(edge)
        edge._connect_to(self)

    def _repr_coords(self):
        #TODO use a .coords() method?
        #TODO make castable to XY?
        return super().__repr__()

    def __repr__(self):
        # Can't use newlines inside f-strings because '\' are not allowed
        return "{}\n{}".format(super().__repr__(), '\n'.join(["\t{}".format(edge._rel_repr(self)) for edge in self.edges]))
