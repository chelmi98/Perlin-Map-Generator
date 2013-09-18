from math import cos, pi, sqrt

def noise(x,y,seed):
    n=x+y*57
    n=(n<<13)^n
    return (1.0-((n*(n*n*seed+789221)+1376312589)&0x7fffffff)/1073741824.0)

def intropilate(a,b,x):
    f=(1-cos(x*pi))*0.5
    return a*(1-f)+b*f

def intropilate2d(x,y,preNoise,seed):
    intX=int(x)
    frcX=x-intX
    intY=int(y)
    frcY=y-intY

    try:v1=preNoise[intX][intY]
    except:v1=noise(intX,intY,seed)

    try:
        v2=preNoise[intX+1][intY]
        v3=preNoise[intX][intY+1]
        v4=preNoise[intX+1][intY+1]
    except:
        v2=noise(intX+1,intY,seed)
        v3=noise(intX,intY+1,seed)
        v4=noise(intX+1,intY+1,seed)

    i1=intropilate(v1,v2,frcX)
    i2=intropilate(v3,v4,frcX)

    return intropilate(i1,i2,frcY)

def noiseMap(w,h,d,seed):
    i=1.0/d
    rX=(w/d)+1
    rY=(h/d)+1
    l=[]

    preNoise=[]
    for x in range(rX):
        preNoise.append([])
        for y in range(rY):
            preNoise[x].append(noise(x,y,seed))

    for y in range(rY):
        for y2 in range(d):
            l.append([])
            for x in range(rX):
                for x2 in range(d):
                    l[(y*d)+y2].append(
                        intropilate2d((x2+(x*d))*i,(y2+(y*d))*i,preNoise,seed))

    return l

#DONT USE AT THE MOMENT
def perlin2d(width,height,octaves,seed,limitLow=0,limitHigh=255):
    maps=[]
    xPoints=width
    yPoints=height
    for i in range(octaves):
        maps.append(noiseMap(width,height,xPoints,yPoints,seed))
        xPoints/=2
        yPoints/=2
    pix=[]
    for y in range(height):
        pix.append([])
        for x in range(width):
            tmp=0
            for i in range(octaves):
                tmp+=maps[i][y][x]*(2**i)
            tmp/=(2**octaves)-1
            if tmp<limitLow:
                tmp=limitLow
            elif tmp>limitHigh:
                tmp=limitHigh
            pix[y].append(tmp)
    return pix