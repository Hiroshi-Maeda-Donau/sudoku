# 数独問題解析プログラム　　　　Rev.m  2020.4.11   by Hiroshi Maeda
# for WEB(server.py)		Rev.a  2020.7.9
#                               Rev.b  2020.7.11
#                               Rev.c  2020.7.16  独立宣言-->座席予約
#                               Rev.d  2020.8.2   rotate関数変更、chconv関数追加

import numpy as np

def icw(Wrot):
# i-direction rotation clockwise
    Wrot2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                Wrot2[i1,j1,k1]=Wrot[i1,8-k1,j1]
    return Wrot2

def jcw(Wrot):
# j-direction rotation clockwise
    Wrot2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                Wrot2[i1,j1,k1]=Wrot[k1,j1,8-i1]
    return Wrot2

def kcw(Wrot):
# k-direction rotation clockwisew
    Wrot2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                Wrot2[i1,j1,k1]=Wrot[j1,8-i1,k1]
    return Wrot2

def iccw(Wrot):
# i-direction rotation counterclockwise
    Wrot2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                Wrot2[i1,j1,k1]=Wrot[i1,k1,8-j1]
    return Wrot2

def jccw(Wrot):
# j-direction rotation counterclockwise
    Wrot2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                Wrot2[i1,j1,k1]=Wrot[8-k1,j1,i1]
    return Wrot2

def kccw(Wrot):
# k-direction rotation counterclockwisew
    Wrot2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                Wrot2[i1,j1,k1]=Wrot[8-j1,i1,k1]
    return Wrot2

def c_to_b(Wbl):
# Cube to block（ブロック番号を列とするキューブに変換）
    Wbl2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(3):
        for j1 in range(3):
            for i2 in range(3):
                for j2 in range(3):
                    for k in range(9):

                        bnum=3*i1+j1

                        Wbl2[3*j2+i2,bnum,k]=Wbl[3*i1+i2,3*j1+j2,k]
    return Wbl2

def b_to_c(Wbl):
# block to Cube（上記を通常のキューブに戻す）
    Wbl2=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(3):
        for i2 in range(3):
            for j1 in range(3):
                for j2 in range(3):
                    for k in range(9):
                        i3=3*i1+i2
                        j3=3*j1+j2

                        Wbl2[i3,j3,k]=Wbl[3*j2+i2,3*i1+j1,k]
    return Wbl2


# 三次元化
def dim3(W1,W2):		 # W1:二次元データ、W2:三次元データ
    for i in range(9):           # 行
        for j in range(9):       # 列
            if W1[i,j]==0:
                pass
            else:
                k=W1[i,j]
                W2[i,j,k-1]=1

# 二次元化
def dim2(W1,W2):
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if W1[i,j,k]==0:
                    pass
                else:
                    W2[i,j]=k+1
  
     
# マスク作成
def msk1(W1,W2):			# W1:確定ノード三次元データ
   					# W2:マスクノード三次元データ
    for i1 in range(3):
        for i2 in range(3):
            for j1 in range(3):
                for j2 in range(3):
                    for k in range(9):
                        i=3*i1+i2
                        j=3*j1+j2
                        num=W1[i,j,k]
                        if num==1:
                            for l in range(9):	# 行方向マスク
                                W2[l,j,k]=1

                            for r in range(9):	# 列方向マスク
                                W2[i,r,k]=1

                            for c in range(9):	# カラム方向マスク
                                W2[i,j,c]=1

                            for bi in range(3):	# ブロック方向マスク
                                for bj in range(3):
                                    W2[3*i1+bi,3*j1+bj,k]=1

# W1のマスク計算して単独不確定ノードが見つかったらW2に１を入れる
def msk2(W1,W2):
    ext=0
# 行ごとに列方向のマスク和を計算

    for i in range(9):
        for k in range(9):
            sum=0
            for r in range(9):
                sum=sum+W1[i,r,k]
            if sum==8:
                for x in range(9):
                    num=W1[i,x,k]
                    if num==0:
                        ext=1
                        W2[i,x,k]=1

# 列ごとに行方向のマスク和を計算

    for j in range(9):
        for k in range(9):
            sum=0
            for l in range(9):
                sum=sum+W1[l,j,k]
            if sum==8:
                for x in range(9):
                    num=W1[x,j,k]
                    if num==0:
                        ext=1
                        W2[x,j,k]=1

# 行、列ごとにカラム方向のマスク和を計算

    for i in range(9):
        for j in range(9):

            sum=0
            for c in range(9):
                sum=sum+W1[i,j,c]
            if sum==8:
                for x in range(9):
                    num=W1[i,j,x]
                    if num==0:
                        ext=1
                        W2[i,j,x]=1

# ブロックごとにブロック方向のマスク和を計算

    for i1 in range(3):
        for j1 in range(3):
            for k in range(9):
                sum=0
         
                for bi in range(3):
                    for bj in range(3):
                        sum=sum+W1[3*i1+bi,3*j1+bj,k]
                if sum==8:
                    for bi in range(3):
                        for bj in range(3):
                            num=W1[3*i1+bi,3*j1+bj,k]
                            if num==0:
                                ext=1
                                W2[3*i1+bi,3*j1+bj,k]=1
   
    return ext

# 回答数
def figcnt(W3):
    num=0
    for i in range(9):
        for j in range(9):
            x1=W3[i,j]
            if x1==0:
                pass
            else:
                num=num+1
    return num


# マスクのマージ
def merge(W1,W2):		# W1とW2をマージしてW1へ
    for i in range(9):
        for j in range(9):
            for k in range(9):
                num1=W1[i,j,k]
                num2=W2[i,j,k]
                if num1==1 or num2==1:
                    W1[i,j,k]=1

# 独立宣言のマスクを探す
def IndMask(W1):	# W1=CubeMask
    W2=np.zeros(shape=[9,9,9],dtype='int')	# for CubeMaskTemp 
    W3=np.zeros(shape=[9,9,9],dtype='int')	# for core node
    ext=0
    for i1 in range(3):
        for j1 in range(3):
            for k in range(9):
            # ブロック内の未確定ノード数カウント
                bnum=0
                for i2 in range(3):
                    for j2 in range(3):
                        num=W1[3*i1+i2,3*j1+j2,k]
                        if num==0:
                            bnum=bnum+1

            # ブロック行と行の比較
                # ブロック行の未確定ノードカウント
                for bi in range(3):
                    bnumi=0
                    for bj in range(3):	# ブロック行内の未確定ノード数カウント
                        num=W1[3*i1+bi,3*j1+bj,k]
                        if num==0:
                            bnumi=bnumi+1
                        if bnumi>1:

                # 同じ行の未確定ノードカウント
                            numi=0
                            for l in range(9):
                                num=W1[3*i1+bi,l,k]
                                if num==0:
                                    numi=numi+1
                # 比較
                            if bnumi==numi:	# ブロックにマスク
                                if bnumi==bnum:
                                    pass
                                else:
                                    for bi2 in range(3):
                                        for bj2 in range(3): 
                                            if bi2==bi:
                                                W3[3*i1+bi2,3*j1+bj2,k]=1	# core nodes
                                                #pass
                                            else:
                                                W2[3*i1+bi2,3*j1+bj2,k]=1	# mask nodes
                                                ext=1
                            if bnumi==bnum:	# 行にマスク
                                if bnumi==numi:
                                    pass
                                else:
                                    for r in range(9):
                                        if r==3*j1 or r==3*j1+1 or r==3*j1+2:
                                            W3[3*i1+bi,r,k]=1	# core nodes
                                            #pass
                                        else:
                                            W2[3*i1+bi,r,k]=1	# mask nodes
                                            ext=1

           # ブロック列と列の比較
                # ブロック列の未確定ノードカウント
                for bj in range(3):
                    bnumj=0
                    for bi in range(3):	# ブロック列内の未確定ノード数カウント
                        num=W1[3*i1+bi,3*j1+bj,k]
                        if num==0:
                            bnumj=bnumj+1
                        if bnumj>1:

                # 同じ列の未確定ノードカウント
                            numj=0
                            for l in range(9):
                                num=W1[l,3*j1+bj,k]
                                if num==0:
                                    numj=numj+1
                # 比較
                            if bnumj==numj:	# ブロックにマスク
                                if bnumj==bnum:
                                    pass
                                else:
                                    for bi2 in range(3):
                                        for bj2 in range(3):
                                            if bj2==bj:
                                                W3[3*i1+bi2,3*j1+bj2,k]=1	# core nodes
                                                #pass
                                            else:
                                                W2[3*i1+bi2,3*j1+bj2,k]=1	# mask nodes
                                                ext=1

                            if bnumj==bnum:	# 同じ列にマスク
                                if bnumj==numj:
                                    pass
                                else:
                                    for l in range(9):
                                        if l==3*i1 or l==3*i1+1 or l==3*i1+2:
                                            W3[l,3*j1+bj,k]=1	# core nodes
                                            #pass
                                        else:
                                            W2[l,3*j1+bj,k]=1	# mask nodes
                                            ext=1

    return ext,W3,W2

# i方向のコア番号を決める
# j1=j n1=N x1=cnti x2=cntk W3=CORE[2,N+1] W4=INUMi[9] W5=INUMk[9] W6=UFNR[9,9]
# W7=CubeMask W8=CubeMaskTemp m2=mode 
def sub2(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2):	

# CORE配列(2,N)をWh配列(9,9,9)に変換
  #Wcr=np.zeros(shape=[9,9,9],dtype='int')
  #for i1 in range(n1):
    #for k1 in range(n1):
      #iixx=W3[1,i1]
      #kkxx=W3[0,k1]
      #Wcr[iixx,j1,kkxx]=1

      #if j1==1:
          #print("j1=",j1)	#*****************************
          #print("CORE=")	#******************************
          #print(W3)		#******************************
          #print("Wcr=")	#*****************************
          #print(Wcr)	#******************************
  
  ext1=0

  #print("x1=",x1,"  n1=",n1)	#****************************
  for i1 in range(x1-n1+1):
    W3[1,0]=W4[i1]
    for i2 in range(i1+1,x1-n1+2):
      W3[1,1]=W4[i2]
      if n1==2:
        #print("i1=",i1,"  i2=",i2)	#*******************
        #print("W4=")	#********************************
        #print(W4)	#****************************
        #print("W3=")	#**********************************
        #print(W3)	#*********************************
        ext1,Wcr,W8=sub3(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2)

        if ext1==1:
          return ext1,Wcr,W8

      else:
        for i3 in range(i2+1,x1-n1+3):
          W3[1,2]=W4[i3]
          if n1==3:
            ext1,Wcr,W8=sub3(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2)
            if ext1==1:
              return ext1,Wcr,W8
          else:
            for i4 in range(i3+1,x1-n1+4):
              W3[1,3]=W4[i4]
              if n1==4:
                ext1,Wcr,W8=sub3(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2)
                if ext1==1:
                  return ext1,Wcr,W8
              else:
                for i5 in range(i4+1,x1-n1+5):
                  W3[1,4]=W4[i5]
                  if n1==5:
                    ext1,Wcr,W8=sub3(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2)
                    if ext1==1:
                      return ext1,Wcr,W8
                  else:
                    for i6 in range(i5+1,x1-n1+6):
                      W3[1,5]=W4[i6]
                      if n1==6:
                        ext1,Wcr,W8=sub3(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2)
                        if ext1==1:
                          return ext1,Wcr,W8
                      else:
                        for i7 in range(i6+1,x1-n1+7):
                          W3[1,6]=W4[i7]
                          ext1,Wcr,W8=sub3(j1,n1,x1,x2,W3,W4,W5,W6,W7,W8,m2)
                          if ext1==1:
                            return ext1,Wcr,W8
  return ext1,Wcr,W8


# コア情報を決めてマスクする
def sub3(j2,n2,cn1,cn2,WQ,WV,WR,WS,WT,WU,m3):	# n1:コアの大きさ　j2:j=列番号n2:n1=N=n  cn1:cnti   cn2:cntk 
                                                # WQ:W3=CORE WV:W4=INUMi WR:W5=INUMk WS:W6=UFNR WT:W7=W1=CubeMask WU:W8=W2=CubeMaskTemp

  TP=np.zeros(shape=[n2+1,n2+1],dtype='int')		# コアのUFNと縦方向のUFNの数を記憶
  ext2=0

# COREを三次元に変換(Wcr2)
  Wcr3=np.zeros(shape=[9,9,9],dtype='int')
  for i1 in range(n2):
    for k1 in range(n2):
      iixx=WQ[1,i1]
      kkxx=WQ[0,k1]
      Wcr3[iixx,j2,kkxx]=1

# コアの縦横共UFNが１個以上あるか？

  for kx in range(n2):
    for ix in range(n2):

      cni=WQ[1,ix]	#CORE
      cnk=WQ[0,kx]	#CORE

      #print("ix=",ix)	#************************
      #print("kx=",kx)	#************************
      #print("j2=",j2)	#************************
      #print("n2=",n2)	#************************
      #print("cni=",cni)	#************************
      #print("cnk=",cnk)	#***********************
      #print("WQ(CORE)=",WQ)	#*********************

      TP[ix,kx]=WT[cni,j2,cnk]

  cnt2i=0               # TP配列のi方向の不確定ノードの数
  cnt2k=0                # TP配列のk方向の不確定ノードの数
  numi=0                # TP配列のUFNがある行（横方向）の数
  numk=0                # TP配列のUFNがある列（縦方向）の数

  for ix in range(n2):
    cnt2k=0
    for kx in range(n2):
      xx=TP[ix,kx]
      if xx==0:
        cnt2k=cnt2k+1

    TP[ix,n2]=cnt2k
    if cnt2k>=1:
      numi=numi+1

  for kx in range(n2):
    cnt2i=0
    for ix in range(n2):
      xx=TP[ix,kx]
      if xx==0:
        cnt2i=cnt2i+1

    TP[n2,kx]=cnt2i

    if cnt2i>=1:
      numk=numk+1

  if numi==n2 and numk==n2:


# コアの各列にはコア以外にUFNはないか
    numxx=0             # コア列のUFNと列全体のUFNの数が同じ列の数
    for kx2 in range(n2):

      xx2=TP[n2,kx2]
      cnk=WQ[0,kx2]	# CORE
      xx3=WS[j2,cnk]	# UFNR（コア各列のUFNの数）

      if xx2==xx3:	# コア列のマスク条件合致
        numxx=numxx+1

# 上の条件を満たせばマスクする
    if numxx==n2:	# マスク条件全て合致

      for kx3 in range(cn2):
        xxx=WV[kx3]		# INUMiのk方向kx3番目のカラム番号

# xxxがコア列のどれかと一致しないかどうか調べる
        mtch=0
        for kx4 in range(n2):

          yyy=WQ[0,kx4]		# CORE k方向のカラム番号
          if xxx==yyy:		# 調べている列がコア列と一致
            mtch=1

        if mtch==1:
          pass
        else:   		# コア列ではない列のコア行のUFNにマスクをかける
          for ix3 in range(n2):
            xyz=WQ[1,ix3]	# マスクする行（コアi方向）
            ghi=WT[xyz,j2,xxx]
            if ghi==0:
              WU[xyz,j2,xxx]=1

              ext2=1

          if ext2==1:

              return ext2,Wcr3,WU

  return ext2,Wcr3,WU


# NXNコア問題のマスクを探す
# W1=CubeMask m1=mode
def AliMask(N,W1,m1):
    W2=np.zeros(shape=[9,9,9],dtype='int')	# for CubeMaskTemp
    ext=0

# １.準備段階（行、列、ブロック）X数字の面
# 1-(2) 不確定ノードの数をピアごとに数える
# 1-(2)-1  jxk面のi方向の和
    UFNR=np.zeros(shape=[9,9],dtype='int')
    for j in range(9):
        for k in range(9):
            num1=0
            for i in range(9):
                x=W1[i,j,k]
                if x==0:
                    num1=num1+1
            UFNR[j,k]=num1
    
    
# 1-(2)-2  ixj面のk方向の和
    UFNC=np.zeros(shape=[9,9],dtype='int')
    for i in range(9):
        for j in range(9):
            num1=0
            for k in range(9):
                x=W1[i,j,k]
                if x==0:
                    num1=num1+1
            UFNC[i,j]=num1

# ２．マスク作成段階

# (1) コアを探してマスクする
    for j in range(9):	# 不確定ノード数が存在する行の数をカウントする
        INUMi=np.zeros(shape=[9],dtype='int')        	# k方向の不確定ノードの和がゼロでない行番号iを記憶
        INUMk=np.zeros(shape=[9],dtype='int')       	# i方向の不確定ノードの和がゼロでないカラム番号kを記憶
        CORE=np.zeros(shape=[2,9],dtype='int')		# コアの行列番号を記憶（[0,*]がカラム、[1,*]が行）
                                                        # INUMi,INUMkにおけるコア行列番号のイテレータ
        Wcr2=np.zeros(shape=[9,9,9],dtype='int')
        cnti=0	# k方向のUFNが１以上ある行の数
        cntk=0  # i方向のUFNが１以上あるカラムの数

        for i in range(9):
            if UFNC[i,j]>0:
                cnti=cnti+1
                INUMi[cnti-1]=i	# 不確定ノードがカラム方向に存在する行番号

        for k in range(9):
            if UFNR[j,k]>0:
                cntk=cntk+1
                INUMk[cntk-1]=k	# 不確定ノードが行方向に存在するカラム番号

# (2) cntk>=N+1およびcnti>=N ならNXNコアのマトリックスを作る

        if cntk>=N+1 and cnti>=N:	# k方向にマスクがある

            for k1 in range(cnti-N+1):
                CORE[0,0]=INUMk[k1]
                for k2 in range(k1+1,cnti-N+2):
                    CORE[0,1]=INUMk[k2]
                    if N==2:
                        ext,Wcr2,W2=sub2(j,N,cnti,cntk,CORE,INUMi,INUMk,UFNR,W1,W2,m1)

                        if ext==1:
                            #print("j=",j)	#****************************
                            #print("INUMi=")     #*****************************
                            #print(INUMi)        #*****************************
                            #print("INUMk=")	#*****************************
                            #print(INUMk)	#*****************************
                            #print("CORE=")	#******************************
                            #print(CORE)		#*****************************
                            #print("Wcr2=")	#****************************
                            #print(Wcr2)		#*******************************
                            #print("CubeMask(回転後)=")	#***********************
                            #print(W1)	#***********************:
                            return ext,Wcr2,W2
                    else:
                        for k3 in range(k2+1,cnti-N+3):
                            CORE[0,2]=INUMk[k3]
                            if N==3:
                                ext,Wcr2,W2=sub2(j,N,cnti,cntk,CORE,INUMi,INUMk,UFNR,W1,W2,m1)
                                if ext==1:
                                    return ext,Wcr2,W2
                            else:
                                for k4 in range(k3+1,cnti-N+4):
                                    CORE[0,3]=INUMk[k4]
                                    if N==4:
                                        ext,Wcr2,W2=sub2(j,N,cnti,cntk,CORE,INUMi,INUMk,UFNR,W1,W2,m1)
                                        if ext==1:
                                            return ext,Wcr2,W2
                                    else:
                                        for k5 in range(k4+1,cnti-N+5):
                                            CORE[0,4]=INUMk[k5]
                                            if N==5:
                                                ext,Wcr2,W2=sub2(j,N,cnti,cntk,CORE,INUMi,INUMk,UFNR,W1,W2,m1)
                                                if ext==1:
                                                    return ext,Wcr2,W2
                                            else:
                                                for k6 in range(k5+1,cnti-N+6):
                                                    CORE[0,5]=INUMk[k6]
                                                    if N==6:
                                                        ext,Wcr2,W2=sub2(j,N,cnti,cntk,CORE,INUMi,INUMk,UFNR,W1,W2,m1)
                                                        if ext==1:
                                                            return ext,Wcr2,W2
                                                    else:
                                                        for k7 in range(k6+1,cnti-N+7):
                                                            CORE[0,6]=INUMk[k7]
                                                            if N==7:
                                                                ext,Wcr2,W2=sub2(j,N,cnti,cntk,CORE,INUMi,INUMk,UFNR,W1,W2,m1)
                                                                if ext==1:
                                                                    return ext,Wcr2,W2


    return ext,Wcr2,W2


def ToolCube(WX):
    Wix=np.zeros(shape=[9,9,9],dtype='int')
    Wjx=np.zeros(shape=[9,9,9],dtype='int')
    Wkx=np.zeros(shape=[9,9,9],dtype='int')
    Wbx=np.zeros(shape=[9,9,9],dtype='int')
    Wstx=np.zeros(shape=[9,9,9],dtype='int')
    Wwkx=np.zeros(shape=[9,9,9],dtype='int')
    Whist=np.zeros(shape=[9,9,9],dtype='int')
    WB=c_to_b(WX)

# WXのjxk面のi方向の和
    UFNR=np.zeros(shape=[9,9],dtype='int')
    for j in range(9):
        for k in range(9):
            num1=0
            for i in range(9):
                x=WX[i,j,k]
                if x==0:
                    num1=num1+1
            UFNR[j,k]=num1

# WXのixj面のk方向の和
    UFNC=np.zeros(shape=[9,9],dtype='int')
    for i in range(9):
        for j in range(9):
            num1=0
            for k in range(9):
                x=WX[i,j,k]
                if x==0:
                    num1=num1+1
            UFNC[i,j]=num1

# WXのixk面のj方向の和
    UFNL=np.zeros(shape=[9,9],dtype='int')
    for i in range(9):
        for k in range(9):
            num1=0
            for j in range(9):
                x=WX[i,j,k]
                if x==0:
                    num1=num1+1
            UFNL[i,k]=num1

# WBのjxk面のi方向の和
    UFNR_B=np.zeros(shape=[9,9],dtype='int')
    for j in range(9):
        for k in range(9):
            num1=0
            for i in range(9):
                x=WB[i,j,k]
                if x==0:
                    num1=num1+1
            UFNR_B[j,k]=num1

# WBのiXj面のk方向の和
    UFNC_B=np.zeros(shape=[9,9],dtype='int')
    for i in range(9):
        for j in range(9):
            num1=0
            for k in range(9):
                x=WB[i,j,k]
                if x==0:
                    num1=num1+1
            UFNC_B[j,k]=num1

# Wixの作成
    for j in range(9):
        for k in range(9):
            for i in range(9):
                x1=WX[i,j,k]
                x2=UFNR[j,k]
                if x1==0:
                    Wix[i,j,k]=x2

# Wjxの作成
    for i in range(9):
        for k in range(9):
            for j in range(9):
                x1=WX[i,j,k]
                x2=UFNL[i,k]
                if x1==0:
                    Wjx[i,j,k]=x2

# Wkxの作成
    for i in range(9):
        for j in range(9):
            for k in range(9):
                x1=WX[i,j,k]
                x2=UFNC[i,j]
                if x1==0:
                    Wkx[i,j,k]=x2

# Wbxの作成
    Wbx_Temp=np.zeros(shape=[9,9,9],dtype='int')
    for j in range(9):
        for k in range(9):
            for i in range(9):
                x1=WB[i,j,k]
                x2=UFNR_B[j,k]
                if x1==0:
                    Wbx_Temp[i,j,k]=x2
    Wbx=b_to_c(Wbx_Temp)

# Wstxの作成
    for i in range(9):
        for j in range(9):
            for k in range(9):
                num1=0
                if Wix[i,j,k]==2:
                    num1=num1+1
                if Wjx[i,j,k]==2:
                    num1=num1+1
                if Wkx[i,j,k]==2:
                    num1=num1+1
                if Wbx[i,j,k]==2:
                    num1=num1+1
                if num1>=2:
                   Wstx[i,j,k]=num1

# Wwkxの作成
    for i in range(9):
        for j in range(9):
            for k in range(9):
                num1=0
                if Wix[i,j,k]>=2:
                    num1=num1+1
                if Wjx[i,j,k]>=2:
                    num1=num1+1
                if Wkx[i,j,k]>=2:
                    num1=num1+1
                if Wbx[i,j,k]>=2:
                    num1=num1+1
                if num1>=2:
                   Wwkx[i,j,k]=num1

    return Wix,Wjx,Wkx,Wbx,Wstx,Wwkx


# リンク先ノード候補テーブルの作成
# x3=1(強)、x3=0(弱)、i3~k3:リンク元ノード
def linktable(ctrl3,x3,i3,j3,k3,Wi3,Wj3,Wk3,Wb3,Wst3,Wwk3,Whist3):

  numix=Wi3[i3,j3,k3]
  if x3==1 and numix>2:
    numix=0
  numjx=Wj3[i3,j3,k3]
  if x3==1 and numjx>2:
    numjx=0
  numkx=Wk3[i3,j3,k3]
  if x3==1 and numkx>2:
    numkx=0
  numbx=Wb3[i3,j3,k3]
  if x3==1 and numbx>2:
    numbx=0
  numx=numix+numjx+numkx+numbx		# ノードごとの総リンク数

  patxx=np.zeros(shape=[5,numx],dtype='int')

  if numx==0:			#リンクノードなし
    pass
  else:

    cnt=0
    for ix in range(9):
      xyzi=Wi3[ix,j3,k3]
      qvri=Whist3[ix,j3,k3]

      if xyzi>0 and ix!=i3 and qvri==1:	# 行内にリンクあり＆基底ノードではない＆履歴がない

        if x3==1 and xyzi!=2:	# リンク先が強リンク指定（従ってリンク数は２）
          pass
        else:

          patxx[0,cnt]=xyzi
          patxx[1,cnt]=ix
          patxx[2,cnt]=j3
          patxx[3,cnt]=k3
          patxx[4,cnt]=3*(ix//3)+(j3//3)
          cnt=cnt+1

    for jx in range(9):
      xyzj=Wj3[i3,jx,k3]
      qvrj=Whist3[i3,jx,k3]

      if xyzj>0 and jx!=j3 and qvrj==1:

        if x3==1 and xyzj!=2:
          pass
        else:
          patxx[0,cnt]=xyzj
          patxx[1,cnt]=i3
          patxx[2,cnt]=jx
          patxx[3,cnt]=k3
          patxx[4,cnt]=3*(i3//3)+(jx//3)
          cnt=cnt+1

    for kx in range(9):
      xyzk=Wj3[i3,j3,kx]
      qvrk=Whist3[i3,j3,kx]

      if xyzk>0 and kx!=k3 and qvrk==1:

        if x3==1 and xyzk!=2:
          pass
        else:
          patxx[0,cnt]=xyzk
          patxx[1,cnt]=i3
          patxx[2,cnt]=j3
          patxx[3,cnt]=kx
          patxx[4,cnt]=3*(i3//3)+(j3//3)
          cnt=cnt+1

    for bix in range(3):
      for bjx in range(3):
        bix2=3*(i3//3)+bix
        bjx2=3*(j3//3)+bjx
        xyzb=Wb3[bix2,bjx2,k3]
        qvrb=Whist3[bix2,bjx2,k3]

        if xyzb>0 and bix2!=i3 and bjx2!=j3 and qvrb==1:
          if x3==1 and xyzb!=2:
            pass
          else:
            patxx[0,cnt]=xyzb
            patxx[1,cnt]=bix2
            patxx[2,cnt]=bjx2
            patxx[3,cnt]=k3
            patxx[4,cnt]=3*(bix2//3)+(bjx2//3)

  return numx,patxx

# リンクのサーチ
# bn=0:一つ目のノード、bn=1:二つ目のノード、xc3=何層めか
# xx3,調べる表番号、st=候補ノードのリンク先があるか（st=0:弱のリンク先、st=1:強のリンク先
def search(xx3,st3,bn3,xc3,pat3,Wchain3,Whist3,Wst3,Wwk3):

  exi=0

  i11=pat3[1,xx3]
  j11=pat3[2,xx3]
  k11=pat3[3,xx3]

  if st3==0:
    ch1=Wwk3[i11,j11,k11]
  else:
    ch1=Wst3[i11,j11,k11]

  if ch1>0:		#候補ノードのリンク先がある

    xyz=Whist3[i11,j11,k11]

    if xyz==1:
      exi=1

      Whist3[i11,j11,k11]=0  # 選択されたノードを履歴から消す

      Wchain3[bn3,0,xc3]=i11
      Wchain3[bn3,1,xc3]=j11
      Wchain3[bn3,2,xc3]=k11

  return exi,Wchain3,Whist3

# 末端２ノードの強弱チェーンの有無チェック
# return:linkx=0:リンクなし、1=弱リンク、2=強リンク
def chklnk(xc4,Wchain4,Wi4,Wj4,Wk4,Wb4,Wst4,Wwk4):

  for xxx in range(3):
    qi1=Wchain4[0,0,xc4]
    qi2=Wchain4[1,0,xc4]

    qj1=Wchain4[0,1,xc4]
    qj2=Wchain4[1,1,xc4]

    qk1=Wchain4[0,2,xc4]
    qk2=Wchain4[1,2,xc4]

    qb1=3*(qi1//3)+(qj1//3)
    qb2=3*(qi2//3)+(qj2//3)

    cnumi=Wi4[qi1,qj1,qk1]
    cnumj=Wj4[qi1,qj1,qk1]
    cnumk=Wk4[qi1,qj1,qk1]
    cnumb=Wb4[qi1,qj1,qk1]

    if qi1==qi2 and qj1==qj2:
      linkx=1
      if cnumk==2:
        linkx=2
    elif qi1==qi2 and qk1==qk2:
      linkx=1
      if cnumj==2:
        linkx=2
    elif qj1==qj2 and qk1==qk2:
      linkx=1
      if cnumi==2:
        linkx=2
    elif qb1==qb2 and qk1==qk2:
      linkx=1
      if cnumk==2:
        linkx=2
    else:
      linkx=0
        
  return linkx

# 強チェーン成立時のマスク作成
def stmask(Wchain5):

  W2=np.zeros(shape=[9,9,9],dtype='int')

  iz=Wchain5[0,0,0]
  jz=Wchain5[0,1,0]
  kz=Wchain5[0,2,0]

  for ix in range(9):
    if ix!=iz:
      W2[ix,jz,kz]=1

  return W2

# 弱チェーン成立時のマスク作成
def wkmask(Wchain6):

  W2=np.zeros(shape=[9,9,9],dtype='int')

  iz=Wchain6[0,0,0]
  jz=Wchain6[0,1,0]
  kz=Wchain6[0,2,0]

  W2[iz,jz,kz]=1

  return W2

# 強チェーンリングマスクの作成
def ChnMaskSt(ctrl2,W1):	# W1:CubeMask

  Wi,Wj,Wk,Wb,Wst,Wwk=ToolCube(W1)      # 準備作業

  for i in range(9):
    for j in range(9):
      for k in range(9):

          W2=np.zeros(shape=[9,9,9],dtype='int')	# CubeMaskTemp
          Wchain=np.zeros(shape=[2,3,10],dtype='int')	# チェーンのアドレス履歴

# Whistの作成（UFNノードの位置情報：一度チェーンが決まったノードは消していく）

          Whist=np.zeros(shape=[9,9,9],dtype='int')

          for i2 in range(9):
            for j2 in range(9):
              for k2 in range(9):
                x=W1[i2,j2,k2]
                if x==0:
                  Whist[i2,j2,k2]=1

          xc=0        # チェーン回数カウント
          closex=0    # チェーンが閉じたかどうか

          stnum0=Wst[i,j,k]
          if stnum0>0 and Whist[i,j,k]==1:        #強チェーンが二個以上あるノードが有り

            Whist[i,j,k]=0	#最初のノードが確定したので消す
            izero=i		#最初のノード位置を覚えておく
            jzero=j
            kzero=k
            bzero=3*(i//3)+(j//3)

# チェーンノードの履歴
# [0:i0,i1,i2 *********,i9]  一つ目の枝
# [0:j0,j1,j2 *********,j9]
# [0:k0,k1,k2 *********,k9]
# [1,i0,i1,i2 *********,i9]  二つ目の枝
# [1,j0,j1,j2 *********,j9]
# [1,k0,k1,k2 *********,k9]

            Wchain[0,0,0]=izero
            Wchain[0,1,0]=jzero
            Wchain[0,2,0]=kzero

# 一層目のノードを決める（強リンクの組み合わせがいくつか考えられるため）

            xc=1	# 一層目

            abc=1	# 基底ノードとのリンクが強
            cn1,pat11=linktable(ctrl2,abc,i,j,k,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)	# 一層目の候補ノードの表を作る

            if cn1<2:
              pass

            else:
            # 一層目の一つ目の強リンクノードを選ぶ
              for lay11 in range(cn1):
            
              # リンクのサーチ
              # bn=0:一つ目のノード、bn=1:二つ目のノード、xc=何層目か
              # st=候補ノードのリンク先が強か弱か。前が強なら次は弱、前が弱なら次は強

                st=0
                bn=0
                xc=1

                exist,Wchain,Whist=search(lay11,st,bn,xc,pat11,Wchain,Whist,Wst,Wwk)

                if exist==0:
                  pass

                else:
              # 一層目の二つめの強リンクノードを選ぶ
                  for lay12 in range(cn1):

                    st=0
                    bn=1
                    xc=1

                    exist,Wchain,Whist=search(lay12,st,bn,xc,pat11,Wchain,Whist,Wst,Wwk)

                    if exist==0:
                      pass

                    else:
                # 上の２ノードは弱リンクか強リンクか
                # stwk:0=リンクなし、1=弱リンク、2=強リンク

                      stwk=chklnk(xc,Wchain,Wi,Wj,Wk,Wb,Wst,Wwk)

                      if stwk==1:
                        closex=1
                        W2=stmask(Wchain)
                        #print("Wchain") #**********************
                        #print(Wchain)   #***********************

                        return closex,xc,W2,Wchain

# 二層目
                        xc=2
                        abc=0	#一層目とのリンクが弱
                
                        pat21=np.zeros(shape=[5,4],dtype='int')
                        pat22=np.zeros(shape=[5,4],dtype='int')

                        i21=Wchain[0,0,xc-1]
                        j21=Wchain[0,1,xc-1]
                        k21=Wchain[0,2,xc-1]

                        i22=Wchain[1,0,xc-1]
                        j22=Wchain[1,1,xc-1]
                        k22=Wchain[1,2,xc-1]

                        cn21,pat21=linktable(ctrl2,abc,i21,j21,k21,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)	# 二層目の一つ目の候補ノード
                        cn22,pat22=linktable(ctrl2,abc,i22,j22,k22,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)	# 二層目の一つ目の候補ノード

                        if cn21<1 or cn22<1:
                          pass
                        else:

                  # 二層目の一つ目の弱リンクノードを選ぶ

                          for lay21 in range(cn21):

                  # リンクのサーチ
                  # bn=0:一つ目のノード、bn=1:二つ目のノード、xc3=何層目か、cn3=候補ノード数
                  # st=候補ノードが強か弱か。前が強なので次は弱(0)

                            st=0
                            bn=0
                            xc=2

                            exist,Wchain,Whist=search(lay21,st,bn,xc,pat21,Wchain,Whist,Wst,Wwk)

                            if exist==0:
                              pass
                            else:

                    # 二層目の二つめの弱リンクノードを選ぶ

                              for lay22 in range(cn22):

                                st=0
                                bn=1
                                xc=2

                                exist,Wchain,Whist=search(lay22,st,bn,xc,pat22,Wchain,Whist,Wst,Wwk)

                                if exist==0:
                                  pass

                                else:

                      # 上の２ノードは弱リンクか強リンクか
                      # stwk:0=リンクなし、1=弱リンク、2=強リンク

                                  stwk=chklnk(xc,Wchain,Wi,Wj,Wk,Wb,Wst,Wwk)

                                  if stwk==2:	# 末端の２ノードが強リンク

                                    closex=1
                                    W2=stmask(Wchain)
                                    #print("Wchain") #**********************
                                    #print(Wchain)   #***********************

                                    return closex,xc,W2,Wchain

# 三層目                          else:

                                    xc=3
                                    abc=1 #二層目とのリンクが強

                                    pat31=np.zeros(shape=[5,4],dtype='int')
                                    pat32=np.zeros(shape=[5,4],dtype='int')

                                    i31=Wchain[0,0,xc-1]
                                    j31=Wchain[0,1,xc-1]
                                    k31=Wchain[0,2,xc-1]

                                    i32=Wchain[1,0,xc-1]
                                    j32=Wchain[1,1,xc-1]
                                    k32=Wchain[1,2,xc-1]

                                    cn31,pat31=linktable(ctrl2,abc,i31,j31,k31,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)       # 三層目の一つ目の候補ノード
                                    cn32,pat32=linktable(ctrl2,abc,i32,j32,k32,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)       # 三層目の一つ目の候補ノード

                                    if cn31<1 or cn32<1:
                                      pass

                                    else:
                  # 三層目の一つ目の弱リンクノードを選ぶ

                                      for lay31 in range(cn31):

                  # リンクのサーチ
                  # bn=0:一つ目のノード、bn=1:二つ目のノード、xc3=何層目か、cn3=候補ノード数
                  # st=候補ノードが強か弱か。前が強なので次は弱(0)

                                        st=0
                                        bn=0
                                        xc=3

                                        exist,Wchain,Whist=search(lay31,st,bn,xc,pat31,Wchain,Whist,Wst,Wwk)

                                        if exist==0:
                                          pass
                                        else:
                    # 三層目の二つめの弱リンクノードを選ぶ
                                          for lay32 in range(cn22):

                                            st=0
                                            bn=1
                                            xc=3

                                            exist,Wchain,Whist=search(lay32,st,bn,xc,pat32,Wchain,Whist,Wst,Wwk)

                                            #print("Wchain") #**********************
                                            #print(Wchain)   #***********************

                                            if exist==0:
                                              pass
                                            else:
                      # 上の２ノードは弱リンクか強リンクか
                      # stwk:0=リンクなし、1=弱リンク、2=強リンク

                                              stwk=chklnk(xc,Wchain,Wi,Wj,Wk,Wb,Wst,Wwk)

                                              if stwk==1:

                                                closex=1
                                                W2=stmask(Wchain)
                                                #print("Wchain")	#**********************
                                                #print(Wchain)	#***********************
                                                return closex,xc,W2,Wchain

                                              else:
                                                break

  return closex,xc,W2,Wchain

def ChnMaskWk(ctrl2,W1):

  Wi,Wj,Wk,Wb,Wst,Wwk=ToolCube(W1)      # 準備作業

  for i in range(9):
    for j in range(9):
      for k in range(9):

          W2=np.zeros(shape=[9,9,9],dtype='int')        # CubeMaskTemp
          Wchain=np.zeros(shape=[2,3,10],dtype='int')   # チェーンのアドレス履歴

# Whistの作成（UFNノードの位置情報：一度チェーンが決まったノードは消していく）

          Whist=np.zeros(shape=[9,9,9],dtype='int')

          for i2 in range(9):
            for j2 in range(9):
              for k2 in range(9):
                x=W1[i2,j2,k2]
                if x==0:
                  Whist[i2,j2,k2]=1

          xc=0        # チェーン回数カウント
          closex=0    # チェーンが閉じたかどうか

          stnum0=Wwk[i,j,k]

          if stnum0>0 and Whist[i,j,k]==1:        #強チェーンが二個以上あるノードが有り

            Whist[i,j,k]=0      #最初のノードが確定したので消す
            izero=i             #最初のノード位置を覚えておく
            jzero=j
            kzero=k
            bzero=3*(i//3)+(j//3)

# チェーンノードの履歴
# [0:i0,i1,i2 *********,i9]  一つ目の枝
# [0:j0,j1,j2 *********,j9]
# [0:k0,k1,k2 *********,k9]
# [1,i0,i1,i2 *********,i9]  二つ目の枝
# [1,j0,j1,j2 *********,j9]
# [,k0,k1,k2 *********,k9]

            Wchain[0,0,0]=izero
            Wchain[0,1,0]=jzero
            Wchain[0,2,0]=kzero

# 一層目のノードを決める（弱リンクの組み合わせがいくつか考えられるため）

            xc=1        # 一層目

            abc=0       # 基底ノードとのリンク先が弱
            cn,pat1=linktable(ctrl2,abc,i,j,k,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)      # 一層目の候補ノードの表を作る

            if cn<2:
              pass

            else:
            # 一層目の一つ目の弱リンクノードを選ぶ
              for lay11 in range(cn):

              # リンクのサーチ
              # bn=0:一つ目のノード、bn=1:二つ目のノード、xc=何層目か
              # st=候補ノードのリンク先が強か弱か。前が強なら次は弱、前が弱なら次は強

                st=1	# 二層目は強
                bn=0
                xc=1

                exist,Wchain,Whist=search(lay11,st,bn,xc,pat1,Wchain,Whist,Wst,Wwk)

                if exist==0:
                  pass

                else:
              # 一層目の二つめの弱リンクノードを選ぶ
                  for lay12 in range(cn):

                    st=1	# 二層目は強
                    bn=1
                    xc=1

                    exist,Wchain,Whist=search(lay12,st,bn,xc,pat1,Wchain,Whist,Wst,Wwk)

                    if exist==0:
                      pass

                    else:

                # 上の２ノードは弱リンクか強リンクか
                # stwk:0=リンクなし、1=弱リンク、2=強リンク

                      stwk=chklnk(xc,Wchain,Wi,Wj,Wk,Wb,Wst,Wwk)

                      if stwk==2:
                        closex=1
                        W2=wkmask(Wchain)
                        #print("Wchain=")	#*************************
                        #print(Wchain)	#****************************

                        return closex,xc,W2,Wchain

# 二層目
                      else:
                        xc=2
                        abc=1 # 一層目とのリンクが強

                        pat21=np.zeros(shape=[5,4],dtype='int')
                        pat22=np.zeros(shape=[5,4],dtype='int')

                        i21=Wchain[0,0,xc-1]
                        j21=Wchain[0,1,xc-1]
                        k21=Wchain[0,2,xc-1]

                        i22=Wchain[1,0,xc-1]
                        j22=Wchain[1,1,xc-1]
                        k22=Wchain[1,2,xc-1]

                        cn21,pat21=linktable(ctrl2,abc,i21,j21,k21,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)       # 二層目の一つ目の候補ノード
                        cn22,pat22=linktable(ctrl2,abc,i22,j22,k22,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)       # 二層目の一つ目の候補ノード

                        if cn21<1 or cn22<1:
                          pass
            
                        else:
                  # 二層目の一つ目の強リンクノードを選ぶ
                          for lay21 in range(cn21):

                  # リンクのサーチ
                  # bn=0:一つ目のノード、bn=1:二つ目のノード、xc3=何層目か、cn3=候補ノード数
                  # st=候補ノードが強か弱か。前が弱なので次は強(1)

                            st=1
                            bn=0
                            xc=2

                            exist,Wchain,Whist=search(lay21,st,bn,xc,pat21,Wchain,Whist,Wst,Wwk)

                            if exist==0:
                              pass

                            else:
                    # 二層目の二つめの強リンクノードを選ぶ
                              for lay22 in range(cn22):

                                st=1
                                bn=1
                                xc=2

                                exist,Wchain,Whist=search(lay22,st,bn,xc,pat22,Wchain,Whist,Wst,Wwk)

                                if exist==0:
                                  pass

                                else:

                      # 上の２ノードは弱リンクか強リンクか
                      # stwk:0=リンクなし、1=弱リンク、2=強リンク

                                  stwk=chklnk(xc,Wchain,Wi,Wj,Wk,Wb,Wst,Wwk)

                                  if stwk==1:       # 末端の２ノードが弱リンク

                                    closex=1
                                    W2=wkmask(Wchain)
                                    #print("Wchain=")	#**********************
                                    #print(Wchain)	#************************

                                    return closex,xc,W2,Wchain

# 三層目
                                  else:

                                    xc=3
                                    abc=0 # 二層目とのリンクが弱

                                    pat31=np.zeros(shape=[5,4],dtype='int')
                                    pat32=np.zeros(shape=[5,4],dtype='int')

                                    i31=Wchain[0,0,xc-1]
                                    j31=Wchain[0,1,xc-1]
                                    k31=Wchain[0,2,xc-1]

                                    i32=Wchain[1,0,xc-1]
                                    j32=Wchain[1,1,xc-1]
                                    k32=Wchain[1,2,xc-1]

                                    cn31,pat31=linktable(ctrl2,abc,i31,j31,k31,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)       # 三層目の一つ目の候補ノード
                                    cn32,pat32=linktable(ctrl2,abc,i32,j32,k32,Wi,Wj,Wk,Wb,Wst,Wwk,Whist)       # 三層目の一つ目の候補ノード

                                    if cn31<1 or cn32<1:
                                      pass
                                    else:

                  # 三層目の一つ目の弱リンクノードを選ぶ
                                      for lay31 in range(cn31):

                  # リンクのサーチ
                  # bn=0:一つ目のノード、bn=1:二つ目のノード、xc3=何層目か、cn3=候補ノード数
                  # st=候補ノードが強か弱か。前が弱なので次は強(1)

                                        st=1
                                        bn=0
                                        xc=3

                                        exist,Wchain,Whist=search(lay31,st,bn,xc,pat31,Wchain,Whist,Wst,Wwk)

                                        if exist==0:
                                          pass
                                        else:

                    # 三層目の二つめの弱リンクノードを選ぶ
                                          for lay32 in range(cn22):

                                            st=1
                                            bn=1
                                            xc=3

                                            exist,Wchain,Whist=search(lay32,st,bn,xc,pat32,Wchain,Whist,Wst,Wwk)

                                            if exist==0:
                                              pass

                                            else:
                      # 上の２ノードは弱リンクか強リンクか
                      # stwk:0=リンクなし、1=弱リンク、2=強リンク

                                              stwk=chklnk(xc,Wchain,Wi,Wj,Wk,Wb,Wst,Wwk)

                                              if stwk==2:

                                                closex=1
                                                W2=wkmask(Wchain)
                                                #print("Wchain=")	#****************
                                                #print(Wchain)	#*********************

                                                return closex,xc,W2,Wchain


  return closex,xc,W2,Wchain

# Wchainの三次元化
def chconv(chx,Wch):
  Wc=np.zeros(shape=[9,9,9],dtype='int')	#Wchを三次元化
  # 基幹ノード
  i0=Wch[0,0,0]
  j0=Wch[0,1,0]
  k0=Wch[0,2,0]
  Wc[i0,j0,k0]=1
  for n in range(chx):
    ix1=Wch[0,0,n+1]
    jx1=Wch[0,1,n+1]
    kx1=Wch[0,2,n+1]
    ix2=Wch[1,0,n+1]
    jx2=Wch[1,1,n+1]
    kx2=Wch[1,2,n+1]
    Wc[ix1,jx1,kx1]=1
    Wc[ix2,jx2,kx2]=1

  return Wc

#---------------------- main routine --------------------------------
# level  actual method
#   1    unidentified node
#   2    1+independence declaration
#   3    1+2+(2X2)matrix
#   4    1+2+3+(3X3)matrix
#   5    1+1+3+4+(4X4)matrix
#   6    1+2+3+4+5+(5X5)matrix
#   7    1+2+3+4+5+6+strong&week chain

def s_web_main(level,QX):

    # 初期化
    result_level=1
    Q=np.zeros(shape=[9,9],dtype='int')
    Q=QX
    Qtemp=QX
    Qtemp0=np.full(shape=[9,9],fill_value=int(0),dtype='int')

    Cube=np.full(shape=[9,9,9],fill_value=int(0),dtype='int')
    CubeMask=np.full(shape=[9,9,9],fill_value=int(0),dtype='int')
    CubeTemp=Cube
    CubeTemp0=np.full(shape=[9,9,9],fill_value=int(0),dtype='int')
    CubeMaskTemp=np.full(shape=[9,9,9],fill_value=int(0),dtype='int')
    ctrl=1	#***************for test

    # 三次元化
    dim3(Q,Cube)

    # マスク作成
    msk1(Cube,CubeMask)

    # 回答数
    x1=figcnt(Qtemp)

    message=""

    while x1<81:

        mode=" "

        # 単独不確定ノードのみマスク作成

        msk1(CubeTemp0,CubeMaskTemp)

        # 元の単独不確定ノードマスクと一時ノードマスクをマージ
        merge(CubeMask,CubeMaskTemp)

        # 初期確定ノードと一時確定ノードをマージ

        merge(CubeTemp,CubeTemp0)

        # マスク計算して新たな不確定ノードをセット
        CubeTemp0=np.full(shape=[9,9,9],fill_value=int(0),dtype='int')

        x2=msk2(CubeMask,CubeTemp0)

        CubeTemp=CubeTemp+CubeTemp0
        Qtemp0=np.full(shape=[9,9],fill_value=int(0),dtype='int')

        # 二次元に戻す

        dim2(CubeTemp,Qtemp)

        # 回答完了(x1=81)なら終了ルーチンへ

        x1=figcnt(Qtemp)

        # 次のループのための初期化
        CubeMaskTemp=np.full(shape=[9,9,9],fill_value=int(0),dtype='int')
        Qtemp0=np.full(shape=[9,9],fill_value=int(0),dtype='int')

        if x2==1:				# 単独UFNあり
            pass
        else:
            # 指定レベルが１なら終了
            if level==1:
                break
            else:
                # 指定レベルが２以上で単独不確定ノードが無い場合座席予約へ進む

                # 座席予約によるマスクを探し、あればx３＝１にする

                x3,Wcore,CubeMaskTemp=IndMask(CubeMask)

                if x3==1:	# 座席予約のマスクが追加されている
                    if result_level<2:
                        result_level=2
                    print("座席予約********")
                    message=message+" + 座席予約"

                else:
                    if level==2:	# レベル指定が座席予約までなら終了
                        break
                    else:
                        n=2

                        # n=2からn=level-1まで各パターンのマスク有無を調べる

                        while n<level:

                            print(n,"X",n,"コア","level=",level)

                            # n国同盟によるマスクを探し、あればx４＝１にする
                            mode="ALI-HR"
                            x4,Wcore,CubeMaskTemp=AliMask(n,CubeMask,mode)

                            if x4==1:	# 隠れN国同盟（列）のマスクが追加されている
                                if result_level<n+1:
                                    result_level=n+1
                                print("隠れ",n,"国同盟（列）")
                                message=message+" + 隠れ"+str(n)+"国同盟（列）"
                                print("ALI-HR")	#**********************************
                                break

                            else:

                                WX=np.zeros(shape=[9,9,9],dtype='int')
                                WY=np.zeros(shape=[9,9,9],dtype='int')
                                WX=jcw(CubeMask)				# j方向回転

                                mode="ALI_R"
                                x4,Wcore,WY=AliMask(n,WX,mode)			# N国同盟（列）マスクチェック

                                CubeMaskTemp=jccw(WY)				# CubeMaskTempの回転を戻す

                                if x4==1:					# N国同盟（列）のマスクが追加されている
                                    if result_level<n+1:
                                        result_level=n+1
                                    print(n,"国同盟（列）")
                                    message=message+" + "+str(n)+"国同盟（列）"
                                    print("ALI-R")	#**********************************
                                    break

                                else:

                                    WX=np.zeros(shape=[9,9,9],dtype='int')
                                    WY=np.zeros(shape=[9,9,9],dtype='int')
                                    WX=kcw(CubeMask)				# k方向回転

                                    mode="ALI_HL"
                                    x4,Wcore,WY=AliMask(n,WX,mode)		# 隠れN国同盟（行）マスクチェック
                                    CubeMaskTemp=kccw(WY)			# 回転を戻す

                                    if x4==1:					# 隠れN国同盟（行）のマスクが追加されている
                                        if result_level<n+1:
                                            result_level=n+1
                                        print("隠れ",n,"国同盟（行）")
                                        message=message+" + 隠れ"+str(n)+"国同盟（行）"
                                        print("ALI-HL")	#******************************
                                        break

                                    else:

                                        WX=np.zeros(shape=[9,9,9],dtype='int')
                                        WY=np.zeros(shape=[9,9,9],dtype='int')
                                        WZ=np.zeros(shape=[9,9,9],dtype='int')
                                        WX=kcw(CubeMask)                           # k方向回転

                                        WY=jcw(WX)                                 # さらにj方向回転

                                        mode="ALI_L"

                                        x4,Wcore,WZ=AliMask(n,WY,mode)                    # N国同盟（行）マスクチェック
                                        WY=jccw(WZ)                                 # 回転を戻す（一回目）
                                        CubeMaskTemp=kccw(WY)                      # 回転を戻す（二回目）

                                        if x4==1:# N国同盟（行）のマスクが追加されている
                                            if result_level<n+1:
                                                result_level=n+1
                                            print(n,"国同盟（行）")
                                            message=message+" + "+str(n)+"国同盟（行）"
                                            print("ALI-L")	#****************************
                                            break

                                        else:

                                            WX=np.zeros(shape=[9,9,9],dtype='int')
                                            WY=np.zeros(shape=[9,9,9],dtype='int')
                                            WX=c_to_b(CubeMask)			# ブロックに展開
                                            mode="ALI_HB"
                                            X4,Wcore,WY=AliMask(n,WX,mode)		# 隠れN国同盟（ブロック）マスクチェック
                                            CubeMaskTemp==b_to_c(WY)                   # ブロック化を戻す

                                            if x4==1:# 隠れN国同盟（ブロック）のマスクが追加されている
                                                if result_level<n+1:
                                                    result_level=n+1
                                                print("隠れ",n,"国同盟（ブロック）")
                                                message=message+" + 隠れ"+str(n)+"国同盟(ブロック）"
                                                print("ALI-HB")
                                                break

                                            else:

                                                WX=np.zeros(shape=[9,9,9],dtype='int')
                                                WY=np.zeros(shape=[9,9,9],dtype='int')
                                                WZ=np.zeros(shape=[9,9,9],dtype='int')
                                                WX=c_to_b(CubeMask)			# ブロックに展開
                                                WY=jcw(WX)				# j方向回転

                                                mode="ALI_B"
                                                x4,Wcore,WZ=AliMask(n,WY,mode)		# N国同盟（ブロック）マスクチェック
                                                WY=jccw(WZ)				# 回転を戻す
                                                CubeMaskTemp=b_to_c(WY)		# ブロック化を戻す

                                                if x4==1:# N国同盟（ブロック）のマスクが追加されている
                                                    if result_level<n+1:
                                                        result_level=n+1
                                                    print(n,"国同盟（ブロック）")
                                                    message=message+" + "+str(n)+"国同盟（ブロック）"
                                                    print("ALI-B")	#*********************
                                                    break

                                                else:

                                                    WX=np.zeros(shape=[9,9,9],dtype='int')
                                                    WY=np.zeros(shape=[9,9,9],dtype='int')
                                                    WX=icw(CubeMask)                           # i方向回転

                                                    mode="SQ_L"
                                                    x4,Wcore,WY=AliMask(n,WX,mode)		# 四辺形の定理（行）NXNマスクチェック
                                                    CubeMaskTemp=iccw(WY)                      # 回転を戻す

                                                    if x4==1:                                  # 四辺形の定理（行）NXNのマスクが追加されている
                                                        if result_level<n+1:
                                                            result_level=n+1
                                                        print("四辺形の定理（行）",n,"X",n)
                                                        message=message+" + "+"四辺形の定理（行）"+str(n)+"X"+str(n)
                                                        print("SQ-L")	#******************
                                                        break
                                                    else:

                                                        WX=np.zeros(shape=[9,9,9],dtype='int')
                                                        WY=np.zeros(shape=[9,9,9],dtype='int')
                                                        WZ=np.zeros(shape=[9,9,9],dtype='int')
                                                        WX=icw(CubeMask)			# i方向回転
                                                        WY=jcw(WX)				# j方向回転

                                                        mode="SQ_R"
                                                        x4,Wcore,WZ=AliMask(n,WY,mode)		# 四辺形の定理（列）NXNマスクチェック
                                                        WY=jccw(WZ)				# 回転を戻す（一回目）
                                                        CubeMaskTemp=iccw(WY)		# 回転を戻す（二回目）

                                                        if x4==1:				# 四辺形の定理（列）NXNのマスクが追加されている
                                                            if result_level<n+1:
                                                                result_level=n+1
                                                            print("四辺形の定理（列）",n,"X",n)
                                                            message=message+" + "+"四辺形の定理(列）"+str(n)+"X"+str(n)
                                                            print("SQ-R")	#***************
                                                            break
                                                        else:
                                                            n=n+1

                        #while中でマスクが見つからなかったらn=n+1実行後ここに来てwhileに戻る

                        if n==level and n!=7:
                            print("at debug-1"," n=",n,"level=",level,"mode=",mode)	#***************************************:
                            break

                    #whileの間のbreakでここに来る→何もなければ上位のwhileに戻る
                    print("n=",n,"level=",level)	#******************************
                    if n<level:	# whileの間にブレークした
                        print("n=",n,"level=",level,"mode=",mode)	#*************************************
                        #pass
                    else:
                        if level<6:
                            pass
                        else:
                            #チェーン法のマスクを検索

                            print("強リンクループによる解法")

                            CubeMaskTemp=np.zeros(shape=[9,9,9],dtype='int')

                            x5,y5,CubeMaskTemp,CubeCore=ChnMaskSt(ctrl,CubeMask)

                            if x5==1:
                                if result_level<7:
                                    result_level=7
                                print("●＝○ー○＝○ー○＝● ループ発見")
                                message=message+" + "+"強リンクループ"

                            else:
                                print("弱リンクループによる解法")

                                x6,y6,CubeMaskTemp,CubeCore=ChnMaskWk(ctrl,CubeMask)

                                if x6==1:
                                    if result_level<7:
                                        result_level=7
                                    print("●ー○＝○ー○＝○ー● ループ発見")
                                    message=message+" + "+"弱リンクループ"

                                else:
                                    break

    x1=figcnt(Qtemp)

    if x1<81:
        print("答えが見つかりません")

    #print("回答")
    #print(Qtemp)
    #print(x1)

    np.savetxt('q_answer.txt',Qtemp)

    print("終了しました")
    message="level-"+str(result_level)+message
    return x1,message,Qtemp

