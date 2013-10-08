#===============================================================================
#Python Perlin Noise based map generation
#   This program creates a pseudo-random noise pattern and then smooths it and
#   applies a cos based intropilation. It then layers several octaves of noise
#   and uses a weighted average of them. A mask is then applied.
#===============================================================================

import Image
import primes
import perlin
from random import randint
from math import sqrt

width=256
height=256
octaves=[1,2,4,8,16,32]

threshold=30

#seed generation
if raw_input('Generate seed? y/n ')[0]=='y':
    seed=primes.nextPrime(randint(10000,50000))
    print ("The seed is "+str(seed))
else:
    seed=primes.nextPrime(int(raw_input('Enter a seed: (numbers only) ')))
    print ("The seed is "+str(seed))

#noise generation
print('Generating heightmap...')
heightMap=perlin.perlin2d(width,height,octaves,seed)
print('Done!')

#creates empty coastline
landMap=[]
for y in range(width):
    landMap.append([])
    for x in range(height):
        landMap[y].append([])

#processing
for x in range(width):
    for y in range(height):
        val = heightMap[y][x]

        #mask creation and aplication
        dist = int(1.5 * (sqrt(abs(128 - x) ** 2 + abs(128 - y) ** 2)))
        val -= dist
        if val < 0: val = 0
        heightMap[y][x] = val

        #coastline creation
        val2 = val
        if val2 < threshold: val2 = (138,210,255)
        else: val2 = (255,233,161)
        landMap[y][x] = val2

#image creation
img=Image.new('RGB',(width,height),'black')
pixels=img.load()

#map to image
for x in range(width):
    for y in range(height):
        val=heightMap[y][x]
        val=(val,val,val)
        val2=landMap[y][x]
        val3=(
            (val2[0]*(val[0]+50))/255,
            (val2[1]*(val[1]+50))/255,
            (val2[2]*(val[2]+50))/255
            )
        pixels[x,y]=val3

img.save('map.png')