TABLESIZE = 9

constset = set([0,1,2,3,4,5,6,7,8,9])

updateCount = 0
margeCount = 0

hintmap = []
for i in range(TABLESIZE):
    hintmap.append([[]] * TABLESIZE)

yTable = [[],[],[],[],[],[],[],[],[]]
table  = [[],[],[],[],[],[],[],[],[]]


def main():
    global updateCount
    global margeCount

    while(clearCheck() == False):
        checked = 0
        for x in range(TABLESIZE):
            for y in range(TABLESIZE):
                if(table[y][x] == 0):
                    hintmap[y][x]=update(x,y)
                    updateCount += 1
                    if(len(hintmap[y][x]) == 1):
                        table[y][x] = hintmap[y][x][0]
                        print("UPDATE",x+1,y+1,table[y][x])
                        checked +=1

        if(checked == 0): #値が上の方法では更新できなかったときに処理を書く
            for x in range(TABLESIZE):
                for y in range(TABLESIZE):
                    if(table[y][x] == 0 and len(hintmap[y][x]) >= 1):
                        marge(x,y)
                        margeCount += 1
                        if(len(hintmap[y][x]) == 1):
                            table[y][x] = hintmap[y][x][0]
                            print("MARGED",x+1,y+1,table[y][x])

        if(updateCount >= 1500): #とりあえず、3000回更新しても何もなかったら強制終了
            print("Resolving Failed")
            break
    print2array()
    print("Update Count " ,updateCount)



def clearCheck(): #未入力地点が無いことを検索
    for x in range(TABLESIZE):
        for y in range(TABLESIZE):
            if(table[x][y] == 0):
                return False
    return True


def print2array(): #2次元配列をきれいに表示するだけ
    for i in range(TABLESIZE):
        for j in range(TABLESIZE):
            print(table[i][j],end=" ")
        print("")


def inputTable(): #標準入力でテーブルを受け取る
    for i in range(TABLESIZE):
        table[i] = [int(s) for s in input("Line" + str(i) + ">> ").split(" ")]


def marge(x, y): #差集合により、
    #x
    tmpset = set(hintmap[y][x])
    li = list(range(TABLESIZE))
    li.remove(x)
    for i in li:
        tmpset = tmpset - set(hintmap[y][i])
    if(len(tmpset) == 1):
        hintmap[y][x] = list(tmpset)
        return

    #y
    tmpset = set(hintmap[y][x])
    li = list(range(TABLESIZE))
    li.remove(y)
    for i in li:
        tmpset = tmpset - set(hintmap[i][x])
    if(len(tmpset) == 1):
        hintmap[y][x] = list(tmpset)
        return

    #囲み
    tmpL = []
    for tl in around9hintmap(x,y):
        tmpL.extend(tl)
    tmpset = set(hintmap[y][x]) - set(tmpL)
    #print("SQUARE",x+1,y+1,hintmap[y][x])
    #print(set(tmpL))
    if(len(tmpset) == 1):
        hintmap[y][x] = list(tmpset)
        return

def update(x, y): #候補の更新
    updateYTable()

    res = constset - set(table[y])
    res = res - set(yTable[x])
    res = res - set(around9table(x,y))

    return list(res)


def updateYTable(): #縦方向のリストを取得してくるだけ
    for y in range(TABLESIZE):
        res = []
        for x in range(TABLESIZE):
            res.append(table[x][y])
        yTable[y] = res


def getSquareP(x, y): #座標がどの囲みに存在するか変換するだけ
    if(x in [0,1,2] and y in [6,7,8]):
        return 1,7
    elif(x in [3,4,5] and y in [6,7,8]):
        return 4,7
    elif(x in [6,7,8] and y in [6,7,8]):
        return 7,7
    elif(x in [0,1,2] and y in [3,4,5]):
        return 1,4
    elif(x in [3,4,5] and y in [3,4,5]):
        return 4,4
    elif(x in [6,7,8] and y in [3,4,5]):
        return 7,4
    elif(x in [0,1,2] and y in [0,1,2]):
        return 1,1
    elif(x in [3,4,5] and y in [0,1,2]):
        return 4,1
    elif(x in [6,7,8] and y in [0,1,2]):
        return 7,1
    else:
        return 4,4


def around9table(x, y): #9マスのリストを取得する、囲みのリストを生成するため
    tx, ty = getSquareP(x,y)
    return [
        table[ty-1][tx-1],table[ty][tx-1],table[ty+1][tx-1],
        table[ty-1][tx  ],table[ty][tx  ],table[ty+1][tx  ],
        table[ty-1][tx+1],table[ty][tx+1],table[ty+1][tx+1]
        ]


def around9hintmap(x,y): #自分以外の値を取得
    tx,ty = getSquareP(x,y)

    res = [
        hintmap[ty-1][tx-1],hintmap[ty][tx-1],hintmap[ty+1][tx-1],
        hintmap[ty-1][tx  ],hintmap[ty][tx  ],hintmap[ty+1][tx  ],
        hintmap[ty-1][tx+1],hintmap[ty][tx+1],hintmap[ty+1][tx+1]
    ]
    res.remove(hintmap[y][x])
    return res


def rprint(x,y,rx,ry,text):
    if(x == rx and y == ry):
        print(text)


#数独のテーブルのいくつか
testT = [
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
easyT = [
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
middleT = [
    [0,0,0,0,0,0,6,0,9],
    [1,0,0,0,0,4,0,0,0],
    [0,0,5,3,0,6,8,2,1],
    [0,0,4,6,7,0,0,5,0],
    [0,0,7,0,0,0,9,0,0],
    [0,0,0,5,4,0,0,0,0],
    [3,7,0,4,0,5,2,0,6],
    [0,0,0,0,0,0,5,1,0],
    [0,6,0,0,2,0,0,3,7]
]
highT = [
    [5,8,6,0,7,0,0,0,0],
    [0,0,0,9,0,1,6,0,0],
    [0,0,0,6,0,0,0,0,0],
    [0,0,7,0,0,0,0,0,0],
    [9,0,2,0,1,0,3,0,5],
    [0,0,5,0,9,0,0,0,0],
    [0,9,0,0,4,0,0,0,8],
    [0,0,3,5,0,0,0,6,0],
    [0,0,0,0,2,0,4,7,0]
]
expartT = [
    [0,0,0,0,0,0,0,0,9],
    [5,9,0,0,0,0,3,0,0],
    [4,0,0,0,6,0,0,0,5],
    [0,0,2,0,0,0,8,7,0],
    [0,0,6,0,0,4,0,0,0],
    [0,3,0,0,8,0,0,0,0],
    [0,0,0,6,0,0,0,3,2],
    [0,0,0,3,0,0,0,1,0],
    [0,0,0,5,4,9,0,0,0]
]

if __name__ == "__main__":
    #inputTable()
    #table = highT
    table = expartT
    main()