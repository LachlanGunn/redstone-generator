#!/usr/bin/env python

import nbt
from nbt.nbt import *

import numpy
import blocks
import gzip

class Schematic(object):
    def __init__(self, filename = None):
        if filename != None:
            nbtfile = NBTFile(filename, 'rb')
            blocks_arr = [ord(x) for x in nbtfile['Blocks'].value]
            data_arr   = [ord(x) for x in nbtfile['Data'].value]
            
            self.width  = nbtfile['Width' ].value
            self.length = nbtfile['Length'].value
            self.height = nbtfile['Height'].value

            self.blocks = numpy.array(blocks_arr,copy=True, \
                                      dtype=numpy.uint8).reshape( \
                (self.height,self.length,self.width))

            self.data = numpy.array(data_arr,copy=True, \
                                        dtype=numpy.uint8).reshape( \
                (self.height,self.length,self.width))
        else:
            self.width = 0
            self.height = 0
            self.length = 0
            self.blocks = numpy.array(0,ndmin=3,dtype=numpy.uint8)
            self.data   = numpy.array(0,ndmin=3,dtype=numpy.uint8)

    def write(self, filename):
        s = blocks.NBTString()
        s.addCompound("Schematic")
        s.addShort(self.width,  "Width")
        s.addShort(self.length, "Length")
        s.addShort(self.height, "Height")

        ids = []
        data = []
        for z in range(self.height):
            for y in range(self.length):
                for x in range(self.width):
                    ids.append(self.blocks[z][y][x])
                    data.append(self.data[z][y][x])

        s.addByteArray(ids,  'Blocks')
        s.addByteArray(data, 'Data')

        s.addList(blocks.TAG_Compound, [], 'Entities')
        s.addList(blocks.TAG_Compound, [], 'TileEntities')
        s.addEnd()
        
        f = gzip.GzipFile(filename, 'wb')
        f.write(s.getString())
        f.close()



    def insert(self, rhs, x, y, z):
        min_width  = rhs.width  + x
        min_length = rhs.length + y
        min_height = rhs.height + z

        new_width  = max(min_width, self.width)
        new_length = max(min_length, self.length)
        new_height = max(min_height, self.height)

        if new_width > self.width or \
                new_length > self.length or \
                new_height > self.height:

            new_blocks = numpy.zeros((new_height, new_length, new_width),
                                     dtype=numpy.uint8)
            new_data   = numpy.zeros((new_height, new_length, new_width),
                                     dtype=numpy.uint8)
            for k in range(self.height):
                for j in range(self.length):
                    for i in range(self.width):
                        new_blocks[k][j][i] = self.blocks[k][j][i]
                        new_data[k][j][i] = self.data[k][j][i]

            self.data = new_data
            self.blocks = new_blocks
            self.width = new_width
            self.length = new_length
            self.height = new_height

        for k in range(rhs.height):
            for j in range(rhs.length):
                for i in range(rhs.width):
                    self.blocks[k+z][j+y][i+x] = rhs.blocks[k][j][i]
                    self.data[k+z][j+y][i+x]   = rhs.data[k][j][i]
       
if __name__ == '__main__':

    prefix_cell = Schematic('pcell.schematic')

    adder = Schematic()


    s.insert(s_2, 0,8,0)
    s.insert(s_2, 1,0,1)

    s.write('tiled.schematic')
