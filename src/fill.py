def floodFill(src,rplc,x,y):
    width=len(src[0])
    height=len(src)
    color = src[y][x]
    que = []
    que.append((x,y))
    running=True
    while running:
        for i in que:
            src[i[1]][i[0]]=rplc
            if not i[0]+1 == width and src[i[1]][i[0]+1] == color:
                que.append((i[0]+1,i[1]))
            if not i[1]+1 == height and src[i[1]+1][i[0]] == color:
                que.append((i[0],i[1]+1))
            if not i[0]-1 == 0 and src[i[1]][i[0]-1] == color:
                que.append((i[0]-1,i[1]))
            if not i[1]-1 == 0 and src[i[1]-1][i[0]] == color:
                que.append((i[0],i[1]-1))
            que.remove(i)
        if len(que)==0:
            running=False

    return src