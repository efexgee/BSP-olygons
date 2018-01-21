#!/usr/bin/env python

from PIL import Image, ImageDraw
from random import choice

COLORS=("red", "green", "blue", "cyan", "magenta", "yellow") 

IMG_SIZE=(500,500)
SQUARE_SIZE=200

IMG_COLOR="black"

def centered_text_start(bounds, text):
    ''' Given a string and the coordinates of a rectangle
        calculate where the text should start to be centered
        (NOT IMPLEMENTED) '''
    return

def draw_square(image, top_left, size, color=None, label=None):
    ''' Draw a square on an image. (label is not implemented) '''
    default_color = "white"

    # allow for colors when we debug sub-squares later
    if not color:
        color = default_color

    draw = ImageDraw.Draw(img)

    bottom_right = (top_left[0] + size, top_left[1] + size)

    draw.rectangle([top_left, bottom_right], color, color)

# main
#TODO I should have an import guard
img = Image.new("RGBA", IMG_SIZE, IMG_COLOR)

square_top_left = ((IMG_SIZE[0] - SQUARE_SIZE) / 2, (IMG_SIZE[1] - SQUARE_SIZE) / 2)

draw_square(img, square_top_left, SQUARE_SIZE, color=choice(COLORS))


