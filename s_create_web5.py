# web version 2020.7.2
# update s_create_web3  2020.11.1
# another version  2020.11.16
# add getFinal() 2020.12.01
# update s_create_web4 2020.12.12
# update s_create_web4b 2020.12.20
# update s_create_web4c 2020.12.25
# update s_create_web4d3 2020.12.31
# update s_create_web4d4 2021.1.4
# update s_create_web4d5 2021.1.5
# update s_create_web4d7 2021.1.12 link max method
# update s_create_web4d8 2021.1.17 add getBase()
# update s_create_web4d9 2021.1.18 total review
# web4d10 update 2021.1.20   add getMini
# web4d11 update 2021.1.21   improve
# web4d12 update 2021.1.22   change main flow
# web4d13 update 2021.2.23   speed up by link simulation
# web4d15 update 2021.3.2    improve getSeed
# web4d16 update 2021.3.3    focus to one pattern in level-3 or higher
# web4d17 update 2021.3.5    modify sun_check with Winhi again
# web4d18 update 2021.3.8    improve scan ratio
# web4d19 update 2021.3.17   change print message from Japanese to English 

import datetime
import random
import numpy as np
from sudoku_web4 import *

# generate core related face and cubes/IND(seat reservation)
#    fnum2	core face number
#    cdir2	core direction(0=holizontal,1=vertical
#    cblk21	core block number(0~8)
#    cblk22	core number in core block(0~2)
#    fbk2	flag block to i/j(0) or i/j to block(1)

def core_gen_ind(fnum2,cdir2,cblk21,cblk22,fbk2):

    Wcore2=np.zeros(shape=[9,9,9],dtype='int')   # core nodes
    Wmask2=np.zeros(shape=[9,9,9],dtype='int')   # mask nodes related to core nodes
    Wtarg2=np.zeros(shape=[9,9,9],dtype='int')   # target nodes related to core nodes
    Cface2=np.zeros(shape=[9,9],dtype='int')	# core face

# generate Wcore2

    bi1=cblk21//3
    bj1=cblk21%3

    if cdir2==0:
        Wcore2[3*bi1+cblk22,3*bj1,fnum2]=1
        Wcore2[3*bi1+cblk22,3*bj1+1,fnum2]=1
        Wcore2[3*bi1+cblk22,3*bj1+2,fnum2]=1

        Cface2[3*bi1+cblk22,3*bj1]=1
        Cface2[3*bi1+cblk22,3*bj1+1]=1
        Cface2[3*bi1+cblk22,3*bj1+2]=1

    if cdir2==1:
        Wcore2[3*bi1,3*bj1+cblk22,fnum2]=1
        Wcore2[3*bi1+1,3*bj1+cblk22,fnum2]=1
        Wcore2[3*bi1+2,3*bj1+cblk22,fnum2]=1

        Cface2[3*bi1,3*bj1+cblk22]=1
        Cface2[3*bi1+1,3*bj1+cblk22]=1
        Cface2[3*bi1+2,3*bj1+cblk22]=1

# generate Wmask2

    if fbk2==0:
       for bi2 in range(3):
           for bj2 in range(3):
               if Wcore2[3*bi1+bi2,3*bj1+bj2,fnum2]==0:
                    Wmask2[3*bi1+bi2,3*bj1+bj2,fnum2]=1

    if fbk2==1 and cdir2==0:
        for j1 in range(9):
            if Wcore2[3*bi1+cblk22,j1,fnum2]==0:
                Wmask2[3*bi1+cblk22,j1,fnum2]=1

    if fbk2==1 and cdir2==1:
        for i1 in range(9):
            if Wcore2[i1,3*bj1+cblk22,fnum2]==0:
                Wmask2[i1,3*bj1+cblk22,fnum2]=1

# generate Wtarg2

    if fbk2==0 and cdir2==0:
        for j1 in range(9):
            if Wcore2[3*bi1+cblk22,j1,fnum2]==0:
                Wtarg2[3*bi1+cblk22,j1,fnum2]=1

    if fbk2==0 and cdir2==1:
        for i1 in range(9):
            if Wcore2[i1,3*bj1+cblk22,fnum2]==0:
                Wtarg2[i1,3*bj1+cblk22,fnum2]=1

    if fbk2==1:
       for bi2 in range(3):
           for bj2 in range(3):
               if Wcore2[3*bi1+bi2,3*bj1+bj2,fnum2]==0:
                   Wtarg2[3*bi1+bi2,3*bj1+bj2,fnum2]=1

    return Cface2,Wcore2,Wmask2,Wtarg2


# generate core related face and cubes/NXN(square)
    # matn2	matrix number for NXN type
    # fpos2	face=i/j(0=i/j,1=i/k,2=j/k,3=b/k)
    # fnum2	face number(0~8)
    # mdir2	mask direction(0=holizontal,1=vertical)

def core_gen_sq(matn2,fpos2,fnum2,mdir2):

    Wcore2=np.zeros(shape=[9,9,9],dtype='int')   # core nodes
    Wmask2=np.zeros(shape=[9,9,9],dtype='int')   # mask nodes related to core nodes
    Wtarg2=np.zeros(shape=[9,9,9],dtype='int')   # target nodes related to core nodes
    Cface2=np.zeros(shape=[9,9],dtype='int')     # core nodes in core face
    Cmask2=np.zeros(shape=[9,9],dtype='int')     # mask nodes in core face
    Ctarg2=np.zeros(shape=[9,9],dtype='int')     # target nodes in core face
    Hsum2=np.zeros(shape=[9],dtype='int')	 # holizontal direction sum of core
    Vsum2=np.zeros(shape=[9],dtype='int')        # vertical direction sum of core

# generate Cface2
    if fpos2==0 and matn2>2:	# for i/j face
        evod=matn2%2	# 1=even  0=odd
        hf=matn2//2
        if evod==1:
            Hsum2[4]=1
            Vsum2[4]=1
        
        # add holozontal direction
        xyz1=0
        while xyz1<hf:
            x1=random.randint(0,3)
            Hsum2[x1]=1
            Hsum2[8-x1]=1
            xyz1=0
            for y1 in range(4):
                if Hsum2[y1]==1:
                    xyz1=xyz1+1

        # add vertical direction
        xyz1=0
        while xyz1<hf:
            x1=random.randint(0,3)
            Vsum2[x1]=1
            Vsum2[8-x1]=1
            xyz1=0
            for y1 in range(4):
                if Vsum2[y1]==1:
                    xyz1=xyz1+1

    else:
        # add holizontal direction
        xyz1=0
        while xyz1<matn2:
            x1=random.randint(0,8)
            Hsum2[x1]=1
            xyz1=0
            for y1 in range(9):
                if Hsum2[y1]==1:
                    xyz1=xyz1+1

        # add vertical position
        xyz1=0    
        while xyz1<matn2:
            x1=random.randint(0,8)
            Vsum2[x1]=1
            xyz1=0
            for y1 in range(9):
                if Vsum2[y1]==1:
                    xyz1=xyz1+1

    # make Cface2
    for i1 in range(9):
        for j1 in range(9):
            xyz2=Vsum2[i1]
            xyz3=Hsum2[j1]
            if xyz2==1 and xyz3==1:
                Cface2[i1,j1]=1

# genarate Cmask2
    if mdir2==0:                # target direction is vertical/apply holizontal direction mask
        for i1 in range(9):
            if Vsum2[i1]>0:
                for j1 in range(9):
                    if Cface2[i1,j1]==0:
                        Cmask2[i1,j1]=1
    if mdir2==1:                # target direction is holizontal/apply vertical direction Hmask
        for j1 in range(9):
            if Hsum2[j1]>0:
                for i1 in range(9):
                    if Cface2[i1,j1]==0:
                        Cmask2[i1,j1]=1

# genarate Ctarg2           
    if mdir2==0:                # vertical target
        for j1 in range(9):
            if Hsum2[j1]>0:
                for i1 in range(9):
                    if Cface2[i1,j1]==0:
                        Ctarg2[i1,j1]=1

    if mdir2==1:                # holizontal target
        for i1 in range(9):
            if Vsum2[i1]>0:
                for j1 in range(9):
                    if Cface2[i1,j1]==0:
                        Ctarg2[i1,j1]=1

# generate Wcore2 and Wmask2
    if fpos2==0:	# i/j face
        for i1 in range(9):
            for j1 in range(9):
                Wcore2[i1,j1,fnum2]=Cface2[i1,j1]
                Wmask2[i1,j1,fnum2]=Cmask2[i1,j1]
                Wtarg2[i1,j1,fnum2]=Ctarg2[i1,j1]
    if fpos2==1:	# i/k face
        for i1 in range(9):
            for k1 in range(9):
                Wcore2[i1,fnum2,k1]=Cface2[i1,k1]
                Wmask2[i1,fnum2,k1]=Cmask2[i1,k1]
                Wtarg2[i1,fnum2,k1]=Ctarg2[i1,k1]
    if fpos2==2:	# j/k face
        for j1 in range(9):
            for k1 in range(9):
                Wcore2[fnum2,j1,k1]=Cface2[j1,k1]
                Wmask2[fnum2,j1,k1]=Cmask2[j1,k1]
                Wtarg2[fnum2,j1,k1]=Ctarg2[j1,k1]

    if fpos2==3:	# b/k face
        bi1=fnum2//3
        bj1=fnum2%3
        for bi2 in range(3):
            for bj2 in range(3):
                for k1 in range(9):
                    Wcore2[3*bi1+bi2,3*bj1+bj2,k1]=Cface2[bi2+3*bj2,k1]
                    Wmask2[3*bi1+bi2,3*bj1+bj2,k1]=Cmask2[bi2+3*bj2,k1]
                    Wtarg2[3*bi1+bi2,3*bj1+bj2,k1]=Ctarg2[bi2+3*bj2,k1]

    return Cface2,Wcore2,Wmask2,Wtarg2

# generate Wlink2
def link_gen(Wcore2,Wmask2):

    Wlink2=np.zeros(shape=[9,9,9],dtype='int')   # link table for mask nodes

    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=Wmask2[i1,j1,k1]
                xyz2=Wcore2[i1,j1,k1]
                if xyz1==1 and xyz2==0:	# masks which should be False
                    for i2 in range(9):
                        xyz4=Wmask2[i2,j1,k1]
                        if xyz4==1:
                            pass
                        else:
                            xyz3=Wlink2[i2,j1,k1]
                            xyz3=xyz3+1
                            Wlink2[i2,j1,k1]=xyz3
                    for j2 in range(9):
                        xyz4=Wmask2[i1,j2,k1]
                        if xyz4==1:
                            pass
                        else:
                            xyz3=Wlink2[i1,j2,k1]
                            xyz3=xyz3+1
                            Wlink2[i1,j2,k1]=xyz3
                    for k2 in range(9):
                        xyz4=Wmask2[i1,j1,k2]
                        if xyz4==1:
                            pass
                        else:
                            xyz3=Wlink2[i1,j1,k2]
                            xyz3=xyz3+1
                            Wlink2[i1,j1,k2]=xyz3
                    bi1=i1//3
                    bj1=j1//3
                    for bi2 in range(3):
                        for bj2 in range(3):
                            xyz4=Wmask2[3*bi1+bi2,3*bj1+bj2,k1]
                            if xyz4==1:
                                pass
                            else:
                                xyz3=Wlink2[3*bi1+bi2,3*bj1+bj2,k1]
                                xyz3=xyz3+1
                                Wlink2[3*bi1+bi2,3*bj1+bj2,k1]=xyz3

    return Wlink2

# generate Winhi2
def inhi_gen(Wcore2,Wmask2,Wtarg2):

    Winhi2=np.zeros(shape=[9,9,9],dtype='int')   # nodes in which True is inhibited
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=Wcore2[i1,j1,k1]
                xyz2=Wmask2[i1,j1,k1]
                xyz3=Wtarg2[i1,j1,k1]
                if xyz1==1 or xyz2==1 or xyz3==1:
                    # same peers in a same face as core nodes
                    Winhi2[i1,j1,k1]=1
                if xyz1==1:
                    # symmetrical position
                    i2=8-i1
                    j2=8-j1
                    for k2 in range(9):
                        Winhi2[i2,j2,k2]=1

    return Winhi2

# check core condition
def core_check(lvl2,CondTable2,Cface2,Wcore2,Wfalse2):

    fnum2=CondTable2[0]
    cdir2=CondTable2[1]
    cblk12=CondTable2[2]
    cblk22=CondTable2[3]
    fbk2=CondTable2[4]
    matn2=CondTable2[5]
    fpos2=CondTable2[6]
    mdir2=CondTable2[7]

    if lvl2==2:			# seat reservation type
        chk=1			# core situation(1=OK,0=NG)
        bi1=cblk12//3
        bj1=cblk12%3
        if cdir2==0:
            xyz1=0				# core nodes count
            for j1 in range(3):
                xyz2=Wfalse2[3*bi1+cblk22,3*bj1+j1,fnum2]
                xyz1=xyz1+xyz2
        if cdir2==1:
            xyz1=0 
            for i1 in range(3):
                xyz2=Wfalse2[3*bi1+i1,3*bj1+cblk22,fnum2]
                xyz1=xyz1+xyz2
        if xyz1<2:
            chk=0

    if lvl2>2:                 # NXN type
        Cface_false=np.zeros(shape=[9,9],dtype='int')
        chk=1                   # core situation(1=OK,0=NG)
        if fpos2==0:	# face i/j
            for i1 in range(9):
                for j1 in range(9):
                    Cface_false[i1,j1]=Wfalse2[i1,j1,fnum2]

        if fpos2==1:	# face i/k
            for j1 in range(9):
                for k1 in range(9):
                    Cface_false[j1,k1]=Wfalse2[fnum2,j1,k1]

        if fpos2==2:    # face j/k
            for i1 in range(9):
                for k1 in range(9):
                    Cface_false[i1,k1]=Wfalse2[i1,fnum2,k1]

        if fpos2==3:    # face b/k
            bi1=fnum2//3
            bj1=fnum2%3
            for bi2 in range(3):
                for bj2 in range(3):
                    for k1 in range(9):
                        Cface_false[3*bi2+bj2,k1]=Wfalse2[3*bi1+bi2,3*bj1+bj2,k1]

# compare Cface2 and Cface_false

        # holozontal direction check
        for i1 in range(9):
            xyz1=0
            for j1 in range(9):
                xyz2=Cface_false[i1,j1]
                xyz3=Cface2[i1,j1]
                if xyz2==1 and xyz3==1:
                    xyz1=xyz1+1
            if xyz1<2:
                chk=0
        # vertical direction
        for j1 in range(9):
            xyz1=0
            for i1 in range(9):
                xyz2=Cface_false[i1,j1]
                xyz3=Cface2[i1,j1]
                if xyz2==1 and xyz3==1:
                    xyz1=xyz1+1
            if xyz1<2:
                chk=0

    return chk

# sequential table of Wlink for seeding
def link_table_gen(Wlink2):
    LinkTable2=np.zeros(shape=[4,729],dtype='int')
    ptr2=0
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=Wlink2[i1,j1,k1]
                if xyz1>0:
                    LinkTable2[0,ptr2]=i1
                    LinkTable2[1,ptr2]=j1
                    LinkTable2[2,ptr2]=k1
                    LinkTable2[3,ptr2]=xyz1
                    ptr2=ptr2+1

    return ptr2,LinkTable2

# sequential table for final making
def final_table_gen(Wtrue2,Wfalse2,Winhi2):
    FinalTable=np.zeros(shape=[3,729],dtype='int')
    ptr3=0
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=Wtrue2[i1,j1,k1]
                xyz2=Wfalse2[i1,j1,k1]
                xyz3=Winhi2[i1,j1,k1]
                if xyz1==0 and xyz2==0 and xyz3==0:

                    FinalTable[0,ptr3]=i1
                    FinalTable[1,ptr3]=j1
                    FinalTable[2,ptr3]=k1

                    ptr3=ptr3+1

    return ptr3,FinalTable

# save CubeMask
def csave(W1):
    W2=np.zeros(shape=[9,9,9],dtype='int')   # cube for save
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                W2[i1,j1,k1]=W1[i1,j1,k1]
    return W2

# generate false nodes
def false_gen(ix1,jx1,kx1,W1):
    for i1 in range(9):
        if i1==ix1:
            pass
        else:
            W1[i1,jx1,kx1]=1
    for j1 in range(9):
        if j1==jx1:
            pass
        else:
            W1[ix1,j1,kx1]=1
    for k1 in range(9):
        if k1==kx1:
            pass
        else:
            W1[ix1,jx1,k1]=1
    bi1=ix1//3
    bi2=ix1%3
    bj1=jx1//3
    bj2=jx1%3
    for bi3 in range(3):
        for bj3 in range(3):
            if bi2==bi3 and bj2==bj3:
                pass
            else:
                W1[3*bi1+bi3,3*bj1+bj3,kx1]=1 
                    
    return W1

# check whether all necessary nodes for seeding are masked
def mask_check(Wmask2,Wcore2,Wfalse2):
    xyz1=np.sum(Wmask2)
    #xyz2=np.sum(Wcore2)
    chk=0
    fmask=0
    for i2 in range(9):
        for j2 in range(9):
            for k2 in range(9):
                xyz4=Wmask2[i2,j2,k2]
                #xyz5=Wcore2[i2,j2,k2]
                xyz6=Wfalse2[i2,j2,k2]
                if xyz4==1 and xyz6==1:
                    fmask=fmask+1
    if fmask==xyz1:
        chk=1

    return chk,fmask

# check all peers (no peer of 9 false nodes)
def peer_check(W1):
    flag1=0
    for i1 in range(9):
        for j1 in range(9):
            xyz1=0
            for k1 in range(9):
                xyz1=xyz1+W1[i1,j1,k1]
            if xyz1==9:
                flag1=1
                return flag1
    for k1 in range(9):
        for i1 in range(9):
            xyz2=0
            for j1 in range(9):
                xyz2=xyz2+W1[i1,j1,k1]
            if xyz2==9:
                flag1=1
                return flag1
     
    for j1 in range(9):
        for k1 in range(9):
            xyz3=0
            for i1 in range(9):
                xyz3=xyz3+W1[i1,j1,k1]
            if xyz3==9:
                flag1=1
                return flag1

    for k1 in range(9):
        for bi1 in range(3):
            for bj1 in range(3):
                xyz4=0
                for bi2 in range(3):
                    for bj2 in range(3):
                        xyz4=xyz4+W1[3*bi1+bi2,3*bj1+bj2,k1]
                if xyz4==9:
                    flag1=1
                    return flag1

    return flag1 
        
# sort Link_Table
def link_table_sort(pt2,W1):
    W2=np.zeros(shape=[4,pt2],dtype='int')
    W3=np.zeros(shape=[4,pt2],dtype='int')
    # seerch max link
    lmax=0
    for x in range(729):
        xyz=W1[3,x]
        if xyz>lmax:
            lmax=xyz

    # delete "0" 
    ctr=0
    for x in range(729):
        xyz=W1[3,x]
        if xyz>0:
            W2[0,ctr]=W1[0,x]
            W2[1,ctr]=W1[1,x]
            W2[2,ctr]=W1[2,x]
            W2[3,ctr]=W1[3,x]
            ctr=ctr+1

    # sort per link number
    ctr2=0
    ctr3=lmax
    while ctr3>0:
        lhist=np.zeros(shape=[pt2],dtype='int')
        lhsum=np.sum(lhist)
        while lhsum<pt2:
            xyz3=random.randint(0,pt2-1)
            xyz4=W2[3,xyz3]
            xyz5=lhist[xyz3]
            lhist[xyz3]=1
            if xyz4==ctr3 and xyz5==0:
                W3[0,ctr2]=W2[0,xyz3]
                W3[1,ctr2]=W2[1,xyz3]
                W3[2,ctr2]=W2[2,xyz3]
                W3[3,ctr2]=W2[3,xyz3]
                ctr2=ctr2+1
            lhsum=np.sum(lhist)

        ctr3=ctr3-1

    return lmax,W3

# check target mask exists
def targ_check(Wtarg2,Wcore2,Wfalse2,Wtrue2):
    targcnt=0
    TargTable2=np.zeros(shape=[3,20],dtype='int')
    Wtargpair2=np.zeros(shape=[9,9,9],dtype='int')

    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=Wtarg2[i1,j1,k1]
                #xyz2=Wcore2[i1,j1,k1]
                xyz3=Wfalse2[i1,j1,k1]
                xyz4=Wtrue2[i1,j1,k1]
                if xyz1==1 and xyz3==0 and xyz4==0:
                    TargTable2[0,targcnt]=i1
                    TargTable2[1,targcnt]=j1
                    TargTable2[2,targcnt]=k1
                    targcnt=targcnt+1

    # check pair nodes of target nodes exist
    for ptr_targ in range(targcnt):
        ix=TargTable2[0,ptr_targ]
        jx=TargTable2[1,ptr_targ]
        kx=TargTable2[2,ptr_targ]
        cnti=0
        for ix2 in range(9):
            xyz5=Wfalse2[ix2,jx,kx]
            xyz6=Wcore2[ix2,jx,kx]
            xyz7=Wtarg2[ix2,jx,kx]
            if xyz5==0 and xyz6==0 and xyz7==0:
                cnti=cnti+1
                Wtargpair2[ix2,jx,kx]=1
        #if cnti>1:
            #return targcnt,TargTable2

        cntj=0
        for jx2 in range(9):
            xyz5=Wfalse2[ix,jx2,kx]
            xyz6=Wcore2[ix,jx2,kx]
            xyz7=Wtarg2[ix,jx2,kx]
            if xyz5==0 and xyz6==0 and xyz7==0:
                cntj=cntj+1
                Wtargpair2[ix,jx2,kx]=1
        #if cntj>1:
            #return targcnt,TargTable2

        cntk=0
        for kx2 in range(9):
            xyz5=Wfalse2[ix,jx,kx2]
            xyz6=Wcore2[ix,jx,kx2]
            xyz7=Wtarg2[ix,jx,kx2]
            if xyz5==0 and xyz6==0 and xyz7==0:
                cntk=cntk+1
                Wtargpair2[ix,jx,kx2]
        #if cntk>1:
            #return targcnt,TargTable2

        cntb=0
        bi1=i1//3
        bj1=j1//3
        for bi2 in range(3):
            for bj2 in range(3):
                xyz5=Wfalse2[3*bi1+bi2,3*bj1+bj2,kx]
                xyz6=Wcore2[3*bi1+bi2,3*bj1+bj2,kx]
                xyz7=Wtarg2[3*bi1+bi2,3*bj1+bj2,kx]
                if xyz5==0 and xyz6==0 and xyz7==0:
                    cntb=cntb+1
                    Wtargpair2[3*bi1+bi2,3*bj1+bj2,kx]=1

        #if cntb>1:
            #return targcnt,TargTable2

    targpaircnt=np.sum(Wtargpair2) 

    return targcnt,TargTable2,targpaircnt,Wtargpair2

# check UFN(SUN) and Winhi
def ufn_check(Winhi2,Wfalse2,Wtrue2):
    flg_ufn2=0
    Wsun2=np.zeros(shape=[9,9,9],dtype='int')
    # step-1 SUN check with Winhi
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=Wfalse2[i1,j1,k1]
                xyz2=Wtrue2[i1,j1,k1]
                # check this node is UFN and SUN
                if xyz1==0 and xyz2==0:
                    cnti=0
                    for i2 in range(9):
                        xyz2=Wfalse2[i2,j1,k1]
                        if xyz2==0:
                            cnti=cnti+1
                    cntj=0
                    for j2 in range(9):
                        xyz3=Wfalse2[i1,j2,k1]
                        if xyz3==0:
                            cntj=cntj+1
                    cntk=0
                    for k2 in range(9):
                        xyz4=Wfalse2[i1,j1,k2]
                        if xyz4==0:
                            cntk=cntk+1
                    cntb=0
                    bi1=i1//3
                    bj1=j1//3
                    for bi2 in range(3):
                        for bj2 in range(3):
                            xyz5=Wfalse2[3*bi1+bi2,3*bj1+bj2,k1]
                            if xyz5==0:
                                cntb=cntb+1
                    if cnti==1 or cntj==1 or cntk==1 or cntb==1:	#this UFN is SUN
                        Wsun2[i1,j1,k1]=1
                        if Winhi2[i1,j1,k1]==1:
                            flg_ufn2=1
                            return flg_ufn2,Wsun2

    # conflict check of Wsun
    flg_ufn2=0
    for i1 in range(9):
        for j1 in range(9):
            cntk=0
            for k1 in range(9):
                if Wsun2[i1,j1,k1]==1:
                    cntk=cntk+1
            if cntk>1:
                flg_ufn=1
                return flg_ufn2,Wsun2

    for j1 in range(9):
        for k1 in range(9):
            cnti=0
            for i1 in range(9):
                if Wsun2[i1,j1,k1]==1:
                    cnti=cnti+1
            if cnti>1:
                flg_ufn2=1
                return flg_ufn2,Wsun2

    for k1 in range(9):
        for i1 in range(9):
            cntj=0
            for j1 in range(9):
                if Wsun2[i1,j1,k1]==1:
                    cntj=cntj+1
            if cntj>1:
                flg_ufn2=1
                return flg_ufn2,Wsun2

    for k1 in range(9):
        for bi1 in range(3):
            for bj1 in range(3):
                cntb=0
                for bi2 in range(3):
                    for bj2 in range(3):
                        if Wsun2[3*bi1+bi2,3*bj1+bj2,k1]==1:
                            cntb=cntb+1
                if cntb>1:
                    flg_ufn2=1
                    return flg_ufn2,Wsun2

    return flg_ufn2,Wsun2

# SUN link check
def sun_check(lvl2,Wsun2,Wfalse2,Wtrue2,Winhi2):
    Wsunx=np.zeros(shape=[9,9,9],dtype='int')
    Wfalsex=np.zeros(shape=[9,9,9],dtype='int')
    Wtruex=np.zeros(shape=[9,9,9],dtype='int')
    Wfalsex=csave(Wfalse2)
    Wtruex=csave(Wtrue2)

    f_rpt=1
    while f_rpt>0:

        flg4,Wsunx=ufn_check(Winhi2,Wfalsex,Wtruex)
        sunctr=np.sum(Wsunx)
        flg_inhi=0

        if sunctr==0:
            pass
        else:
            while sunctr>0:
                for i1 in range(9):
                    for j1 in range(9):
                        for k1 in range(9):
                            xyz1=Wsunx[i1,j1,k1]
                            xyz2=Winhi2[i1,j1,k1]
                            if xyz1==1 and xyz2==1:
                                flg_inhi=1
                                return flg_inhi,Wfalsex,Wtruex,Wsunx

                            elif xyz1==1 and xyz2==0:
                                Wtruex[i1,j1,k1]=1
                                Wfalsex=false_gen(i1,j1,k1,Wfalsex)
                                flg4,Wsunx=ufn_check(Winhi2,Wfalsex,Wtruex)
                                sunctr=np.sum(Wsunx)
                            else:
                                pass

        if lvl2<2:
            break
        else:
            x_ind,Wcore3,Wtemp3=IndMask(Wfalsex)      # Wtemp3=CubeMaskTemp
            #print("x_ind=",x_ind)	#*************************************
            if x_ind==1:            # seat reservation exists
                W4=merge(Wtemp3,Wfalsex)
                Wfalsex=csave(W4)
            else:
                if lvl2<3:
                    break
                else:   # in case lvl2>=3
                    mode="sun check"
                    fmask=0
                    for cn in range(2,lvl2):
                        # ALI-HR
                        x_ali,Wcore3,Wtemp3=AliMask(cn,Wfalsex,mode)
                        #print("ALI-HR/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W4=merge(Wtemp3,Wfalsex)
                            Wfalsex=csave(W4)
                        # ALI-R
                        W4=jcw(Wfalsex)
                        x_ali,Wcore3,Wtemp3=AliMask(cn,W4,mode)
                        #print("ALI-R/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W5=jccw(Wtemp3)
                            W6=merge(W5,Wfalsex)
                            Wfalsex=csave(W6)
                        # ALI-HL
                        W4=kcw(Wfalsex)
                        x_ali,Wcore3,Wtemp3=AliMask(cn,W4,mode)
                        #print("ALI-HL/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W5=kccw(Wtemp3)
                            W6=merge(W5,Wfalsex)
                            Wfalsex=csave(W6)
                        # ALI-L
                        W4=kcw(Wfalsex)
                        W5=jcw(W4)
                        x_ali,Wcore3,Wtemp3=AliMask(cn,W5,mode)
                        #print("ALI-L/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W6=jccw(Wtemp3)
                            W7=kccw(W6)
                            W8=merge(W7,Wfalsex)
                            Wfalsex=csave(W8)
                        # ALI-HB
                        W4=c_to_b(Wfalsex)
                        x_ali,Wcore3,Wtemp3=AliMask(cn,W4,mode)
                        #print("ALI-HB/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W5=b_to_c(Wtemp3)
                            W6=merge(W5,Wfalsex)
                            Wfalsex=csave(W6)
                        # ALI-B
                        W4=c_to_b(Wfalsex)
                        W5=jcw(W4)
                        x_ali,Wcore3,Wtemp3=AliMask(cn,W5,mode)
                        #print("ALI-B/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W6=jccw(Wtemp3)
                            W7=b_to_c(W6)
                            W8=merge(W7,Wfalsex)
                            Wfalsex=csave(W8)
                        # SQ-L
                        W4=icw(Wfalsex)
                        x_ali,Wcore3,Wtemp3=AliMask(cn,W4,mode)
                        #print("SQ-L/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W5=iccw(Wtemp3)
                            W6=merge(W5,Wfalsex)
                            Wfalsex=csave(W6)
                        # SQ-R
                        W4=icw(Wfalsex)
                        W5=jcw(W4)
                        x_ali,Wcore,Wtemp=AliMask(cn,W5,mode)
                        #print("SQ-R/x_ali=",x_ali)   #**********************
                        if x_ali==1:
                            fmask=1
                            W6=jccw(Wtemp)
                            W7=iccw(W6)
                            W8=merge(W7,Wfalsex)
                            Wfalsex=csave(W8)
                    # cn loop end
                    if fmask==0:
                        break

            #return to while loop
 
    return flg_inhi,Wfalsex,Wtruex,Wsunx

# 3-dimension to 2-dimension
def three_to_two(W1):
    Q1=np.zeros(shape=[9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz=W1[i1,j1,k1]
                if xyz==1:
                    Q1[i1,j1]=k1+1
    return Q1
# 2-dimension to 3 dimension
def two_to_three(Q1):
    W1=np.zeros(shape=[9,9,9],dtype='int')
    for i1 in range(9):
        for j1 in range(9):
            xyz=Q1[i1,j1]
            if xyz>0:
                W1[i1,j1,xyz-1]=1

    return W1

# generete LT3
def lt_gen(W1x,W2x,W3x):
    LT3x=np.zeros(shape=[3,729],dtype='int')
    ctr_LT3x=0
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz1=W1x[i1,j1,k1]       # Wtrue
                xyz2=W2x[i1,j1,k1]       # Wfalse
                xyz3=W3x[i1,j1,k1]       # Winhi
                if xyz1==0 and xyz2==0 and xyz3==0:
                    LT3x[0,ctr_LT3x]=i1
                    LT3x[1,ctr_LT3x]=j1
                    LT3x[2,ctr_LT3x]=k1
                    ctr_LT3x=ctr_LT3x+1

    return ctr_LT3x,LT3x


# generate LT4(shuffle LT3)
def lt_shuffle(ctr,Table):
    Table2=np.zeros(shape=[3,ctr],dtype='int')
    Table_hist=np.zeros(shape=[ctr],dtype='int')
    for ctr4 in range(ctr):
        xyz5=1
        while xyz5>0:
            xyz4=random.randint(0,ctr-1)
            xyz5=Table_hist[xyz4]

        Table2[0,ctr4]=Table[0,xyz4]
        Table2[1,ctr4]=Table[1,xyz4]
        Table2[2,ctr4]=Table[2,xyz4]

        Table_hist[xyz4]=1

    return Table2

# double true check
def wt_check(W1):	#W1=Wtrue
    flg_wt=0
    for i1 in range(9):
        for j1 in range(9):
            xyz=0
            for k1 in range(9):
                if W1[i1,j1,k1]==1:
                    xyz=xyz+1
            if xyz>1:
                flg_wt=1
                return flg_wt

    for j1 in range(9):
        for k1 in range(9):
            xyz=0
            for i1 in range(9):
                if W1[i1,j1,k1]==1:
                    xyz=xyz+1
            if xyz>1:
                flg_wt=1
                return flg_wt

    for k1 in range(9):
        for i1 in range(9):
            xyz=0
            for j1 in range(9):
                if W1[i1,j1,k1]==1:
                    xyz=xyz+1
            if xyz>1:
                flg_wt=1
                return flg_wt

    for k1 in range(9):
        for bi1 in range(3):
            for bj1 in range(3):
                xyz=0
                for bi2 in range(3):
                    for bj2 in range(3):
                        if W1[3*bi1+bi2,3*bj1+bj2,k1]==1:
                            xyz=xyz+1
                if xyz>1:
                    flg_wt=1
                    return flg_wt

    return flg_wt

# double true check 2
def check_wt2(iz,jz,kz,Wtrue):
    # i direction
    wcnti=0
    for i2 in range(9):
        xyzi=Wtrue[i2,jz,kz]
        if xyzi==1:
            wcnti=wcnti+1
    wcntj=0
    for j2 in range(9):
        xyzj=Wtrue[iz,j2,kz]
        if xyzj==1:
            wcntj=wcntj+1
    wcntk=0
    for k2 in range(9):
        xyzk=Wtrue[iz,jz,k2]
        if xyzk==1:
            wcntk=wcntk+1
    wcntb=0
    bi1=iz//3
    bj1=jz//3
    for bi2 in range(3):
        for bj2 in range(3):
            xyzb=Wtrue[3*bi1+bi2,3*bj1+bj2,kz]
            if xyzb==1:
                wcntb=wcntb+1

    if wcnti>1 or wcntj>1 or wcntk>1 or wcntb>1:
        flg_wt2=1	#NG
    else:
        flg_wt2=0	#OK

    return flg_wt2

def make_targ_false(W1,W2):	#W1=Wfalse,W2=Wtarg
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                if W2[i1,j1,k1]==1:
                    W1[i1,j1,k1]=1
    return W1

def get_st_pair(W1):	#W1=Wfalse
    W2=np.zeros(shape=[9,9,9],dtype='int')	# for pier i
    W3=np.zeros(shape=[9,9,9],dtype='int')	# for pier j
    W4=np.zeros(shape=[9,9,9],dtype='int')	# for pier k
    W5=np.zeros(shape=[9,9,9],dtype='int')	# for pier b
    W6=np.zeros(shape=[9,9,9],dtype='int')	# for st_pair nodes
    for i1 in range(9):
        for j1 in range(9):
            for k1 in range(9):
                xyz=W1[i1,j1,k1]
                if xyz==1:
                    pqr1=0
                    for j2 in range(9):
                        xyz2=W1[i1,j2,k1]
                        if xyz2==1:
                            pqr1=pqr1+1
                    W2[i1,j1,k1]=pqr1

                    pqr2=0
                    for i2 in range(9):
                        xyz3=W1[i2,j1,k1]
                        if xyz3==1:
                            pqr2=pqr2+1
                    W3[i1,j1,k1]=pqr2

                    pqr3=0
                    for k2 in range(9):
                        xyz4=W1[i1,j1,k2]
                        if xyz4==1:
                            pqr3=pqr3+1
                    W4[i1,j1,k1]=pqr3

                    pqr4=0
                    bi1=i1//3
                    bj1=j1//3
                    for bi2 in range(3):
                        for bj2 in range(3):
                            xyz5=W1[3*bi1+bi2,3*bj1+bj2,k1]
                            if xyz5==1:
                                pqr4=pqr4+1
                    W5[i1,j1,k1]=pqr4
                    
                    #if pqr1==2 or pqr2==2 or pqr3==2 or pqr4==2:
                        #if pqr1>1 and pqr2>1 and pqr3>1 and pqr4>1:
                            #W6[i1,j1,k1]=1

                    if pqr1<3 or pqr2<3 or pqr3<3 or pqr4<3:
                        W6[i1,j1,k1]=1

    return W6

# link max check
# W1=csave(Wtruef)
def lmax_check(lvl,W1):

    Qfin2=three_to_two(W1)

    fcomp,res_lvl2,mess2,Qfinal2=s_web_main(lvl,Qfin2)

    Wtfinal=two_to_three(Qfinal2)
    flag_Wt1=wt_check(Wtfinal)
    if flag_Wt1==0:
        if fcomp==81 and res_lvl2>=lvl:
            flg_comp=1
        elif fcomp<81 and res_lvl2>=lvl:
            flg_comp=0
        elif res_lvl2<lvl:
            flg_comp=2
    else:
        flg_comp=2

    return flg_comp,fcomp,flag_Wt1,Qfinal2,res_lvl2,mess2

#---------------x---------------- MAIN FLOW -----------------------------
def getCond(lvl):

    CondTable=np.zeros(shape=[8],dtype='int')
    # condition in general
    fnum=random.randint(0,8)    # face number(0~8)

    # condition of reservation seat type
    cdir=random.randint(0,1)            # core direction(0=holizontal,1=vertical)
    cblk1=random.randint(0,8)           # core block number(0~8)
    cblk2=random.randint(0,2)           # core number in core block(0~2)
    fbk=random.randint(0,1)             # flag block to i/j(0) or i/j to block(1)

    # condition of NXN type
    matn=lvl-1                          # matrix number for NXN type
    fpos=random.randint(0,3)            # face=i/j(0=i/j,1=i/k,2=j/k,3=b/k)
    mdir=random.randint(0,1)            # mask direction(0=holizontal,1=vertical)

    CondTable=[fnum,cdir,cblk1,cblk2,fbk,matn,fpos,mdir]

    if lvl==2:
        Cface,Wcore,Wmask,Wtarg=core_gen_ind(fnum,cdir,cblk1,cblk2,fbk)
    if lvl>2:
        Cface,Wcore,Wmask,Wtarg=core_gen_sq(matn,fpos,fnum,mdir)

    Wlink=link_gen(Wcore,Wmask)

    ptr,LinkTable=link_table_gen(Wlink)

    Winhi=inhi_gen(Wcore,Wmask,Wtarg)

    return ptr,CondTable,LinkTable,Cface,Wcore,Wmask,Wtarg,Winhi

def getSeed(lvl,ptr,CondTable,LinkTable,Cface,Wcore,Wmask,Wtarg,Winhi):

    # seeding start

    flg2=0
    flg3=0
    flagx1=0
    for cntx in range(5):
        print("cntx=",cntx)	 #*******************************
        Wfalse=np.zeros(shape=[9,9,9],dtype='int')           # nodes of false
        Wtrue=np.zeros(shape=[9,9,9],dtype='int')           # nodes of True
        Wsun=np.zeros(shape=[9,9,9],dtype='int')	# nodes of SUN  
        Wsave1=np.zeros(shape=[9,9,9],dtype='int')
        Wsave2=np.zeros(shape=[9,9,9],dtype='int')
        Wsave3=np.zeros(shape=[9,9,9],dtype='int')
        Wsave4=np.zeros(shape=[9,9,9],dtype='int')
        Wsave5=np.zeros(shape=[9,9,9],dtype='int')
        Wsave6=np.zeros(shape=[9,9,9],dtype='int')
        lmax,LinkTable2=link_table_sort(ptr,LinkTable)          # sort linktable

        for ctr1 in range(ptr):
            #print("ctr1=",ctr1)	#**********************
            #print("A",end="")	#*********************************
            synm_side=0		# first synmetrical position
            i1=LinkTable2[0,ctr1]
            j1=LinkTable2[1,ctr1]
            k1=LinkTable2[2,ctr1]
            z1=LinkTable2[3,ctr1]

            xyz2=Wfalse[i1,j1,k1]
            xyz3=Winhi[i1,j1,k1]
            xyz2t=Wtrue[i1,j1,k1]

            # for mask increase check later
            flg1,masknum1=mask_check(Wmask,Wcore,Wfalse)	# flg1=1 means all mask completed
        
            if xyz2==1 or xyz3==1 or xyz2t==1:
                pass
                #print("B*")		#************************************

            else:
                #print("B",end="")		#************************************
                Wsave1=csave(Wfalse)
                Wsave2=csave(Wtrue)
                Wtrue[i1,j1,k1]=1
                Wfalse=false_gen(i1,j1,k1,Wfalse)
                flagx2=peer_check(Wfalse)

                if flagx2==1:
                    #print("C*")	#*********************************
                    Wfalse=csave(Wsave1)
                    Wtrue=csave(Wsave2)

                else:
                    #print("C",end="")	#***************************************
                    core_cond=core_check(lvl,CondTable,Cface,Wcore,Wfalse)
                    cnt_targ,TT,cnt_pair,Wtargpair=targ_check(Wtarg,Wcore,Wfalse,Wtrue)
                    flg_ufn,Wsun=ufn_check(Winhi,Wfalse,Wtrue)

                    if core_cond==1 or cnt_targ==0 or flg_ufn==1 or cnt_pair==0:
                        #print("D*")	#*********************************
                        Wfalse=csave(Wsave1)
                        Wtrue=csave(Wsave2)

                    else:
                        #print("D",end="")	#***************************
                        #check mask increased?
                        flg1,masknum2=mask_check(Wmask,Wcore,Wfalse)    # flg1=1 means all mask completed

                        if masknum2==masknum1:
                            #print("E*")	#********************************
                            Wfalse=csave(Wsave1)
                            Wtrue=csave(Wsave2)

                        else:
                            # check center
                            #print("E",end="")	#*******************************
                            if i1==4 and j1==4:
                                synm_side=1	# no second synmetrical position
                                #print("F*")	#********************************
                            else:
                                # check symmetrical position
                                #print("F",end="")	#************************************
                                Cpeer=np.zeros(shape=[9],dtype='int')               # UFN check for a peer
                                Cpeer_hist=np.zeros(shape=[9],dtype='int')		# check history in a peer

                                i2=8-i1
                                j2=8-j1

                                # make Cpeer

                                pptr=0
                                cnt_true=0
                                for k2 in range(9):
                                    xyz5=Wfalse[i2,j2,k2]
                                    xyz6=Winhi[i2,j2,k2]
                                    #xyz7=Whist[i2,j2,k2]
                                    xyz7=Wtrue[i2,j2,k2]
                                    if xyz5==0 and xyz6==0:
                                        Cpeer[pptr]=k2
                                        pptr=pptr+1
                                    elif xyz7==1:
                                        cnt_true=cnt_true+1
                                if pptr==0 or cnt_true>0:
                                    #print("G*")	#*********************************
                                    Wfalse=csave(Wsave1)
                                    Wtrue=csave(Wsave2)
                                elif cnt_true==1:
                                    synm_side=1
                                else:
                                    #print("G",end="")	#********************************
                                    xyz9=0
                                    while pptr>xyz9:
                                        #print("H",end="")		#*******************************
                                        k2x=random.randint(0,pptr-1)
                                        xyz8=Cpeer_hist[k2x]
                                        if xyz8==1:
                                            pass
                                            #print("I*")	#*****************************
                                        else:
                                            #print("I",end="")	#****************************
                                            Wsave3=csave(Wfalse)
                                            Wsave4=csave(Wtrue)

                                            Cpeer_hist[k2x]=1

                                            Wtrue[i2,j2,k2x]=1
                                            Wfalse=false_gen(i2,j2,k2x,Wfalse)
                                            flagx2=peer_check(Wfalse)

                                            if flagx2==0:
                                                #print("J",end="")	#***************************
                                        
                                                core_cond=core_check(lvl,CondTable,Cface,Wcore,Wfalse)
                                                cnt_targ,TT,cnt_pair,Wtargpair=targ_check(Wtarg,Wcore,Wfalse,Wtrue)
                                                flg_ufn,Wsun=ufn_check(Winhi,Wfalse,Wtrue)

                                                if core_cond==1 or cnt_targ==0 or flg_ufn==1 or cnt_pair==0:
                                                    #print("K*")	#***********************************
                                                    Wfalse=csave(Wsave3)
                                                    Wtrue=csave(Wsave4)

                                                else:
                                                    #print("K")	#***************************************
                                                    synm_side=1	# second synmetrical position
                                                    break

                                            else:
                                                #print("J*",end="")		#***************************************
                                                Wfalse=csave(Wsave3)
                                                Wtrue=csave(Wsave4)

                                        # while loop-2 last 
                                        #print("L",end="")		#*************************************** 
                                        xyz9=np.sum(Cpeer_hist)

                                    # after go out from while loop-2 
                                    #print("xyz9=",xyz9,"pptr=",pptr)	#*****************************
                                    if xyz9==pptr:
                                        #print("M")	#***************************************
                                        Wfalse=csave(Wsave1)
                                        Wtrue=csave(Wsave2)

            
            # last of ctr1 loop

            flg2,masknum3=mask_check(Wmask,Wcore,Wfalse)    # flg2=1 means all mask completed

            if flg2==1 and synm_side==1:
                # SUN link check
                Wsave5=csave(Wfalse)
                Wsave6=csave(Wtrue)

                flg_ufn,Wsun=ufn_check(Winhi,Wfalse,Wtrue)

                flg_inhi,Wfalsex,Wtruex,Wsunx=sun_check(lvl-1,Wsun,Wfalse,Wtrue,Winhi)

                if flg_inhi==1:
                    break	# go to next cntx loop

                else:
                    core_cond=core_check(lvl,CondTable,Cface,Wcore,Wfalsex)
                    cnt_targ,TT,cnt_pair,Wtargpair=targ_check(Wtarg,Wcore,Wfalsex,Wtruex)	# cnt_targ=0 --> NG
                    flg_ufn,Wsun4=ufn_check(Winhi,Wfalsex,Wtruex)	# make Wsun and check double sun in a pier

                    if core_cond==1 or cnt_targ==0 or flg_ufn==1 or cnt_pair==0:
                        break	# go to next cntx loop
                    else:
                        Wfalse=csave(Wsave5)
                        Wtrue=csave(Wsave6)

                        flg_comp,fcomp,flag_Wt1,Qfinal,res_lvl,mess=lmax_check(lvl,Wtrue)

                        flg_seed=0
                        if flg_comp==1:

                            flg_seed=1
                            Qorg=three_to_two(Wtrue)

                            return flg_seed,fcomp,Qorg,Qfinal,res_lvl,mess,Wtrue,Wfalse

                        elif flag_Wt1==0 and res_lvl>=lvl:

                            flg_seed=2
                            Qorg=three_to_two(Wtrue)

                            return flg_seed,fcomp,Qorg,Qfinal,res_lvl,mess,Wtrue,Wfalse

                        else:
                            break	# go to next cntx loop
                  
        #print("ctr1 loop end")	#**************************
            
    flg_seed=0
    fcomp=0
    Qorg=np.zeros(shape=[9,9],dtype='int')
    Qfinal=np.zeros(shape=[9,9],dtype='int')
    res_lvl=0
    mess="fail seeding"
    Wtrue=np.zeros(shape=[9,9,9],dtype='int')
    Wfalse=np.zeros(shape=[9,9,9],dtype='int')

    return flg_seed,fcomp,Qorg,Qfinal,res_lvl,mess,Wtrue,Wfalse

# W1=Wtrue,W2=Wfalse,W3=Winhi
def getBase(lvl_seed,lvl_mini,Wtruef,Wfalsef,Winhif,Wcoref,Wtargf,Cfacef,CondTablef,ctr_LT3,LT4,dt1,cnta2,cntb):

    # initialize work arrays
    Wsave1f=np.zeros(shape=[9,9,9],dtype='int')
    Wsave2f=np.zeros(shape=[9,9,9],dtype='int')
    Wsave3f=np.zeros(shape=[9,9,9],dtype='int')
    Wsave4f=np.zeros(shape=[9,9,9],dtype='int')
    Wsave5f=np.zeros(shape=[9,9,9],dtype='int')
    Wsave6f=np.zeros(shape=[9,9,9],dtype='int')

    Wsave5f=csave(Wfalsef)
    Wsave6f=csave(Wtruef)

    flg_base=0
    for cntz0 in range(ctr_LT3):
        #print("start cntz0 loop")	#*****************************

        Wsave1f=csave(Wfalsef)
        Wsave2f=csave(Wtruef)

        #print("a0",end="")      #*******************************
        synm_side=0             # first synmetrical position
        iz=LT4[0,cntz0]
        jz=LT4[1,cntz0]
        kz=LT4[2,cntz0]

        Wtruef[iz,jz,kz]=1
        Wfalsef=false_gen(iz,jz,kz,Wfalsef)
        flagx2=peer_check(Wfalsef)
        if flagx2==1:
            #print("bo*")	#*************************
            Wfalsef=csave(Wsave1f)
            Wtruef=csave(Wsave2f)

            # return to cntz0 loop

        else:
            #print("b0",end="")   #***************************************
            core_cond=core_check(lvl_seed,CondTablef,Cfacef,Wcoref,Wfalsef)
            cnt_targ,TT,cnt_pair,Wtargpair=targ_check(Wtargf,Wcoref,Wfalsef,Wtruef)
            flg_ufn,Wsunf=ufn_check(Winhif,Wfalsef,Wtruef)

            if core_cond==1 or cnt_targ==0 or flg_ufn==1 or cnt_pair==0:
                #print("c0*")  #***********************************
                Wfalsef=csave(Wsave1f)
                Wtruef=csave(Wsave2f)
                # return to cntz0 loop

            else:
                #print("c0",end="")       #***************************
                # check center
                if iz==4 and jz==4:
                    synm_side=1     # no second synmetrical position
                    #print("d*")     #********************************
              
                else:
                    # check symmetrical position
                    #print("d0",end="")       #************************************
                    Cpeer=np.zeros(shape=[9],dtype='int')               # UFN check for a $
                    Cpeer_shf=np.zeros(shape=[9],dtype='int') 	# shaffle Cpeer
                    Cpeer_hist=np.zeros(shape=[9],dtype='int')          # check history in$

                    iz2=8-iz
                    jz2=8-jz

                    # make Cpeer
                    pptr=0
                    cnt_true=0
                    for k2 in range(9):
                        xyz5=Wfalsef[iz2,jz2,k2]
                        xyz6=Winhif[iz2,jz2,k2]
                        xyz7=Wtruef[iz2,jz2,k2]
                        if xyz5==0 and xyz6==0:
                            Cpeer[pptr]=k2
                            pptr=pptr+1
                        elif xyz7>0:
                            cnt_true=cnt_true+1

                    if pptr==0 or cnt_true>1:
                        #print("f0*") #*********************************
                        Wfalsef=csave(Wsave1f)
                        Wtruef=csave(Wsave2f)
                        # return to ctnz0 loop
                    elif cnt_true==1:
                        synm_side=1
                    else:
                        #print("f0",end="")   #********************************
                        pntr=0
                        while pntr<pptr:
                            shf=random.randint(0,pptr-1)
                            qqq=Cpeer_hist[shf] 
                            if qqq==0:
                                Cpeer_hist[shf]=1
                                Cpeer_shf[shf]=shf
                                pntr=pntr+1

                        for ctr3 in range(pptr):
                            #print("ctr3 loop start")  #*******************************

                            Wsave3f=csave(Wfalsef)
                            Wsave4f=csave(Wtruef)

                            k2x=Cpeer_shf[ctr3]

                            Wtruef[iz2,jz2,k2x]=1
                            Wfalsef=false_gen(iz2,jz2,k2x,Wfalsef)
                            flagx2=peer_check(Wfalsef)

                            if flagx2==0:
                                #print("g0",end="")       #***************************

                                core_cond=core_check(lvl_seed,CondTablef,Cfacef,Wcoref,Wfalsef)
                                cnt_targ,TT,cnt_pair,Wtargpair=targ_check(Wtargf,Wcoref,Wfalsef,Wtruef)
                                flg_ufn,Wsunf=ufn_check(Winhif,Wfalsef,Wtruef)

                                if core_cond==1 or cnt_targ==0 or flg_ufn==1 or cnt_pair==0:
                                    #print("h0*") #***********************************
                                    Wfalsef=csave(Wsave3f)
                                    Wtruef=csave(Wsave4f)
                                    # return to ctr3 loop

                                else:
                                    #print("h0")  #***************************************
                                    synm_side=1     # second synmetrical position

                            else:	# flagx2=1
                                #print("g0*",end="") #******************************
                                Wfalsef=csave(Wsave3f)
                                Wtruef=csave(Wsave4f)
                                # go to next ctr3 loop

                        # after ctr3 loop end
                        if synm_side==0:
                            Wfalsef=csave(Wsave1f)
                            Wtruef=csave(Wsave2f)
                        # go to next cntz0 loop


        # last of cntz0 loop
        #print("k0*")       #*********************

        if synm_side==1:
            #print("l0*")	#********************
            qnum=np.sum(Wtruef)
            if qnum>40:
                #print("l01*")	#********************
                break

            else:
                # last check
                Wsave5f=csave(Wfalsef)
                Wsave6f=csave(Wtruef)

                flg_comp,fcomp,flag_Wt1,Qfinal,res_lvl,mess=lmax_check(lvl_mini,Wtruef)

                cnt_total=cnta2*20+cntb+1
                crtime2,crate3=getPastTime(dt1,cnt_total)

                print("cnta2=",cnta2,"cntb=",cntb,"total count=",cnt_total,"rate=",crate3)
                print("fcomp=",fcomp,"result level=",res_lvl,"qnum=",qnum,"time=",crtime2)

                if flg_comp==1:
                    #print("p0*")        #************************
                    flg_base=1
                    Qorg=three_to_two(Wtruef)

                    return flg_base,fcomp,Qorg,Qfinal,res_lvl,mess,Wtruef,Wfalsef

                elif flg_comp==0:
                    # go to next cntz0 loop
                    Wfalsef=csave(Wsave5f)
                    Wtruef=csave(Wsave6f)

                else:	# flg_comp=2
                    # go to next cntz0 loop cancelling cuurrent pair
                    Wfalsef=csave(Wsave1f)
                    Wtruef=csave(Wsave2f)

    # after cntz0 loop end
        
    flg_base=0
    fcomp=0
    Qorg=np.zeros(shape=[9,9],dtype='int')
    Qfinal=np.zeros(shape=[9,9],dtype='int')
    res_lvl=0
    mess="fail base make"
    Wtruef=np.zeros(shape=[9,9,9],dtype='int')
    Wfalsef=np.zeros(shape=[9,9,9],dtype='int')

    return flg_base,fcomp,Qorg,Qfinal,res_lvl,mess,Wtruef,Wfalsef
    
def getFinal_1(dt1,cnty):

    for cntz in range(500):
        # initialize work arrays
        Wsave1f=np.zeros(shape=[9,9,9],dtype='int')
        Wsave2f=np.zeros(shape=[9,9,9],dtype='int')
        Wsave3f=np.zeros(shape=[9,9,9],dtype='int')
        Wsave4f=np.zeros(shape=[9,9,9],dtype='int')
        Wsave5f=np.zeros(shape=[9,9,9],dtype='int')
        Wsave6f=np.zeros(shape=[9,9,9],dtype='int')

        Wtruef=np.zeros(shape=[9,9,9],dtype='int')
        Wfalsef=np.zeros(shape=[9,9,9],dtype='int')
        Winhif=np.zeros(shape=[9,9,9],dtype='int')

        # print("cntz(level-1)=",cntz)        #***********************:

        for ctr2 in range(81):
            #print("a",end="")   #*******************************
            synm_side=0

            Wsave1f=csave(Wfalsef)
            Wsave2f=csave(Wtruef)
            fnum1=np.sum(Wfalsef)

            iz=random.randint(0,8)
            jz=random.randint(0,8)
            kz=random.randint(0,8)

            Wtruef[iz,jz,kz]=1
            Wfalsef=false_gen(iz,jz,kz,Wfalsef)
            flagx2=peer_check(Wfalsef)
            #print("flg_wt2=",flg_wt2)	#***********************
            if flagx2==1:
                #print("b*") #*********************************
                Wfalsef=csave(Wsave1f)
                Wtruef=csave(Wsave2f)

            else:
                #print("b",end="")   #***************************************
                flg_ufn,Wsunf=ufn_check(Winhif,Wfalsef,Wtruef)

                fnum2=np.sum(Wfalsef)

                if flg_ufn==1 or fnum1==fnum2:
                    #print("c*")  #***********************************
                    Wfalsef=csave(Wsave1f)
                    Wtruef=csave(Wsave2f)

                else:
                    #print("c",end="")       #***************************
                    # check center
                    if iz==4 and jz==4:
                        synm_side=1
                        #print("d*")     #********************************
                    else:
                        # check symmetrical position
                        #print("d",end="")       #************************************
                        Cpeer=np.zeros(shape=[9],dtype='int')               # UFN check for a peer
                        Cpeer_hist=np.zeros(shape=[9],dtype='int')          # check history in a peer

                        iz2=8-iz
                        jz2=8-jz

                        # make Cpier
                        pptr=0
                        for k2 in range(9):
                            xyz5=Wfalsef[iz2,jz2,k2]
                            xyz6=Winhif[iz2,jz2,k2]
                            if xyz5==0 and xyz6==0:
                                Cpeer[pptr]=k2
                                pptr=pptr+1
                        if pptr==0:
                            #print("e*") #*********************************
                            Wfalsef=csave(Wsave1f)
                            Wtruef=csave(Wsave2f)
                        else:
                            #print("e",end="")   #********************************
                            xyz9=0
                            while pptr>xyz9:
                                #print("f",end="")               #*******************************
                                k2x=random.randint(0,pptr-1)
                                xyz8=Cpeer_hist[k2x]
                                if xyz8==1:
                                    pass
                                    #print("g*") #*****************************
                                else:
                                    #print("g",end="")   #****************************
                                    Wsave3f=csave(Wfalsef)
                                    Wsave4f=csave(Wtruef)

                                    Cpeer_hist[k2x]=1

                                    Wtruef[iz2,jz2,k2x]=1
                                    Wfalsef=false_gen(iz2,jz2,k2x,Wfalsef)
                                    flagx2=peer_check(Wfalsef)

                                    if flagx2==0:
                                        #print("h",end="")       #***************************

                                        flg_ufn,Wsunf=ufn_check(Winhif,Wfalsef,Wtruef)

                                        if flg_ufn==1:
                                            #print("i*") #***********************************
                                            Wfalsef=csave(Wsave3f)
                                            Wtruef=csave(Wsave4f)

                                        else:
                                            #print("i")  #***************************************
                                            synm_side=1
                                            break       # go out from while loop

                                    else:
                                        #print("h*",end="")      #******************************
                                        Wfalsef=csave(Wsave3f)
                                        Wtruef=csave(Wsave4f)

                                # while loop last
                                #print("j",end="")       #******************************
                                xyz9=np.sum(Cpeer_hist)

                            #print("xyz9=",xyz9,"pptr=",pptr)    #*****************************
                            if xyz9==pptr:
                                #print("k")      #***************************************
                                Wfalsef=csave(Wsave1f)
                                Wtruef=csave(Wsave2f)

            # last of  ctr2 "for" loop

            if synm_side==1:

                qnum=np.sum(Wtruef)
                if qnum<20:
                    pass

                elif qnum>40:
                    break

                else:

                    lvl_mini=1
                    flg_comp,fcomp,flag_Wt1,Qfinal,res_lvl,mess=lmax_check(lvl_mini,Wtruef)

                    Wsave5f=csave(Wfalsef)
                    Wsave6f=csave(Wtruef)

                    cnt=cntz+1
                    crtime2,crate3=getPastTime(dt1,cnt)

                    print("cntz=",cntz,"rate=",crate3,"fcomp=",fcomp,"qnum=",qnum,"time=",crtime2)

                    if flg_comp==1:
                        #print("p0*")        #************************
                        Qorg=three_to_two(Wtruef)

                        return fcomp,Qorg,Qfinal,mess

                    elif flg_comp==0:
                        # go to next ctr2 loop
                        Wfalsef=csave(Wsave5f)
                        Wtruef=csave(Wsave6f)

                    else:   # flg_comp=2
                        # go to next ctr2 loop cancelling cuurrent pair
                        Wfalsef=csave(Wsave1f)
                        Wtruef=csave(Wsave2f)

    fcomp=0
    Qfinal2=np.zeros(shape=[9,9,],dtype='int')
    Qfin2=np.zeros(shape=[9,9,],dtype='int')
    res_lvl2=1
    mess2="time up!"
    return fcomp,Qfin2,Qfinal2,mess2

def s_create_main(lvl_seed,lvl_mini):

    dt1=datetime.datetime.now()
    Wsave1=np.zeros(shape=[9,9,9],dtype='int')
    Wsave2=np.zeros(shape=[9,9,9],dtype='int')

    if lvl_seed>1:
        cnta2=0
        for cnta in range(1000):

            print("start cnta loop")    #*************************
            ptr2,CondTable2,LinkTable2,Cface2,Wcore2,Wmask2,Wtarg2,Winhi2=getCond(lvl_seed)
            flg_seed,fcomp,Qorg,Qfinal,res_lvl,mess,Wtrues,Wfalses=getSeed(lvl_seed,ptr2,CondTable2,LinkTable2,Cface2,Wcore2,Wmask2,Wtarg2,Winhi2)

            Wsave1=csave(Wfalses)
            Wsave2=csave(Wtrues)

            if flg_seed==0:     # seeding failed
                pass    # retry getCond

            elif flg_seed==1:   # Q table is already completed

                qnum1=np.sum(Wtrues)
                Qmini,qmin=getMini(lvl_mini,Qorg)

                print("Q")
                print(Qmini)

                print("fixed column=",qnum1,"-->",qmin)
                print(mess)

                print("Qfinal")
                print(Qfinal)

                print("CondTable=",CondTable2)

                cnt=1
                crtime2,crate3=getPastTime(dt1,cnt)

                print("already completed after seeding!")
                print("target level=",lvl_seed,"time=",crtime2)

                np.savetxt("q_answer.txt",Qfinal)

                return Qmini,qmin,Qfinal,mess,crtime2

            else:       # go to getBase
 
                # generate link table for getFinal
                ctr_LT3,LT3=lt_gen(Wtrues,Wfalses,Winhi2)

                for cntb in range(20):
                    print("start cntb loop")    #**************************

                    # shuffle LT3 to LT4
                    LT4=lt_shuffle(ctr_LT3,LT3)

                    Wfalses=csave(Wsave1)
                    Wtrues=csave(Wsave2)

                    flg_base,fcomp,Qorg,Qfinal,res_lvl,mess,Wtrueb,Wfalseb=getBase(lvl_seed,lvl_mini,Wtrues,Wfalses,Winhi2,Wcore2,Wtarg2,Cface2,CondTable2,ctr_LT3,LT4,dt1,cnta2,cntb)

                    if flg_base==0:
                        #print("testA")  #************************************:
                        pass    # go to cntb loop end

                    elif flg_base==1:   # completed during base making

                        qnum1=np.sum(Wtrueb)
                        Qmini,qmin=getMini(lvl_mini,Qorg)

                        print("Cface2")         #*********************
                        print(Cface2)           #*********************

                        print("Q")
                        print(Qmini)

                        print("fixed column=",qnum1,"-->",qmin)
                        print(mess)

                        print("Qfinal")
                        print(Qfinal)

                        print("CondTable=",CondTable2)

                        cnt_total=cnta2*20+cntb+1
                        crtime2,crate3=getPastTime(dt1,cnt_total)

                        print("cnta2=",cnta2,"cntb=",cntb,"total count=",cnt_total,"rate=",crate3)
                        print("target level=",lvl_seed,"time=",crtime2)

                        np.savetxt("q_answer.txt",Qfinal)

                        return Qmini,qmin,Qfinal,mess,crtime2

                    else:
                        pass

                    #print("last of cntb loop")  #*******************
                #print("after end of cntb loop") #*********************
                cnta2=cnta2+1

            # cnta loop last

        #after cnta loop

    else:       # level-1

        for cnty in range(500):

            fcomp,Qfin,Qfinal,mess=getFinal_1(dt1,cnty)

            if fcomp==81:
                qnum=0
                for i in range(9):
                    for j in range(9):
                        abc=Qfin[i,j]
                        if abc>0:
                            qnum=qnum+1

                Qmini,qmin=getMini(lvl_seed,Qfin)
                print("Q")
                print(Qmini)

                print("fixed column=",qnum,"-->",qmin)
                print(mess)

                print("Qfinal")
                print(Qfinal)

                cnt=1
                crtime2,crate3=getPastTime(dt1,cnt)
                print("time=",crtime2)

                np.savetxt("q_answer.txt",Qfinal)

                return Qmini,qmin,Qfinal,mess,crtime2


    cnt=1
    crtime2,crate3=getPastTime(dt1,cnt)
    print("time=",crtime2)
    print("所要時間=",crtimer2)
    print("問題作成失敗しました")
    Qmini=np.zeros(shape=[9,9],dtype='int')
    Qfinal=np.zeros(shape=[9,9],dtype='int')
    mess="問題作成失敗しました"
    qmin=0
    return Qmini,qmin,Qfinal,mess,crtime2

def getMini(lvl,Q1):

    Q2=Q1
    for x in range(4):
        for y in range(9):
            if x==4 and y==4:
                break
            z1=Q2[x,y]
            z2=Q2[8-x,8-y]
            if z1>0:
                Q2[x,y]=0
                Q2[8-x,8-y]=0
                fcomp,res_lvl,mess,Qfinal=s_web_main(lvl,Q2)
                if fcomp<81 or res_lvl<lvl:
                    Q2[x,y]=z1
                    Q2[8-x,8-y]=z2

    qmin=0
    for i1 in range(9):
        for j1 in range(9):
            xyz=Q2[i1,j1]
            if xyz>0:
                qmin=qmin+1

    return Q2,qmin

def getPastTime(dt1,cnt):

    dt2=datetime.datetime.now()
    dt3=dt2-dt1
    crtime=str(dt3)
    a=crtime.find(":")

    if a>2:
        b=crtime.find("d")
        dth_day=crtime[0:b]
        dth_hour=crtime[a-2:a]
    else:
        dth_day=0
        dth_hour=crtime[0:a]

    dth=str(int(dth_day)*24+int(dth_hour))
    dtm=crtime[a+1:a+3]
    dts=crtime[a+4:a+6]
    crtime2=dth+":"+dtm+":"+dts
    time_total=int(dth)*3600+int(dtm)*60+int(dts)
    crate=time_total/cnt
    crate2=str(crate)
    crate3=crate2[0:5]

    return crtime2,crate3

