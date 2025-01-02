# -*- coding: utf-8 -*-
import typing
import time
from term_printer import Color, cprint, StdText, Format
import json

TABLESIZE = 9
CONSTSET = set([0,1,2,3,4,5,6,7,8,9])

def cursor_hide():
    print('\033[?25l', end='')

def cursor_show():
    print('\033[?25h', end='')

def setup():
    clear_screen()
    cursor_hide()

def cursor_top():
    print("\033[;H")

def clear_screen():
    print("\033[;H\033[2J")

cursor_hide()

class SudokuSolver():
    def __init__(self, table):
        self.updateCount = 0
        self.margeCount = 0

        self. hintmap: typing.List[typing.List[typing.List[int]]] = []
        for _ in range(TABLESIZE):
            self.hintmap.append([[]] * TABLESIZE)

        self.table: typing.List[typing.List[int]]  = [[],[],[],[],[],[],[],[],[]]
        self.y_table: typing.List[typing.List[int]] = [[],[],[],[],[],[],[],[],[]]
        
        self.table = table
    
    def save(self, filename):
        table = self.table
        ytable = self.y_table
        hintmap = self.hintmap
        td = {
            "table": table,
            "ytable":ytable,
            "hint": hintmap
        }
        with open(filename, "w") as f:
            json.dump(td, f)
    
    def load(self, filename):
        with open(filename) as f:
            td = json.load(f)
        self.table = td["table"]
        self.y_table = td["ytable"]
        self.hintmap = td["hint"]

    def solve(self):
        clear_screen()
        self.step_count = 0
        while(not self.is_clear()):
            checked = 0
            for y in range(TABLESIZE):
                for x in range(TABLESIZE):
                    if(table[y][x] == 0):
                        self.hintmap[y][x]=self.update(x,y)
                        self.updateCount += 1
                        self.step_count += 1
                        print(f"STEP:{self.step_count:04}  {x+1} {y+1}", " "*15)
                        self.print2array_v2(targety=y, targetx=x, color=Color.BG_GREEN)
                        if(len(self.hintmap[y][x]) == 1):
                            table[y][x] = self.hintmap[y][x][0]
                            print(f"STEP:{self.step_count:04}  UPDATE",x+1,y+1,table[y][x])
                            self.print2array_v2(targety=y, targetx=x, color=Color.BG_MAGENTA)
                            checked +=1

            if(checked == 0): #値が上の方法では更新できなかったときに処理を書く
                for y in range(TABLESIZE):
                    for x in range(TABLESIZE):
                        if(table[y][x] == 0 and len(self.hintmap[y][x]) >= 1):
                            self.marge(x,y)
                            self.margeCount += 1
                            self.step_count += 1
                            print(f"STEP:{self.step_count:04}  {x+1} {y+1}", " "*15)
                            self.print2array_v2(targety=y, targetx=x, color=Color.BG_BLUE)
                            if(len(self.hintmap[y][x]) == 1):
                                table[y][x] = self.hintmap[y][x][0]
                                print(f"STEP:{self.step_count:04}  MARGED",x+1,y+1,table[y][x])
                                self.print2array_v2(targety=y, targetx=x, color=Color.BG_RED)

            if(self.updateCount >= 1500): #とりあえず、1500回更新しても何もなかったら強制終了
                print("Solving Failed")
                self.save("fail")
                break
        # print("Final")
        # self.print2array()
        self.print2array_v2()
        # clear_screen()
        # print("Update Count " ,self.updateCount)
        
    
    def marge(self, x, y): #差集合により、唯一の要素があった場合には更新する
        #x
        tmpset = set(self.hintmap[y][x])
        li = list(range(TABLESIZE))
        li.remove(x)
        for i in li:
            tmpset = tmpset - set(self.hintmap[y][i])
        if(len(tmpset) == 1):
            self.hintmap[y][x] = list(tmpset)
            return

        #y
        tmpset = set(self.hintmap[y][x])
        li = list(range(TABLESIZE))
        li.remove(y)
        for i in li:
            tmpset = tmpset - set(self.hintmap[i][x])
        if(len(tmpset) == 1):
            self.hintmap[y][x] = list(tmpset)
            return

        #囲み
        tmpL = []
        for tl in self.around9hintmap(x,y):
            tmpL.extend(tl)
        tmpset = set(self.hintmap[y][x]) - set(tmpL)
        #print("SQUARE",x+1,y+1,hintmap[y][x])
        #print(set(tmpL))
        if(len(tmpset) == 1):
            self.hintmap[y][x] = list(tmpset)
            return
    
    def update(self, x, y): #候補の更新
        self._sync_ytable()

        res = CONSTSET - set(self.table[y]) # 横方向
        res = res - set(self.y_table[x]) # 縦方向
        res = res - set(self.around9table(x,y)) #マス

        return list(res)

    def _sync_ytable(self): #ytableをtableと同期させる
        for y in range(TABLESIZE):
            res = []
            for x in range(TABLESIZE):
                res.append(self.table[x][y])
            self.y_table[y] = res

    def getSquareP(self, x, y): #座標を囲みの中心に変換する
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


    def around9table(self, x, y): #9マスのリストを取得する、囲みのリストを生成するため
        tx, ty = self.getSquareP(x,y)
        return [
            self.table[ty-1][tx-1],self.table[ty][tx-1],self.table[ty+1][tx-1],
            self.table[ty-1][tx  ],self.table[ty][tx  ],self.table[ty+1][tx  ],
            self.table[ty-1][tx+1],self.table[ty][tx+1],self.table[ty+1][tx+1]
            ]


    def around9hintmap(self, x, y): #自分以外の値を取得
        tx,ty = self.getSquareP(x,y)

        res = [
            self.hintmap[ty-1][tx-1],self.hintmap[ty][tx-1],self.hintmap[ty+1][tx-1],
            self.hintmap[ty-1][tx  ],self.hintmap[ty][tx  ],self.hintmap[ty+1][tx  ],
            self.hintmap[ty-1][tx+1],self.hintmap[ty][tx+1],self.hintmap[ty+1][tx+1]
        ]
        res.remove(self.hintmap[y][x])
        return res


    def is_clear(self): #未入力地点が無いことを検索
        for x in range(TABLESIZE):
            for y in range(TABLESIZE):
                if(self.table[x][y] == 0):
                    return False
        return True

    def print2array(self): #2次元配列をきれいに表示するだけ
        for i in range(TABLESIZE):
            for j in range(TABLESIZE):
                x = self.table[i][j]
                if x == 0:
                    print(" ",end=" ")
                else:
                    print(x,end=" ")
            print("")
        print()

    def print2array_v2(self, targetx=0,targety=0, color=Color.WHITE):
        # print(targety,targetx)
        cursor_top()
        cprint("+-------"*9+"+")
        for i in range(TABLESIZE):
            p_row1 = ["|"]
            p_row2 = ["|"]
            p_row3 = ["|"]
            for j in range(TABLESIZE):
                h = self.hintmap[i][j]
                x = self.table[i][j]
                r1,r2,r3 = self.hint_square(x, h)
                if not x == 0:
                    r1 = str(StdText("".join(r1), Format.REVERSE))
                    r2 = str(StdText("".join(r2), Format.REVERSE))
                    r3 = str(StdText("".join(r3), Format.REVERSE))
                    p_row1.append(r1)
                    p_row2.append(r2)
                    p_row3.append(r3)
                elif j == targetx and i == targety:
                    r1 = str(StdText("".join(r1), color))
                    r2 = str(StdText("".join(r2), color))
                    r3 = str(StdText("".join(r3), color))
                    p_row1.append(r1)
                    p_row2.append(r2)
                    p_row3.append(r3)
                else:
                    p_row1.extend(r1)
                    p_row2.extend(r2)
                    p_row3.extend(r3)
                p_row1.append("|")
                p_row2.append("|")
                p_row3.append("|")
            cprint("".join(p_row1))
            cprint("".join(p_row2))
            cprint("".join(p_row3))
            cprint("+-------"*9+"+")
        # time.sleep(1)
        # time.sleep(0.1)
        # time.sleep(0.03)
        # os.system("cls")
    
    def hint_square(self, ans, hint):
        SP = "  "
        row1 = []
        row2 = []
        row3 = []
        if not ans == 0:
            row1.extend([SP, f" {SP}", SP])
            row2.extend([SP, f" {ans} ", SP])
            row3.extend([SP, f" {SP}", SP])
            return row1, row2, row3
        if 1 in hint:
            row1.append(" 1")
        else:
            row1.append(SP)
        if 2 in hint:
            row1.append("  2")
        else:
            row1.append("   ")
        if 3 in hint:
            row1.append(" 3")
        else:
            row1.append(SP)
        if 4 in hint:
            row2.append(" 4")
        else:
            row2.append(SP)
        if 5 in hint:
            row2.append("  5")
        else:
            row2.append("   ")
        if 6 in hint:
            row2.append(" 6")
        else:
            row2.append(SP)
        if 7 in hint:
            row3.append(" 7")
        else:
            row3.append(SP)
        if 8 in hint:
            row3.append("  8")
        else:
            row3.append("   ")
        if 9 in hint:
            row3.append(" 9")
        else:
            row3.append(SP)
        return row1, row2, row3



def inputTable(): #標準入力でテーブルを受け取る
    for i in range(TABLESIZE):
        table[i] = [int(s) for s in input("Line" + str(i) + ">> ").split(" ")]


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
    # table = [
    #     [1,0,0,0,4,0,7,0,0],
    #     [0,0,2,0,0,5,9,0,0],
    #     [0,3,0,0,0,0,0,0,0],
    #     [0,5,0,0,0,9,0,0,8],
    #     [0,0,7,0,0,0,1,0,0],
    #     [2,0,0,3,0,0,0,7,0],
    #     [0,0,0,0,0,0,0,2,0],
    #     [0,0,5,8,0,0,6,0,0],
    #     [0,0,4,0,5,0,0,0,3],
    # ]
    sd = SudokuSolver(table)
    # sd.load("fail")
    # sd.print2array_v2()
    sd.solve()
