#!/usr/bin/env python

from XY import *

class Vertex(XY):
    def __init__(self, x, y=None):
        #TODO is this right? with the if statement and
        # the single-element tuple?
        edges = []

        if y:
            coords = (x, y)
        else:
            coords = (x,)

        super().__init__(*coords)

    def _connect(self, edge):
        ''' Connect to an Edge '''
        #TODO WDYT? *
        self.edges.append(edge)
        
    def couple(self, edge):
        ''' Connect to an Edge and have it connect to Vertex '''
        self._connect(edge)
        edge._connect(self)

    def __repr__(self):
        return f"{super().__repr__()} {self.edges}"
