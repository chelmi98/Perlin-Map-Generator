#!/usr/bin/env python
#===============================================================================
#Python Perlin Noise based map generation
#   This program creates a pseudo-random noise pattern and then
#   applies a cos based intropilation. It then layers several octaves of noise
#   and uses a weighted average of them. A mask is then applied.
#===============================================================================

import sys
import getopt
import Image
from perlin import perlin2d
from random import randint
from math import sqrt, sin, degrees, radians

def isPrime(p):
    if(p == 2): return True
    if(not(p & 1)): return False
    return pow(2, p-1, p) == 1

def nextPrime(p):
    while True:
        if isPrime(p): return p
        else: p += 1

def processMap(width, height, srcMap, thresholds, thresholdcolors):
    #creates empty 2d array
    landMap=[]
    for y in range(height):
        landMap.append([])
        for x in range(width):
            landMap[y].append([])

    #processing
    for x in range(width):
        for y in range(height):
            val = srcMap[y][x]

            #mask creation and aplication
            maskX = (sin(radians((-180.0 / width) * x)) * 255) + 255
            maskY = (sin(radians((-180.0 / height) * y)) * 255) + 255

            if not wrapX and not wrapY:
                mask = maskX + maskY
            elif wrapX and not wrapY:
                mask = maskY
            elif not wrapX and wrapY:
                mask = maskX
            elif wrapX and wrapY:
                mask = 0

            val -= mask
            val=int(val)
            if val < 0: val = 0
            if val > 255: val = 255
            srcMap[y][x] = val

            #checks height against each threshold in turn
            val2 = val
            for i in range(len(thresholds)):
                if val2 > thresholds[i] + randint(-1, 1):
                    val2 = thresholdcolors[i]
                    break

            if val2 == val:
                val2 = thresholdcolors[len(thresholdcolors) - 1]

            landMap[y][x] = val2

    return landMap

if __name__ == '__main__':
    #gets parameters if ran from command line
    opts, args = getopt.getopt(sys.argv[1:], 'xyw:h:s:n:')

    #default values
    wrapX = False
    wrapY = False
    width = 256
    height = 256
    seed = nextPrime(randint(10000,50000))
    flname = 'map'

    octaves=[1,2,4,8,16]
    thresholds=[
            145,
            90,
            60,
            40,
            30]
    thresholdcolors=[
            (255,255,255),
            (146,168,179),
            (102,150,96),
            (135,179,130),
            (255,233,161),
            (87,148,179)]

    #values if run from command line
    for o, a in opts:
        if o == '-x':
            wrapX = True
        if o == '-y':
            wrapY = True
        if o == '-w':
            width = int(a)
        if o == '-h':
            height = int(a)
        if o == '-s':
            seed = int(a)
        if o == '-n':
            flname = a

    print ('The seed is %s' % (str(seed)))

    print('Generating heightmap...'),
    heightMap = perlin2d(width, height, octaves, seed)
    print('Done!')

    print('Processing...'),
    landMap = processMap(width,height,heightMap,thresholds,thresholdcolors)
    print('Done!')

    print('Creating image...'),
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    #map to image
    for x in range(width):
        for y in range(height):
            pixels[x,y] = landMap[y][x]

    img.save(flname + '.png')
    print('Done!')
    print('Saved as ' + flname + '.png')