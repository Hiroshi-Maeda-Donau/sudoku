# 2020.7.11 s_access2.py
# 2021.1.30 問題を解くルーチン削除

import numpy as np
from sudoku_web2 import *

# 問題をs_mondai.txtに追加書き込み
def monwrite():

   # 数独問題をファイルから読む
    Q=np.loadtxt('q_temp.txt')
    Qtemp=np.loadtxt('q_answer.txt')
    W=np.mat(Q,dtype='int')
    Wtemp=np.mat(Qtemp,dtype='int')

    # 問題と解答を比較
    flag_compare=1
    for i in range(9):
        for j in range(9):
            x1=W[i,j]
            x2=Wtemp[i,j]
            if x1>0 and x1!=x2:
                flag_compare=0

    Qmondai=np.mat(W,dtype='str')

    if flag_compare==0:
        Qans_tmp=np.zeros(shape=[9,9],dtype='int')
        Qans=np.mat(Qans_tmp,dtype='str')
    else:
        Qans=np.mat(Wtemp,dtype='str')


    # Qmondai(9X9)を１行のテキストに変換
    a1=""
    for x1 in range(9):
        for y1 in range(9):
            a1=a1+str(Qmondai[x1,y1])

    # Qans(9X9)を１行のテキストに変換
    a2=""
    for x1 in range(9):
        for y1 in range(9):
            a2=a2+str(Qans[x1,y1])

    # message
    mess=""
    if flag_compare==1:
        f=open("message.txt","r")
        lines=f.readlines()
        f.close()
        mess=lines[0]
    else:
        mess="no answer"

    a3=mess

    # s_mondaiを読んで更新
    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close()

    numx=lines[0]

    numy=int(numx)
    numy=numy+1
    numz=str(numy)

    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close()

    lines[0]=numz+"\n"

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

# 問題をs_mondai.txtに上書き
def monovw():

   # 数独問題をファイルから読む
    Q=np.loadtxt('q_temp.txt')
    Qtemp=np.loadtxt('q_answer.txt')
    W=np.mat(Q,dtype='int')
    Wtemp=np.mat(Qtemp,dtype='int')


    # 問題と解答を比較
    flag_compare=1
    for i in range(9):
        for j in range(9):
            x1=W[i,j]
            x2=Wtemp[i,j]
            if x1>0 and x1!=x2:
                flag_compare=0

    Qmondai=np.mat(W,dtype='str')

    if flag_compare==0:
        Qans_tmp=np.zeros(shape=[9,9],dtype='int')
        Qans=np.mat(Qans_tmp,dtype='str')
    else:
        Qans=np.mat(Wtemp,dtype='str')


    # Qmondai(9X9)を１行のテキストに変換
    a1=""
    for x1 in range(9):
        for y1 in range(9):
            a1=a1+str(Qmondai[x1,y1])

    # Qans(9X9)を１行のテキストに変換
    a2=""
    for x1 in range(9):
        for y1 in range(9):
            a2=a2+str(Qans[x1,y1])

    # message
    mess=""
    if flag_compare==1:
        f=open("message.txt","r")
        lines=f.readlines()
        f.close()
        mess=lines[0]
    else:
        mess="no answer"

    a3=mess

    # s_mondaiを読んで更新

    f=open("qptr.txt","r+")
    lines=f.readlines()
    f.close()

    numx=lines[0]
    numy=int(numx)
    numz=str(numy)

    lx1=3*(numy-1)+1
    lx2=3*(numy-1)+2
    lx3=3*(numy-1)+3

    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close()

    lines[lx1]=a1+"\n"
    lines[lx2]=a2+"\n"
    lines[lx3]=a3+"\n"

    #s_mondai.tstを書き換え
    f=open("s_mondai.txt","w")
    lines=f.writelines(lines)
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

