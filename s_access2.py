# 2020.7.11 s_access2.py
import numpy as np
from sudoku_web2 import *

# 問題をs_mondai.txtに書き込み
def monwrite(QX):

    Qh=np.zeros(shape=[9,9],dtype='int')

    #QX避難
    for i1 in range(9):
        for j1 in range(9):
            Qh[i1,j1]=QX[i1,j1]

    lv=7
    numx,mess,Q4=s_web_main(lv,QX)

    QX=Qh

    # QX(9X9)を１行のテキストに変換
    a1=""
    for x1 in range(9):
        for y1 in range(9):
            a1=a1+str(QX[x1,y1])

    # Q4(9X9)を１行のテキストに変換
    a2=""
    for x1 in range(9):
        for y1 in range(9):
            a2=a2+str(Q4[x1,y1])

    # message
    a3=mess

    # s_mondaiを読んで更新
    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close()

    #print("lines[0]=",lines[0])

    numx=lines[0]

    numy=int(numx)
    numy=numy+1
    numz=str(numy)

    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close()

    lines[0]=numz+"\n"

    #print("lines[0]=",lines[0])
    #print("lines=",lines)

    f=open("s_mondai.txt","w+")
    f.writelines(lines)
    f.close
    

    # 問題、答え、メッセージを保存
    f=open("s_mondai.txt","a")
    f.write(a1)
    f.write("\n")
    f.write(a2)
    f.write("\n")
    f.write(a3)
    f.write("\n")
    f.close()

    return mess

# 問題を読み込んで9X9に変換
def monread(numx):	# numxは整数

    # s_mondaiを読む
    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close()

    num_last=int(lines[0])

    if numx>num_last:
        numx=num_last
    elif numx<1:
        numx=1
    else:
        pass

    # 問題読み込み
    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close

    numa1=3*(numx-1)+1
    numa2=numa1+1
    numa3=numa1+2

    a1=lines[numa1]
    a2=lines[numa2]
    a3=lines[numa3]

    Qmon=np.zeros(shape=[9,9],dtype='int')
    Qans=np.zeros(shape=[9,9],dtype='int')

    for ix in range(9):
        for jx in range(9):
            zx=9*ix+jx
            Qmon[ix,jx]=a1[zx]
            Qans[ix,jx]=a2[zx]

    return Qmon,Qans,a3

