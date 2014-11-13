import colorsys
from random import random
from opc.colors import *
from opc.matrix import OPCMatrix
from opc.hue import getHueGen
from math import sin, cos, pi, fabs
from utils.frange import frange

DELTA_Z = 0.05
MatrixPixels =[]

# Normalization method, so the colors are in the range [0, 1]
def normalize (color):
    return color[0] / 255.0, color[1] / 255.0, color[2] / 255.0
            
# Reformats a color tuple, that uses the range [0, 1] to a 0xFF representation.
def reformat (color):
    return int (round (color[0] * 255)), int (round (color[1] * 255)), int (round (color[2] * 255))

class Art:

    description = "Lissajous figures"

    def __init__(self, matrix):
        self.phase_z = 0

    def start(self, matrix, pixels):
        global MatrixPixels
        MatrixPixels = pixels
        matrix.clear()

    def refresh(self, matrix):
        #(self, dh=1.0, ds=1.0, dv=1.0):  Shift any of hue, saturation, and value on the matrix, specifying the attributes that you'd like to adjust
        matrix.shift(.9, 1, .9)
        #change DELTA_Z phase adding 0.05
        self.phase_z += DELTA_Z

        #find the center
        xcenter = matrix.width/2.0
        ycenter = matrix.height/2.0
        #value in a sin [-1,1]
        theta = sin(self.phase_z)
        if theta < 0:
            theta_x, theta_y = 1, 1 - 2*theta
        else:
            theta_x, theta_y = 1 + 2*theta, 1

        for angle in frange(0, 20*pi, 0.01):
            x = xcenter + xcenter * sin(theta_x * angle)
            y = ycenter + ycenter * cos(theta_y * angle)
            #find next color
            color = MatrixPixels[int(x)-1][int(y)-1]
            color_hsv = colorsys.rgb_to_hsv(*normalize(color))
            color_sat=random()
            color_value=random()
            color_hsv= (color_hsv[0], color_sat, color_value)
            color_next= reformat (colorsys.hsv_to_rgb (*color_hsv))
            matrix.drawPixel(x, y, color_next)
        
    def interval(self):
        return 2500

