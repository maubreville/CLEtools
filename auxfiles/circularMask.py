"""circularMask.py: Create a circular mask within a rectangular image"""
__author__ = "Marc Aubreville"
__license__ = "GPL"
__version__ = "0.0.1"

#import math
import numpy as np

class circularMask:
    mask = 0
    def __init__(self,w,h,r):
        self.x,self.y = np.ogrid[-int(h/2):int(h/2), -int(w/2):int(w/2)]
        self.mask = self.x*self.x + self.y*self.y <= int(r/2)*int(r/2)

# Example: cm=circularMask(576,578,576)
