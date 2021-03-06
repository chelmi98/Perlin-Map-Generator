from math import cos, pi


#generates rnd number based on seed and coords
def noise(x, y, seed):
    n = x + y * 57
    n = (n << 13) ^ n
    return (1.0 - ((n * (n * n * seed + 789221) + 1376312589)
            & 0x7fffffff) / 1073741824.0)


#intropilates between 2 values
def intropilate(a, b, x):
    f = (1 - cos(x * pi)) * 0.5
    return a * (1 - f) + b * f


#intropilate on a 2d plane
def intropilate2d(x, y, preNoise, seed):
    intX = int(x)
    intY = int(y)

    try:
        v1 = preNoise[intX][intY]
    except:
        v1 = noise(intX, intY, seed)

    try:
        v2 = preNoise[intX + 1][intY]
        v3 = preNoise[intX][intY + 1]
        v4 = preNoise[intX + 1][intY + 1]
    except:
        v2 = noise(intX+1, intY, seed)
        v3 = noise(intX, intY + 1, seed)
        v4 = noise(intX+1, intY + 1, seed)

    i1 = intropilate(v1, v2, x - intX)
    i2 = intropilate(v3, v4, x - intX)

    return intropilate(i1, i2, y - intY)


#creates a 2d array using inropilate 2d
def noiseMap(w, h, d, seed):
    i = 1.0 / d
    rX = (w / d) + 1
    rY = (h / d) + 1
    l = []

    #pre-generates a array of noise
    preNoise = [[noise(x, y, seed) for y in xrange(rY)] for x in xrange(rX)]

    #actually makes the array
    for y in xrange(rY):
        for y2 in xrange(d):
            l.append([])
            for x in xrange(rX):
                for x2 in xrange(d):
                    #VVV [here be dragons] VVV
                    l[(y * d) + y2].append(int(intropilate2d(
                        (x2 + (x * d)) * i, (y2 + (y * d)) * i, preNoise, seed)
                        * 128) + 128)

    return l


#creates several noise maps and layers them based on octave list
def perlin2d(width, height, octaves, seed):
    octaves.sort()

    #creates a list of all noise maps specified
    maps = [noiseMap(width, height, i, seed) for i in octaves]

    #combines those maps
    pix = []
    for y in xrange(height):
        pix.append([])
        for x in xrange(width):
            tmp = sum([i[y][x] * (2 ** maps.index(i)) for i in maps])
            tmp /= (2 ** len(maps)) - 1
            pix[y].append(tmp)

    return pix
