#!/usr/bin/env python
#==============================================================================
#Python Perlin Noise based map generation
#   This program creates a pseudo-random noise pattern and then
#   applies a cos based intropilation. It then layers several octaves of noise
#   and uses a weighted average of them. A mask is then applied.
#==============================================================================

import sys
import getopt
import Image
from perlin import perlin2d
from random import randint
from math import sqrt, sin, degrees, radians
from string import ascii_letters, digits


def isPrime(p):
    if(p == 2):
        return True
    if(not(p & 1)):
        return False
    return pow(2, p-1, p) == 1


def nextPrime(p):
    while True:
        if isPrime(p):
            return p
        else:
            p += 1


def processMap(width, height, wrapX, wrapY, srcMap, thrshlds, thrshldcColors):
    #creates empty 2d array
    landMap = [[None] * width for __ in xrange(height)]

    #processing
    for x in xrange(width):
        for y in xrange(height):
            val = srcMap[y][x]

            #mask creation and aplication
            if not wrapX:
                maskX = (sin(radians((-180.0 / width) * x)) * 255) + 255
            else:
                maskX = 0
            if not wrapY:
                maskY = (sin(radians((-180.0 / height) * y)) * 255) + 255
            else:
                maskY = 0

            val -= maskX + maskY
            val = int(val)
            if val < 0:
                val = 0
            if val > 255:
                val = 255
            srcMap[y][x] = val

            #checks height against each threshold in turn
            val2 = val
            for i in xrange(len(thrshlds)):
                if val2 > thrshlds[i] + randint(-1, 1):
                    val2 = thrshldcColors[i]
                    break

            if val2 == val:
                val2 = thrshldcColors[len(thrshldcColors) - 1]

            landMap[y][x] = val2

    return landMap

def main():
    #variables
    validExtentions = ['.png', '.jpg', '.jpeg', '.jpe', '.bmp', '.gif']
    validChars = "-_.() %s%s" % (ascii_letters, digits)

    #gets parameters if ran from command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'xyw:h:s:n:')
    except getopt.GetoptError:
        print('ERROR: Invalid option')
        sys.exit()
    except:
        print('Unexpected error parsing options')
        sys.exit()

    #default values
    wrapX = False
    wrapY = False
    width = 256
    height = 256
    seed = nextPrime(randint(10000, 50000))
    flname = 'map.png'

    octaves = [1, 2, 4, 8, 16]
    thrshlds = [145, 90, 60, 40, 30]
    thrshldcColors = [
        (255, 255, 255),
        (146, 168, 179),
        (102, 150, 96),
        (135, 179, 130),
        (255, 233, 161),
        (87, 148, 179)]

    #sets values if run from command line
    for o, a in opts:
        if o == '-x':
            wrapX = True

        if o == '-y':
            wrapY = True

        if o == '-w':
            try:
                width = int(a)
            except ValueError:
                print('ERROR: -w [width] must be an integer')
                sys.exit()

        if o == '-h':
            try:
                height = int(a)
            except ValueError:
                print('ERROR: -h [height] must be an integer')
                sys.exit()

        if o == '-s':
            try:
                seed = int(a)
            except ValueError:
                print('ERROR: -s [seed] must be an integer')
                sys.exit()
            print ('The seed is %s' % (str(seed)))

        if o == '-n':
            flname = a
            for c in flname:
                if c not in validChars:
                    print('ERROR: Filename cannot contain special characters')
                    sys.exit()
            if not flname[flname.index('.'):] in validExtentions:
                print('ERROR: Filename must contain a valid image extention')
                sys.exit()

    print('Generating heightmap...'),
    heightMap = perlin2d(width, height, octaves, seed)
    print('Done!')

    print('Processing...'),
    landMap = processMap(width, height, wrapX, wrapY,
                         heightMap, thrshlds, thrshldcColors)
    print('Done!')

    print('Creating image...'),
    img = Image.new('RGB', (width, height))
    pixels = img.load()

    #map to image
    for x in xrange(width):
        for y in xrange(height):
            pixels[x, y] = landMap[y][x]

    img.save(flname)
    print('Done!')
    print('Saved as ' + flname)

if __name__ == '__main__':
    main()
