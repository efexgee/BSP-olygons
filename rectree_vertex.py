#!/usr/bin/env python

from xy import *

class Vertex(XY):
    def __init__(self, x, y=None):
        #TODO is this right? with the if statement and
        # the single-element tuple?
        self.edges = []

        if y:
            coords = (x, y)
        else:
            coords = (x,)

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
        #TODO * - **** 
        return super().__repr__()

    def __repr__(self):
        #TODO comprehension in __repr__ OK?
        #TODO why is it printing single ticks?
        return f"{super().__repr__()} {[edge._rel_repr(self) for edge in self.edges]}"
