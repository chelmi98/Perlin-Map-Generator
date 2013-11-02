#===============================================================================
#Python Perlin Noise based map generation
#   This program creates a pseudo-random noise pattern and then smooths it and
#   applies a cos based intropilation. It then layers several octaves of noise
#   and uses a weighted average of them. A mask is then applied.
#===============================================================================

import Image
import primes
import perlin
import fill
from random import randint
from math import sqrt

width=256
height=256
octaves=[1,2,4,8,16]
wrapX=False
wrapY=False

threshold=30
threshold2=40
threshold3=60
threshold4=90
threshold5=145

#seed generation
##if raw_input('Generate seed? y/n ')[0]=='y':
seed=primes.nextPrime(randint(10000,50000))
print ("The seed is "+str(seed))
##else:
##    seed=primes.nextPrime(int(raw_input('Enter a seed: (numbers only) ')))
##    print ("The seed is "+str(seed))

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

        #coastline creation
        val2 = val
        if val2 < threshold: val2 = (87,148,179)
        elif val2 < threshold2: val2 = (255,233,161)
        elif val2 < threshold3: val2 = (135,179,130)
        elif val2 < threshold4: val2 = (102,150,96)
        elif val2 < threshold5: val2 = (146,168,179)
        else: val2 = (255,255,255)
        landMap[y][x] = val2

#landMap=fill.floodFill(landMap,(70,170,170),0,0)
print('Done!')

#image creation
img=Image.new('RGB',(width,height),'black')
pixels=img.load()

#map to image
for x in range(width):
    for y in range(height):
        pixels[x,y]=landMap[y][x]

img.save('map.png')