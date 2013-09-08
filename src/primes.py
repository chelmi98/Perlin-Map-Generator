def isPrime(p):
    if(p==2): return True
    if(not(p&1)): return False
    return pow(2,p-1,p)==1

def nextPrime(p):
    while True:
        if isPrime(p):break
        else: p+=1
    return p