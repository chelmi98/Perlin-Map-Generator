#===============================================================================
#Python Perlin Noise based map generation
#   This program creates a pseudo-random noise pattern and then smooths it and
#   applies a cos based intropilation. It then layers several octaves of noise
#   and uses a weighted average of them. A mask is then applied.
#(c) Charlie Helmich 2013
#===============================================================================

import Image
import primes
from perlin import perlin2d
from random import randint
from math import sqrt

#seed generation
if raw_input('Generate seed? y/n')[0]=='y':
    seed=primes.nextPrime(randint(10000,50000))
    print ("The seed is "+str(seed))
else:
    seed=primes.nextPrime(int(raw_input('Enter a seed: (numbers only)')))
    print ("The seed is "+str(seed))

#image creation and pixel stuff
print('Generating heightmap...')
heightMap=perlin2d(256,256,6,seed)
print('Done!')

img=Image.new('RGB',(256,256),'black')
pixels=img.load()

for x in range(256):
    for y in range(256):
        val=heightMap[y][x]
        dist=int(1.5*(sqrt(abs(128-x)**2+abs(128-y)**2)))
        val-=dist
        if val<0:val=0
        pixels[x,y]=(val,val,val)

img.save('map.png')