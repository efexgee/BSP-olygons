#!/usr/bin/env python

''' Take this library: https://pillow.readthedocs.io/en/5.0.0/

Produce a 500x500px image containing a centered 200x200px white
square on a black background as a png file.'''

from PIL import Image, ImageDraw
from numpy import array, ndarray # make Alec-compatible

IMG_SIZE=(500,500)
SQUARE_SIZE=(200,200)

IMG_COLOR="black"
SQUARE_COLOR="white"

def halve(dimension):
    ''' Halves either integers (i.e. sizes) or numpy arrays (i.e. coordinates) '''
    ''' I may want to change the definition of "half" '''
    
    assert isinstance(dimension, (int, ndarray)), "Not an int or numpy array: {}".format(dimension)
    return dimension // 2

# main
#TODO I should have an import guard
img = Image.new("RGBA", IMG_SIZE, IMG_COLOR)
img_drw = ImageDraw.Draw(img)

# I'm doing coordinate math as numpy arrays
# It would be cool to extend the Image and ImageDraw classes
# to support ndarrays. But would it be dumb?
img_dims= array((img.width, img.height))
square_dims= array(SQUARE_SIZE)

squ_start_coords = halve(img_dims) - halve(square_dims)
squ_end_coords = squ_start_coords + square_dims

img_drw.rectangle([tuple(squ_start_coords), tuple(squ_end_coords)], SQUARE_COLOR, SQUARE_COLOR)

img.save("square.png")
