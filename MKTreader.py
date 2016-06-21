#!/usr/bin/env python

"""MKTreader.py: Read MKT (Cellvizio) raw files."""
__author__ = "Marc Aubreville"
__license__ = "GPL"
__version__ = "0.0.1"

import numpy as np
import struct
from os import stat


class fileinfo:
    offset = 16 # 16 byte header
    gapBetweenImages = 32
    size = 0
    width = 0
    height = 0
    nImages = 0

class MKTreader:
    fileName = ''
    fileHandle = 0
    fi = fileinfo()

    def __init__(self,filename):
       self.fileName = filename;
       self.fileHandle = open(filename, 'rb');

       self.fileHandle.seek(5) # we find the FPS at position 05
       fFPSByte = self.fileHandle.read(4)
       self.fps = struct.unpack('>f', fFPSByte)
       print('FPS: '+str(self.fps))

       self.fileHandle.seek(10) # we find the image size at position 10
       fSizeByte = self.fileHandle.read(4)
       self.fi.size = int.from_bytes(fSizeByte, byteorder='big', signed=True)
       self.fi.nImages=1000
       print("Image size: "+str(self.fi.size)+ " bytes")

       self.fi.width = 576
       if ((self.fi.size/(2*self.fi.width))%2!=0):
            self.fi.width=512
            self.fi.height=int(self.fi.size/(2*self.fi.width))
       else:
            self.fi.height=int(self.fi.size/(2*self.fi.width))

       print("Resolution is " +str(self.fi.width) + " x " + str(self.fi.height))

       filestats = stat(self.fileName)

       self.fi.nImages = int(filestats.st_size / (self.fi.size))
       print("Number of images "+str(self.fi.nImages))

    def readImage(self, position=0):

       self.fileHandle.seek(self.fi.offset + self.fi.size*position + self.fi.gapBetweenImages*position)

       image = np.fromfile(self.fileHandle, dtype=np.int16, count=int(self.fi.size/2))
       image = np.clip(image, 0, 1000)
       image=np.reshape(image, newshape=(self.fi.height, self.fi.width))
       return image


# Example: x = MKTreader('Laesion031-2014.mkt')
