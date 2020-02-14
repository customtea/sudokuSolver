TABLESIZE = 9
SQSIZE = 3

constmap = [0,1,2,3,4,5,6,7,8,9]
constset = set([0,1,2,3,4,5,6,7,8,9])

calccount = 0

hintmap = []
for i in range(TABLESIZE):
    hintmap.append([[]] * TABLESIZE)

square = [[],[],[],[],[],[],[],[],[],[]]
yTable = [[],[],[],[],[],[],[],[],[]]

table = [
    [9,2,0,0,1,0,3,0,0],
    [8,5,0,0,9,0,0,2,0],
    [0,0,3,0,0,0,0,0,0],
    [0,0,0,0,0,2,0,0,0],
    [3,0,0,0,0,1,6,0,0],
    [1,9,7,0,0,0,2,5,0],
    [0,0,0,5,0,9,0,6,2],
    [0,8,5,0,2,0,4,0,0],
    [0,0,9,7,4,0,0,3,0]
]
"""
table = [
    [0,6,0,0,8,0,4,2,0],
    [0,1,5,0,6,0,3,7,8],
    [0,0,0,4,0,0,0,6,0],
    [1,0,0,6,0,4,8,3,0],
    [3,0,6,0,1,0,7,0,5],
    [0,8,0,3,5,0,0,0,0],
    [8,3,0,9,4,0,0,0,0],
    [0,7,2,1,3,0,9,0,0],
    [0,0,9,0,2,0,6,1,0]
]
"""

def main():
    while(clearCheck() == False):
        for x in range(TABLESIZE):
            for y in range(TABLESIZE):
                if(table[y][x] == 0):
                    hintmap[y][x]=update(x,y)
                    if(len(hintmap[y][x]) == 1):
                        table[y][x] = hintmap[y][x][0]
                    else:
                        marge(x,y)
                    global calccount
                    calccount += 1
                    if(calccount >= 1000):
                        print("Resolving Failed")
                        break
    print2array()
    print(calccount)



def clearCheck():
    for x in range(TABLESIZE):
        for y in range(TABLESIZE):
            if(table[x][y] == 0):
                return False
    return True


def print2array():
    for i in range(TABLESIZE):
        for j in range(TABLESIZE):
            print(table[i][j],end=" ")
        print("")


def inputTable():
    for i in range(TABLESIZE):
        table[i] = [int(s) for s in input("Line" + str(i) + ">> ").split(" ")]


def marge(x, y):
    tmpset = set(hintmap[y][x])
    li = list(range(TABLESIZE))
    li.remove(x)
    for i in li:
        if(len(hintmap[y][i]) != 1):
            tmpset = tmpset - set(hintmap[y][i])
            if(len(tmpset) == 1):
                hintmap[y][x] = list(tmpset)
                return
    
    tmpset = set(hintmap[y][x])
    li = list(range(TABLESIZE))
    li.remove(y)
    for i in li:
        if(len(hintmap[i][x]) != 1):
            tmpset = tmpset - set(hintmap[i][x])
            if(len(tmpset) == 1):
                hintmap[y][x] = list(tmpset)
                return
    



def update(x, y):
    updateSquare()
    updateYTable()

    res = constset - set(table[y])
    res = res - set(yTable[x])
    res = res - set(square[getSquareP(x,y)])
    sres = list(res)

    """
    xres = []
    yres = []
    sres = []

    for i in range(len(constmap)):
        if(constmap[i] not in table[y]):
            xres.append(constmap[i])

    for i in range(len(xres)):
        if(xres[i] not in yTable[x]):
            yres.append(xres[i])

    for i in range(len(yres)):
        if(yres[i] not in square[getSquareP(x,y)]):
            sres.append(yres[i])
    """

    return sres


def updateYTable():
    for y in range(TABLESIZE):
        res = []
        for x in range(TABLESIZE):
            res.append(table[x][y])

        yTable[y] = res


def updateSquare():
    square[1] = around9(1,7)
    square[2] = around9(4,7)
    square[3] = around9(7,7)
    square[4] = around9(1,4)
    square[5] = around9(4,4)
    square[6] = around9(7,4)
    square[7] = around9(1,1)
    square[8] = around9(4,1)
    square[9] = around9(7,1)


def getSquareP(x, y):
    if(x in [0,1,2] and y in [6,7,8]):
        return 1
    elif(x in [3,4,5] and y in [6,7,8]):
        return 2
    elif(x in [6,7,8] and y in [6,7,8]):
        return 3
    elif(x in [0,1,2] and y in [3,4,5]):
        return 4
    elif(x in [3,4,5] and y in [3,4,5]):
        return 5
    elif(x in [6,7,8] and y in [3,4,5]):
        return 6
    elif(x in [0,1,2] and y in [0,1,2]):
        return 7
    elif(x in [3,4,5] and y in [0,1,2]):
        return 8
    elif(x in [6,7,8] and y in [0,1,2]):
        return 9
    else:
        return 0


def around9(x, y):
    return [
        table[y-1][x-1],table[y][x-1],table[y+1][x-1],
        table[y-1][x  ],table[y][x  ],table[y+1][x],
        table[y-1][x+1],table[y][x+1],table[y+1][x+1]
        ]


def rprint(x, y, rx, ry, text):
    if(x == rx and y == ry):
        print(text)

if __name__ == "__main__":
    #inputTable()
    main()