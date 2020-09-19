# web version 2020.7.2
import random
import numpy as np
from sudoku_web2 import *

# fill "2" in all piers of WX2, increment all piers in WY2
def fill_mask(i2,j2,k2,WX2,WY2):

    for l in range(9):
        WX2[l,j2,k2]=2
        num=WY2[l,j2,k2]
        num=num+1
        WY2[l,j2,k2]=num
    for m in range(9):
        WX2[i2,m,k2]=2
        num=WY2[i2,m,k2]
        num=num+1
        WY2[i2,m,k2]=num
    for n in range(9):
        WX2[i2,j2,n]=2
        num=WY2[i2,j2,n]
        num=num+1
        WY2[i2,j2,n]=num
    bi=i2//3  # block line
    bj=j2//3  # block raw

    for l in range(3):
        for m in range(3):
            bi2=3*bi+l
            bj2=3*bj+m
            WX2[bi2,bj2,k2]=2
            num=WY2[bi2,bj2,k2]
            num=num+1
            WY2[bi2,bj2,k2]=num

    return WX2,WY2

# decrement "2" in all piers of WY2
def dec_mask(i3,j3,k3,WX3,WY3):
    for l in range(9):
        num=WY3[l,j3,k3]
        if num>0:
            num=num-1
            WY3[l,j3,k3]=num
            if num==0: 
                WX3[l,j3,k3]=0
    for m in range(9):
        num=WY3[i3,m,k3]
        if num>0:
            num=num-1
            WY3[i3,m,k3]=num
            if num==0:
                WX3[i3,m,k3]=0  
    for n in range(9):
        num=WY3[i3,j3,n]
        if num>0:
            num=num-1
            WY3[i3,j3,n]=num
            if num==0:
                WX3[i3,j3,n]=0  
    bi=i3//3  # block line
    bj=j3//3  # block raw

    for l in range(3):
        for m in range(3):
            bi3=3*bi+l
            bj3=3*bj+m
            num=WY3[bi3,bj3,k3]
            if num>0:
                num=num-1
                WY3[bi3,bj3,k3]=num
                if num==0:
                    WX3[bi3,bj3,k3]=0

    return WX3,WY3

# check if all cells in a pier are "2"
def check_mask(WX2):
    numx=0
    for i2 in range(9):
        for j2 in range(9):
            numk=0
            for k2 in range(9):
                x2=WX2[i2,j2,k2]
                if x2==2:
                    numk=numk+1
            if numk==9:
                numx=1
                return numx
    for i2 in range(9):
        for k2 in range(9):
            numj=0
            for j2 in range(9):
                y2=WX2[i2,j2,k2]
                if y2==2:
                    numj=numj+1
            if numj==9:
                numx=1
                return numx
    for j2 in range(9):
        for k2 in range(9):
            numi=0
            for i2 in range(9):
                z2=WX2[i2,j2,k2]
                if z2==2:
                    numi=numi+1
            if numi==9:
                numx=1
                return numx
                
    for k2 in range(9):
        for bi in range(3):
            for bj in range(3):
                numb=0
                for bi2 in range(3):
                    for bj2 in range(3):
                        b2=WX2[3*bi+bi2,3*bj+bj2,k2]
                        if b2==2:
                            numb=numb+1
                            if numb==9:
                                numx=1
                                return numx
    return numx

# count "0" cells
def cnt_num(x,WX2):
    num2=0
    for i2 in range(9):
        for j2 in range(9):
            for k2 in range(9):
                x2=WX2[i2,j2,k2]
                if x2==x:
                    num2=num2+1

    return num2
# count "0" seat for each figure(1~9)    
def count_seats(i2,j2,WX2):
    WF2i=np.zeros(shape=[9],dtype='int')
    WF2j=np.zeros(shape=[9],dtype='int')
    for k3 in range(9):
        numx2=0
        for i3 in range(9):
            x=WX2[i3,j2,k3]
            if x==0:
                numx2=numx2+1
        WF2i[k3]=numx2
        numy2=0
        for j3 in range(9):
            y=WX2[i2,j3,k3]
            if y==0:
                numy2=numy2+1
        WF2j[k3]=numy2

    return WF2i,WF2j

# generate random strings(1~0)
def gen_random():
    WR=np.zeros(shape=[9],dtype='int')
    for z1 in range(9):
        match=1
        while match==1:
            x=int(random.uniform(0,9))+1
            match=0
            for z2 in range(9):
                if WR[z2]==x:
                    match=1

        WR[z1]=x

    for z3 in range(9):
        WR[z3]=WR[z3]-1

    return WR

# check figure with minimum vacant seats
def min_check(ii2,jj2,WX2):

    # check remaining seat
    WFi2,WFj2=count_seats(ii2,jj2,WX2)

    # minimum figure check
    min=9
    for kk2 in range(9):
        if WFj2[kk2]<min and WFj2[kk2]>0:
            min=WFj2[kk2]

    # search min figure when WX2="0"
    min3=10
    flgz=0
    flg2=0

    for z1 in range(min,10):
        for z2 in range(9):
            if WX2[ii2,jj2,z2]==0 and WFj2[z2]==z1:
                min=z1
                min3=z1
                return min3,flg2,WFj2

    if min3==10:
       flg2=1

    return min3,flg2,WFj2

# fix target cell
def fix_target(i2,j2,k2,WX2,WY2):

    fill_mask(i2,j2,k2,WX2,WY2)
    WX2[i2,j2,k2]=1

    check_result=check_mask(WX2)

    if check_result==1:	# all "2" in a pier
        dec_mask(i2,j2,k2,WX2,WY2)
        WX2[i2,j2,k2]=3

    return check_result,WX2,WY2

# check more than one ufn in a pier
def check_mask2(WX2):
    flg=0
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                numk=0
                for k2 in range(9):
                    if WX2[i1,j1,k2]==0:
                        numk=numk+1
                numj=0 
                for j2 in range(9):
                    if WX2[i1,j2,k1]==0:
                        numj=numj+1
                numi=0
                for i2 in range(9):
                    if WX2[i2,j1,k1]==0:
                        numi=numi+1
                numb=0
                bi1=i1%3
                bj1=j1%3
                for bi2 in range(3):
                    for bj2 in range(3):
                        bix=3*bi1+bi2
                        bjx=3*bj1+bj2
                        if WX2[bix,bjx,k1]==0:
                            numb=numb+1

                if numi>1 and numj>1 and numk>1 and numb>1:
                    flg=1
                    return flg
    return flg

# ------------------ main1 routine ----------------------------
# generate final pattern
def s_create_main1():

    WXtemp=np.zeros(shape=[9,9,9],dtype='int')
    WYtemp=np.zeros(shape=[9,9,9],dtype='int')
    Qtemp=np.zeros(shape=[9,9],dtype='int')

    flg1=0	# all "2" cell exists
    flg2=0  	# no more "0" cell

    WRi=gen_random()
    for i2 in range(9):
        i1=WRi[i2]

        WRj=gen_random()
        for j2 in range(9):
            j1=WRj[j2]

            WRk=gen_random()
            for k2 in range(9):
                k1=WRk[k2]

                min2,flg2,WFj=min_check(i1,j1,WXtemp)
                if flg2==1:     #no vacant seat
                    return flg2,Qtemp,WXtemp,WYtemp

                x1=WXtemp[i1,j1,k1]
                y1=WFj[k1]

                if x1==0 and y1==min2:

                    flg1,WXtemp,WYtemp=fix_target(i1,j1,k1,WXtemp,WYtemp)

                    if flg1==0:
                        break
            numz=0
            for zz in range(9):
                if WXtemp[i1,j1,zz]==2 or WXtemp[i1,j1,zz]==3:
                    numz=numz+1
            if numz==9:
                flg2=1

    for ix in range(9):
        for jx in range(9):
            for kx in range(9):
                numx=WXtemp[ix,jx,kx]
                if numx==1:
                    Qtemp[ix,jx]=kx+1

    qwr=figcnt(Qtemp)
    if qwr<81:
        flg2=1
    return flg2,Qtemp,WXtemp,WYtemp

# ------------------------- main2 routine -------------------------------
# make quest pattern
def s_create_main2():

    WXt2=np.zeros(shape=[9,9,9],dtype='int')
    WYt2=np.zeros(shape=[9,9,9],dtype='int')
    Qt2=np.zeros(shape=[9,9],dtype='int')
    Qt3=np.zeros(shape=[9,9],dtype='int')

    flagz=1
    while flagz==1:

        flg=1
        while flg==1:
            flg,Qt2,WXt2,WYt2=s_create_main1()

        # final pattern found
        print("final pattern found")	#*********************************

        pnum=figcnt(Qt2)	#*******************************
        if pnum==80:		#*******************************
            return Qt2	#**************************************************

        flgx=0
        testf=0
        while flgx==0:
            print("step-1")	#****************************************
            # search Qt2>0 and Qt3==0
            flagy=0        
            while flagy==0:
            
                i0a=int(random.uniform(0,9))
                j0a=int(random.uniform(0,9))
                aaa=Qt2[i0a,j0a]
                bbb=Qt3[i0a,j0a]
                print("Qt2(>0)=",aaa,"Qt3(=0)=",bbb)	#*******************
                num1x=figcnt(Qt2)	#******************************
                num2x=figcnt(Qt3)	#*****************************
                print("num1x(Qt2)=",num1x,"num2x(Qt3)=",num2x)	#************
                xx1=num1x//2        #********************
                xx2=Qt2[4,4]        #*******************

                print("Qt2[4,4]=",xx2)	#*********************************************
                if aaa>0 and bbb==0:
                    break
            
                if num2x>num1x:	#**************************
                    return Qt2
                    #break	#************************************

                #testf=0	#************************************
                if num1x==0 and num2x==0:	#********************************
                    return Qt2	#******************************************

                #if xx1==0 and xx2>0:	#**************************
                    #testf=1	#**************************************
                    #print("xx1(0=偶数,1=奇数)",xx1,"Qt2[4,4]=",xx2)	#*****************
                    #break	#******************************************
                #else:	#****************************************
                    #testf=0	#**********************************

            #if testf==1:	#*********************************
                #break	#*********************************

            print("target position found")	#************************************

            k0a=Qt2[i0a,j0a]-1
            dec_mask(i0a,j0a,k0a,WXt2,WYt2)
            Qt2[i0a,j0a]=0

            # synmetrical position
            if i0a==4 and j0a==4:
                i0b=4
                j0b=4
                k0b=k0a
            else:
                i0b=8-i0a
                j0b=8-j0a
                k0b=Qt2[i0b,j0b]-1
                dec_mask(i0b,j0b,k0b,WXt2,WYt2)
                Qt2[i0b,j0b]=0

            print("i0a=",i0a,"j0a=",j0a,"k0a=",k0a)   #*****************
            print("i0b=",i0b,"j0b=",j0b,"k0b=",k0b)   #*****************

            flgz=check_mask2(WXt2)

            if flgz==1:
                Qt3[i0a,j0a]=1
                fill_mask(i0a,j0a,k0a,WXt2,WYt2)
                WXt2[i0a,j0a,k0a]=1
                Qt2[i0a,j0a]=k0a+1

                if i0a==4 and j0a==4:
                    pass
                else:
                    Qt3[i0b,j0b]=1
                    fill_mask(i0b,j0b,k0b,WXt2,WYt2)
                    WXt2[i0b,j0b,k0b]=1
                    Qt2[i0b,j0b]=k0b+1

            #return Qt2	#*************************************

            num1=figcnt(Qt2)
            num2=figcnt(Qt3)

            print("Qt2=",num1,"Qt3=",num2)  #*****************************

            if num1==num2:
                # Qt2を避難させる
                Qth=np.zeros(shape=[9,9],dtype='int')	#******************
                for iixx in range(9):
                    for jjxx in range(9):
                        Qth[iixx,jjxx]=Qt2[iixx,jjxx]

                level=1
                flgq,res,Qt4=s_web_main(level,Qt2)
                print("flgq=",flgq)	#************************************
                msg=""	#******************************************:
                if flgq==81:
                    flagz=0
                    msg=("step-1 OK!")	#***********************************
                    break
                else:
                    print("step-1 failed!!")
                    WXt2=np.zeros(shape=[9,9,9],dtype='int')
                    WYt2=np.zeros(shape=[9,9,9],dtype='int')
                    Qt2=np.zeros(shape=[9,9],dtype='int')
                    Qt3=np.zeros(shape=[9,9],dtype='int')


                    flg=1
                    while flg==1:
                        flg,Qt2,WXt2,WYt2=s_create_main1()

                    # final pattern found(2)
                    print("final pattern found 2")    #*********************************

                    flgx=0
                    testf=0
                    
                    #return Qt2	#****************************************
                    msg=("flgq<81 発生!")	#*************************

                    flagz=1
                    #print(msg)	#*****************************************
                    #***breakでstep-1に戻る*******************

        print("step-2")#**********************************
        print("msg=",msg)	#*************************************
        Qt2=Qth
        xyz=figcnt(Qt2)	#****************************************
        print("Qt2 when after step-2 starts",xyz)	#*******************************:
   
        flag_a=0
        Qt3=np.zeros(shape=[9,9],dtype='int')
        Qt4=np.zeros(shape=[9,9],dtype='int')
        while flag_a==0:

            flagy=0
            while flagy==0:

                i0a=int(random.uniform(0,9))
                j0a=int(random.uniform(0,9))
                aaa=Qt2[i0a,j0a]
                bbb=Qt3[i0a,j0a]
                if aaa>0 and bbb==0:
                    flagy=1

            print("target position found-2")	#*************************

            k0a=Qt2[i0a,j0a]-1
            dec_mask(i0a,j0a,k0a,WXt2,WYt2)
            Qt2[i0a,j0a]=0

            # synmetrical position
            if i0a==4 and j0a==4:
                i0b=4
                j0b=4
                k0b=k0a
            else:
                i0b=8-i0a
                j0b=8-j0a
                k0b=Qt2[i0b,j0b]-1
                dec_mask(i0b,j0b,k0b,WXt2,WYt2)
                Qt2[i0b,j0b]=0

            print("i0a=",i0a,"j0a=",j0a,"k0a=",k0a)   #*****************
            print("i0b=",i0b,"j0b=",j0b,"k0b=",k0b)   #*****************


            qnum1=figcnt(Qt2)	#**********************
            print("Qt2 before=",qnum1)	#************************
            Qtx=np.zeros(shape=[9,9],dtype='int')
            for iii in range(9):
                for jjj in range(9):
                    Qtx[iii,jjj]=Qt2[iii,jjj]
            level=4
            flgq,res,Qt4=s_web_main(level,Qtx)
        
 
            qnum2=figcnt(Qt2)			#***************************
            qnum3=figcnt(Qt4)			#***************************** 
            print("flgq=",flgq,"Qt2_before=",qnum1,"Qt2_after=",qnum2,"Qt4=",qnum3)	#****************************

            if flgq<81:
                Qt3[i0a,j0a]=1
                fill_mask(i0a,j0a,k0a,WXt2,WYt2)
                WXt2[i0a,j0a,k0a]=1
                Qt2[i0a,j0a]=k0a+1

                if i0a==4 and j0a==4:
                    pass
                else:
                    Qt3[i0b,j0b]=1
                    fill_mask(i0b,j0b,k0b,WXt2,WYt2)
                    WXt2[i0b,j0b,k0b]=1
                    Qt2[i0b,j0b]=k0b+1




            num1=figcnt(Qt2)
            num2=figcnt(Qt3)
            num3=figcnt(Qt4)
            #print("Qt2=",num1,"Qt3=",num2,"Qt4=",num3)  #*****************************
            if num1==num2:
                flag_a=1
                msg=msg+" step-2 OK!"	#**********************************
                break

    # Qt2を避難させる
    Qth=np.zeros(shape=[9,9],dtype='int')   #******************
    for iixx in range(9):
        for jjxx in range(9):
            Qth[iixx,jjxx]=Qt2[iixx,jjxx]

    level=4
    flgq,res,Qt4=s_web_main(level,Qt2)

    Qt2=Qth
    qnum=figcnt(Qt2)

    #print("WXt2")        #***********************************
    #print(WXt2)          #**********************************
    #print("WYt2")        #**********************************
    #print(WYt2)          #**********************************
    #print("i0a=",i0a,"j0a=",j0a,"k0a=",k0a)   #*****************
    #print("i0b=",i0b,"j0b=",j0b,"k0b=",k0b)   #*****************
    #print("Qt2",qnum)         #**********************************
    #print(Qt2)           #**********************************
    #print(msg)	#*********************



    return Qt2,Qt4,res	# Qt2:問題 Qt4:答え res:難易度レベル(冒頭コメント参照)
