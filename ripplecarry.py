#!/usr/bin/env python

import sys

import schematicreader

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'Usage: ripplecarry.py <bits> <output>'
        sys.exit(1)

    bits = int(sys.argv[1])
    output = sys.argv[2]

    s          = schematicreader.Schematic()
    adder_cell = schematicreader.Schematic('fulladder.schematic')

    x = 0
    y = 0
    z = 0
    for i in range(bits):
        s.insert(adder_cell, x, y, z)
        y += adder_cell.length

    s.write(output)
