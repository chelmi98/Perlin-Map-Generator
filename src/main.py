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

#seed generation
if raw_input('Generate seed? y/n')[0]=='y':
    seed=primes.nextPrime(randint(10000,50000))
    print ("The seed is "+str(seed))
else:
    seed=primes.nextPrime(int(raw_input('Enter a seed: (numbers only)')))
    print ("The seed is "+str(seed))

#noise generation
print('Generating heightmap...')
heightMap=perlin.perlin2d(width,height,octaves,seed)
print('Done!')

#image creation
img=Image.new('RGB',(width,height),'black')
pixels=img.load()

#map to image
for x in range(width):
    for y in range(height):
        val=heightMap[y][x]

        #mask creation and aplication
        dist=int(1.5*(sqrt(abs(128-x)**2+abs(128-y)**2)))
        val-=dist
        if val<0:val=0

        pixels[x,y]=(val,val,val)

img.save('map.png')