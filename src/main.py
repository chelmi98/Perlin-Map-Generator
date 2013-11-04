#===============================================================================
#Python Perlin Noise based map generation
#   This program creates a pseudo-random noise pattern and then smooths it and
#   applies a cos based intropilation. It then layers several octaves of noise
#   and uses a weighted average of them. A mask is then applied.
#===============================================================================

import sys
import getopt
import Image
import primes
import perlin
import fill
from random import randint
from math import sqrt

#gets parameters if ran from command line
opts, args = getopt.getopt(sys.argv[1:], 'xyw:h:n:')

#default values
wrapX=False
wrapY=False
width=256
height=256
flname='map'

#values if run from cmd
for o, a in opts:
    if o == '-x':
        wrapX = True
    if o == '-y':
        wrapY = True
    if o == '-w':
        width = int(a)
    if o == '-h':
        height = int(a)
    if o == '-n':
        flname = a

#generation perameters
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

#seed generation
seed=primes.nextPrime(randint(10000,50000))
print ("The seed is "+str(seed))

#noise generation
print 'Generating heightmap... '
heightMap=perlin.perlin2d(width,height,octaves,seed)
print('Done!')

print 'Processing... '
#creates empty coastline
landMap=[]
for y in range(height):
    landMap.append([])
    for x in range(width):
        landMap[y].append([])

#processing
for x in range(width):
    for y in range(height):
        val = heightMap[y][x]

        #mask creation and aplication
        if not wrapX and not wrapY:
            mask=((x-(width/2))**2/(width/4))+((y-(height/2))**2/(height/4))
        elif wrapX and not wrapY:
            mask=(y-(height/2))**2/(height/4)
        elif not wrapX and wrapY:
            mask=(x-(width/2))**2/(width/4)
        elif wrapX and wrapY:
            mask=0

        val -= mask
        val=int(val)
        if val < 0: val = 0
        if val > 255: val = 255
        heightMap[y][x] = val

        #checks height against each threshold in turn
        val2 = val
        for i in range(len(thresholds)):
            if val2 > thresholds[i]+randint(-1,1):
                val2 = thresholdcolors[i]
                break

        if val2==val:
            val2=thresholdcolors[len(thresholdcolors)-1]

        landMap[y][x] = val2

#differentiates between sea and other water (disabled for speed)
##landMap=fill.floodFill(landMap,(70,170,170),0,0)
print('Done!')

#image creation
img=Image.new('RGB',(width,height),'black')
pixels=img.load()

#map to image
for x in range(width):
    for y in range(height):
        pixels[x,y]=landMap[y][x]

img.save(flname+'.png')
print('Saved as '+flname+'.png')