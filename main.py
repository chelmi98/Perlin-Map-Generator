#!/usr/bin/env python
'''
Python Perlin Noise based map generation
    This program creates a pseudo-random noise pattern and then
    applies a cos based interpolation. It then layers several octaves of noise
    and uses a weighted average of them. A mask is then applied.
'''

import sys
import getopt
import datetime
import json
import os
from PIL import Image
from perlin import perlin2d
from random import randint
from math import sin, radians
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


def loadJson(path):
    f = open(path)
    j = json.load(f)
    f.close()
    return j


def processMap(srcMap, config, wrapX, wrapY, raw):
    height = len(srcMap)
    width = len(srcMap[0])
    thresholds = config['thresholds']

    #creates empty 2d array
    landMap = [[None] * width for __ in xrange(height)]

    if not raw:
        #processes thresholds
        for x in xrange(width):
            for y in xrange(height):
                val = srcMap[y][x]

                #mask creation and application
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
                for i in xrange(len(thresholds)):
                    if val2 > thresholds[i]['height'] + randint(-1, 1):
                        val2 = tuple(thresholds[i]['color'])
                        break

                if val2 == val:
                    val2 = tuple(config['baseColor'])

                landMap[y][x] = val2

    else:
        #processes raw
        for x in xrange(height):
            for y in xrange(width):
                val = srcMap[y][x]

                #mask creation and application
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

                landMap[y][x] = (val, val, val)

    return landMap


def main():
    #variables
    validExtentions = ['.png', '.jpg', '.jpeg', '.jpe', '.bmp', '.gif']
    validChars = "-_.() %s%s" % (ascii_letters, digits)

    #gets parameters if ran from command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'xyrw:h:o:s:n:c:')
    except getopt.GetoptError:
        print('ERROR: Invalid option')
        sys.exit()
    except:
        print('Unexpected error parsing options')
        sys.exit()

    #default values
    wrapX = False
    wrapY = False
    raw = False
    width = 256
    height = 256
    octaves = [1, 2, 4, 8, 16]
    seed = nextPrime(randint(10000, 100000000))
    flname = 'map.png'
    cnfgname = 'default.json'

    #sets values if run from command line
    for o, a in opts:
        if o == '-x':
            wrapX = True

        if o == '-y':
            wrapY = True

        if o == '-r':
            raw = True

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

        if o == '-o':
            try:
                octaves = [2**i for i in range(int(a))]
            except ValueError:
                print('ERROR: -o [octaves] must be an integer')
                sys.exit()

        if o == '-s':
            try:
                seed = int(a)
            except ValueError:
                print('ERROR: -s [seed] must be an integer')
                sys.exit()
            seed = nextPrime(seed)

        if o == '-n':
            flname = a
            for c in flname:
                if c not in validChars:
                    print('ERROR: Filename cannot contain special characters')
                    sys.exit()
            if not flname[flname.index('.'):].lower() in validExtentions:
                print('ERROR: Filename must contain a valid image extention')
                sys.exit()

        if o == '-c':
            cnfgname = a
            for c in cnfgname:
                if c not in validChars:
                    print('ERROR: Filename cannot contain special characters')
                    sys.exit()
            if cnfgname[cnfgname.index('.'):].lower() != '.json':
                print('ERROR: Configuration file must be a JSON file.')
                sys.exit()

    try:
        config = loadJson(os.path.join(os.path.curdir, 'templates', cnfgname))
    except IOError:
        print('ERROR: Configuration file does not exist')
        sys.exit()
    except ValueError:
        print('ERROR: JSON file is incorrectly formatted')
        sys.exit()

    print ('The seed is %i' % seed)

    #starts the timer
    start = datetime.datetime.now()

    print('Generating heightmap...'),
    heightMap = perlin2d(width, height, octaves, seed)
    print('Done!')

    print('Processing...'),
    landMap = processMap(heightMap, config, wrapX, wrapY, raw)
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

    #prints the duration the program ran
    duration = datetime.datetime.now() - start
    print('%im %is' % (duration.seconds / 60, duration.seconds % 60))

if __name__ == '__main__':
    main()
