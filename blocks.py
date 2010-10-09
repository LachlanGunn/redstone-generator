#!/usr/bin/env python

# Copyright (c) 2010 Lachlan Gunn
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import struct
import zlib

TAG_End        = struct.pack('B', 0)
TAG_Byte       = struct.pack('B', 1)
TAG_Short      = struct.pack('B', 2)
TAG_Int        = struct.pack('B', 3)
TAG_Long       = struct.pack('B', 4)
TAG_Float      = struct.pack('B', 5)
TAG_Double     = struct.pack('B', 6)
TAG_Byte_Array = struct.pack('B', 7)
TAG_String     = struct.pack('B', 8)
TAG_List       = struct.pack('B', 9)
TAG_Compound   = struct.pack('B', 10)

struct_types = 'bhlq'
fmt = {}

for c in struct_types:
    c = '>' + c
    fmt[struct.calcsize(c)*8] = c

class Block(object):
    def __init__(self, type, data):
        self.type = type
        self.data = data

class NBTString(object):

    def __init__(self):
        self.string = ''

    def addEnd(self):
        self.string += TAG_End

    def addByte(self, byte, name = None):
        if name != None:
            self.string += TAG_Byte
            self.addString(name)
        self.string += struct.pack(fmt[8], byte)

    def addShort(self, short, name = None):
        if name != None:
            self.string += TAG_Short
            self.addString(name)
        self.string += struct.pack(fmt[16], short)

    def addInt(self, int, name = None):
        if name != None:
            self.string += TAG_Int
            self.addString(name)
        self.string += struct.pack(fmt[32], int)

    def addLong(self, val, name = None):
        if name != None:
            self.string += TAG_Long
            self.addString(name)
        self.string += struct.pack(fmt[64], val)

    def addFloat(self, val, name = None):
        if name != None:
            self.string += TAG_Float
            self.addString(name)
        self.string += struct.pack('f', val)

    def addDouble(self, val, name = None):
        if name != None:
            self.string += TAG_Double
            self.addString(name)
        self.string += struct.pack('d', val)

    def addByteArray(self, val, name = None):
        if name != None:
            self.string += TAG_Byte_Array
            self.addString(name)
        self.addInt(len(val))
        for byte in val:
            self.string += struct.pack('B', byte)

    def addString(self, val, name = None):
        if name != None:
            self.string += TAG_String
            self.addString(name)
        self.addShort(len(val))
        self.string += struct.pack(str(len(val)) + 's', val)

    def addList(self, type, val, name = None):
        if name != None:
            self.string += TAG_List
            self.addString(name)
        self.string += type
        self.addInt(len(val))

        add = None
        if   type == TAG_Byte:
            add = self.addByte
        elif type == TAG_Short:
            add = self.addShort
        elif type == TAG_Int:
            add = self.addInt
        elif type == TAG_Long:
            add = self.addLong
        elif type == TAG_Float:
            add = self.addFloat
        elif type == TAG_Double:
            add = self.addDouble
        elif type == TAG_Byte_Array:
            add = self.addByteArray
        elif type == TAG_String:
            add = self.addString

        if add != None:
            for element in val:
                add(val)

    def addCompound(self, name):
        self.string += TAG_Compound
        self.addString(name)

    def getString(self):
        return self.string
        


def encode(blocks):
    shape = blocks.shape

    x_size = shape[0]
    y_size = shape[1]
    z_size = shape[2]

    str = ''
