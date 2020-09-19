from flask import Flask, render_template, Response, redirect
import numpy as np
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt

from convert_web import *	# 撮影した画像を9X9に分割
from ocr_web import *		# 分割した画像を数字として読み取る
from s_access2 import *		# 保存した数独問題の読み書き
from sudoku_web2 import *	# 数独問題を解く
from s_create_web2 import *	# 数独問題を作る

#グローバル変数

flag_hint=0
flag_conv=1
flag_hidden=0
flag_core=2

## Flaskサーバーの初期化

app = Flask(__name__)


# 問題ポインター更新
def qp_update(num):
    f=open("qptr.txt", "w+")
    f.write(num)
    f.close

# 問題ポインター読み込み
def qp_read():
    f=open("qptr.txt","r+")
    lines=f.readlines()
    f.close()
    num=lines[0]
    return num

# カーソル位置の数字の書き換え
def col_update(num): #numは整数
    global cur
    numi=cur//9
    numj=cur%9

    Q=np.loadtxt('q_temp.txt') # float
    W=np.mat(Q,dtype='int') # int
    W[numi,numj]=num # 書き換え
    np.savetxt('q_temp.txt',W)
    # カーソルを＋１する
    if cur<80:
        cur=cur+1

# メッセージ更新
def msg_update(msg):
    f=open("message.txt", "w+")
    f.write(msg)
    f.close

# メッセージ読み込み
def msg_read():
    f=open("message.txt","r")
    lines=f.readlines()
    f.close()
    msg=lines[0]
    return msg

# 問題の保存数読み込み
def qnum():
    f=open("s_mondai.txt","r+")
    lines=f.readlines()
    f.close
    numz=lines[0]
    return numz

# カーソルの初期化 0~80
cur=0

# 問題番号の初期化（最後の番号）
qptr=qnum()
qp_update(qptr)


# 回答配列の初期化
WY=np.zeros(shape=[9,9],dtype='int')
np.savetxt('q_answer.txt',WY)

# メッセージクリア
msg=" "
msg_update(msg)

# ルートパス (/) にアクセスがあれば実行する
@app.route('/')
def index():
    global flag_hint,cur

    # 数独問題をファイルから読む
    Q=np.loadtxt('q_temp.txt')
    Qtemp=np.loadtxt('q_answer.txt')
    W=np.mat(Q,dtype='int')
    Wtemp=np.mat(Qtemp,dtype='int')
    WX=np.mat(W,dtype='str')
    WXtemp=np.mat(Wtemp,dtype='str')
    # カーソルポインタ
    curx=cur//9  # 行番号
    cury=cur%9   # 列番号
    # メッセージ読み込み
    msg=msg_read()
    # 問題の保存数読み込み
    qfig=qnum()
    qptr=qp_read()
    pointer=qptr+"/"+qfig
    # クライアントに index.html を返す
    return render_template('index.html',msg=msg,pointer=pointer,WX=WX,WXtemp=WXtemp,cur=cur,curx=curx,cury=cury)

# /start-squat にアクセスがあれば実行する
@app.route('/start-squat')
def start_squat():
    global cap  #************************
    # カメラの読み込み
    cap=cv2.VideoCapture(0)
    print("カメラ読み込み")#**************************************

    # クライアントに squat.html を返す
    return render_template('squat.html')

# /finish-squat にアクセスがあれば実行する
@app.route('/finish-squat')
def finish_squat():

    # 画像を保存
    print("画像を保存")#***************************************
    ret,frame=cap.read()

    while ret==False:
        pass

    cv2.imwrite('sudoku.png',frame)

    # カメラ切り離し
    print("カメラ切り離し")#**********************************

    cap.release()		# maybe not necessary
    cv2.destroyAllWindows()

    # ホーム画面に遷移させる
    return redirect('/')

# /camera.mjpeg にアクセスがあれば実行する
@app.route('/camera.mjpeg')
def camera():
    def gen():
        while True:	# while cap is opened

            # フレームを取得
            ret,frame=cap.read()

            while ret==False:
                pass

            # フレームをJPEGに変換
            ret, jpeg = cv2.imencode('.jpg', frame)

            while ret==False:
                pass

            yield (b'--frame\n'
                b'Content-Type: image/jpeg\n\n' + jpeg.tobytes() + b'\n\n')

    # クライアントにMotion JPEGを配信
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# /c-right にアクセスがあれば実行する
@app.route('/c-right')
def c_right():
    global cur
    if cur<80:
        cur=cur+1
    # ホーム画面に遷移させる
    return redirect('/')

# /c-left にアクセスがあれば実行する
@app.route('/c-left')
def c_left():
    global cur
    if cur>0:
        cur=cur-1
    # ホーム画面に遷移させる
    return redirect('/')

# /c-up にアクセスがあれば実行する
@app.route('/c-up')
def c_up():
    global cur
    if cur>8:
        cur=cur-9
    # ホーム画面に遷移させる
    return redirect('/')

# /c-down にアクセスがあれば実行する
@app.route('/c-down')
def c_down():
    global cur
    if cur<72:
        cur=cur+9
    # ホーム画面に遷移させる
    return redirect('/') 

# /c-home にアクセスがあれば実行する
@app.route('/c-home')
def c_home():
    global cur
    cur=0
    # ホーム画面に遷移させる
    return redirect('/')

# /b-1 にアクセスがあれば実行する
@app.route('/b-1')
def b_1():
    figx=1       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-2 にアクセスがあれば実行する
@app.route('/b-2')
def b_2():
    figx=2       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-3 にアクセスがあれば実行する
@app.route('/b-3')
def b_3():
    figx=3       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-4 にアクセスがあれば実行する
@app.route('/b-4')
def b_4():
    figx=4       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-5 にアクセスがあれば実行する
@app.route('/b-5')
def b_5():
    figx=5       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-6 にアクセスがあれば実行する
@app.route('/b-6')
def b_6():
    figx=6       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-7 にアクセスがあれば実行する
@app.route('/b-7')
def b_7():
    figx=7       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-8 にアクセスがあれば実行する
@app.route('/b-8')
def b_8():
    figx=8       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-9 にアクセスがあれば実行する
@app.route('/b-9')
def b_9():
    figx=9       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-space にアクセスがあれば実行する
@app.route('/b-space')
def b_space():
    figx=0       # int
    col_update(figx) # 該当カラム書き換え
    # ホーム画面に遷移させる
    return redirect('/')

# /b-all にアクセスがあれば実行する
@app.route('/b-all')
def b_all():
    Q=np.zeros(shape=[9,9],dtype='int')
    np.savetxt('q_temp.txt',Q)
    np.savetxt('q_answer.txt',Q)

    # メッセージクリア
    msg=" "
    msg_update(msg)

    # ホーム画面に遷移させる
    return redirect('/')

# /b-mscrl にアクセスがあれば実行する
@app.route('/b-mscrl')
def b_mscrl():

    # メッセージクリア
    msg=" "
    msg_update(msg)

    # ホーム画面に遷移させる
    return redirect('/')

# /convocr にアクセスがあれば実行する
@app.route('/convocr')
def convocr():
    global flag_conv
    #flg=flag_read()	#汎用フラッグ
    if flag_conv==1:
        flag_conv=0	# 二度押しできないようにする
        # 回答配列の初期化
        WY=np.zeros(shape=[9,9],dtype='int')
        np.savetxt('q_answer.txt',WY)
        # 9x9=81マスに分ける
        main_conv()	# convert_web.py
        #結果の取得
        msg=msg_read()
        if msg=="ok":
            # 数字を読みとる
            main_ocr()	# ocr_web.py
            # メッセージ更新
            msg="画像読み取り完了しました！"
            msg_update(msg)
        else:
            # メッセージ更新
            msg="もう一度撮影してください！"
            msg_update(msg)
        flag_conv=1

    # ホーム画面に遷移させる
    return redirect('/')

# /solve（問題を解く!) にアクセスがあれば実行する
@app.route('/solve')
def solve():
    global flag_conv
    if flag_conv==1:
        flag_conv=0        # 二度押しできないようにする
        # 数独問題をファイルから読む
        Q=np.loadtxt('q_temp.txt')
        W=np.mat(Q,dtype='int')

        x1,msg,Qans=s_web_main(7,W)	# import sudoku_web2.py

        msg_update(msg)
        flag_conv=1
    # ホーム画面に遷移させる
    return redirect('/')

# /create（問題を作る!) にアクセスがあれば実行する
@app.route('/create')
def create():
    global flag_conv
    #flg=flag_read()     #汎用フラッグ
    print("flag_conv=",flag_conv)	#***************************

    if flag_conv==1:
        flag_conv=0        # 二度押しできないようにする
        Qtemp,Qans,msg=s_create_main2() # import s_create_web2.py

        np.savetxt('q_temp.txt',Qtemp)
        Qzero=np.zeros(shape=[9,9],dtype='int')
        np.savetxt('q_answer.txt',Qzero)
        msg_update(msg)
        flag_conv=1

    # ホーム画面に遷移させる
    return redirect('/')

# /qsave（問題を保存!) にアクセスがあれば実行する
@app.route('/qsave')
def qsave():
    global flag_conv
    if flag_conv==1:
        flag_conv=0        # 二度押しできないようにする

        Q=np.loadtxt('q_temp.txt')
        W=np.mat(Q,dtype='int')
        msg=monwrite(W)
        msg_update(msg)

        # 問題番号の初期化（最後の番号）
        qptr=qnum()
        qp_update(qptr)

        flag_conv=1

    # ホーム画面に遷移させる
    return redirect('/')

# /qload（問題を読む!) にアクセスがあれば実行する
@app.route('/qload')
def qload():
    global flag_conv
    if flag_conv==1:
        flag_conv=0        # 二度押しできないようにする

        numx=qp_read()		# str
        numy=int(numx)
        Qmon,Qans,mess=monread(numy)

        np.savetxt('q_temp.txt',Qmon)

        Qzero=np.zeros(shape=[9,9],dtype='int')
        np.savetxt('q_answer.txt',Qzero)

        msg_update(mess)

        flag_conv=1

        # ホーム画面に遷移させる
        return redirect('/')

# /qleft（ポインタカウントダウン) にアクセスがあれば実行する
@app.route('/qleft')
def qleft():
    global flag_conv
    if flag_conv==1:
        flag_conv=0        # 二度押しできないようにする

        numx=qp_read()          # str
        numy=int(numx)

        if numy<2:
            pass
        else:
            numz=numy-1
            numz2=str(numz)
            qp_update(numz2)

            flag_conv=1

        # ホーム画面に遷移させる
        return redirect('/')

# /qright（ポインタカウントアップ) にアクセスがあれば実行する
@app.route('/qright')
def qright():
    global flag_conv
    if flag_conv==1:
        flag_conv=0        # 二度押しできないようにする

        numx=qp_read()          # str
        num_max=qnum()		# str
        if int(numx)==int(num_max):
            pass
        else:
            numy=int(numx)
            numz=numy+1
            numz2=str(numz)
            qp_update(numz2)

        flag_conv=1

        # ホーム画面に遷移させる
        return redirect('/')

# /b-hint にアクセスがあれば実行する
@app.route('/b-hint')
def b_hint():
    global flag_hint
    global flag_hidden
    global flag_core
    sfig=np.zeros(shape=[3,3],dtype='int')
    for i in range(3):
        for j in range(3):
            z=i*3+j+1
            sfig[i,j]=z

    # 数独問題をファイルから読む
    Q1h=np.loadtxt('q_temp.txt')
    Q2h=np.mat(Q1h,dtype='int')
    # 三次元配列初期化
    W1h=np.zeros(shape=[9,9,9],dtype='int')	# CubeMaskTemp用
    W2h=np.zeros(shape=[9,9,9],dtype='int')	# 問題を三次元化した配列
    W3h=np.zeros(shape=[9,9,9],dtype='int')     # マスク配列 CubeMask
    W3hx=np.zeros(shape=[9,9,9],dtype='int')     # マスク配列回転後
    W3hy=np.zeros(shape=[9,9,9],dtype='int')     # マスク配列 予備 
    W4h=np.zeros(shape=[9,9,9],dtype='int')	# コア配列　最終型
    W4h2=np.zeros(shape=[9,9,9],dtype='int')     # マスク配列　予備
    Wcore=np.zeros(shape=[9,9,9],dtype='int')     # コア配列 原型
    # Q2を三次元化
    dim3(Q2h,W2h)
    # マスクの作成(W3h=CubeMask)
    msk1(W2h,W3h)

    if flag_hint==1:			# 単独未確定ノードを表示
        msk2(W3h,W4h)

    if flag_hint==2:			# 座席予約のコアノードを表示
        flgind,W4h,W1h=IndMask(W3h)

    if flag_hint==3 and flag_hidden==0:	# N国同盟（行）
        W3hx=kcw(W3h)
        mode="ALI-L"
        ext,Wcore,W1h=AliMask(flag_core,W3hx,mode)
        if ext==1:
            W4h=kccw(Wcore)

    if flag_hint==4 and flag_hidden==0:	# N国同盟（列）
        W3hx=jcw(W3h)
        mode="ALI-R"
        ext,Wcore,W1h=AliMask(flag_core,W3hx,mode)
        if ext==1:
            W4h=jccw(Wcore)

    if flag_hint==5 and flag_hidden==0:	# N国同盟（ブロック）
        W3hx=c_to_b(W3h)
        W3hy=jcw(W3hx)
        mode="ALI-B"
        ext,Wcore,W1h=AliMask(flag_core,W3hy,mode)
        if ext==1:
            W4h2=jccw(Wcore)
            W4h=b_to_c(W4h2)

    if flag_hint==3 and flag_hidden==1:    # 隠れN国同盟（行）
        W3hx=kcw(W3h)
        mode="ALI-HL"
        ext,Wcore,W1h=AliMask(flag_core,W3hx,mode)
        if ext==1:
            W4h=kccw(Wcore)

    if flag_hint==4 and flag_hidden==1:    # 隠れN国同盟（列）
        mode="ALI-HR"
        ext,Wcore,W1h=AliMask(flag_core,W3h,mode)
        if ext==1:
            W4h=Wcore

    if flag_hint==5 and flag_hidden==1:    # 隠れN国同盟（ブロック）
        W3hx=c_to_b(W3h)
        mode="ALI-HB"
        ext,Wcore,W1h=AliMask(flag_core,W3hx,mode)
        if ext==1:
            W4h=b_to_c(Wcore)

    if flag_hint==6:	#四辺形の定理（行）
        W3hx=icw(W3h)
        mode="SQ-L"
        ext,Wcore,W1h=AliMask(flag_core,W3hx,mode)
        if ext==1:
            W4h=iccw(Wcore)

    if flag_hint==7:    #四辺形の定理（列）
        W3hx=icw(W3h)
        W3hy=jcw(W3hx)
        mode="SQ-R"
        ext,Wcore,W1h=AliMask(flag_core,W3hy,mode)
        if ext==1:
            W4h2=jccw(Wcore)
            W4h=iccw(W4h2)

    if flag_hint==8:	#強ループ
        mode="ST-LOOP"
        ctrl="1"
        ext,ext2,W1h,Wcore=ChnMaskSt(ctrl,W3h)
        if ext==1:
            W4h=chconv(ext2,Wcore)

    if flag_hint==9:	#弱ループ
        mode="WK-LOOP"
        ctrl="1"
        ext,ext2,W1h,Wcore=ChnMaskWk(ctrl,W3h)
        if ext==1:
            W4h=chconv(ext2,Wcore)


 # クライアントに hint.html を返す
    return render_template('hint.html',sfig=sfig,W3h=W3h,W4h=W4h,flag_hint=flag_hint,flag_core=flag_core,flag_hidden=flag_hidden)

# /sun にアクセスがあれば実行する
@app.route('/sun')
def sun():
    global flag_hint
    flag_hint=1
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /seat にアクセスがあれば実行する
@app.route('/seat')
def seat():
    global flag_hint
    flag_hint=2
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_ali_row（行） にアクセスがあれば実行する
@app.route('/h_ali_row')
def h_ali_row():
    global flag_hint
    flag_hint=3
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_ali_col（列） にアクセスがあれば実行する
@app.route('/h_ali_col')
def h_ali_col():
    global flag_hint
    flag_hint=4
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_ali_blk（ブロック） にアクセスがあれば実行する
@app.route('/h_ali_blk')
def h_ali_blk():
    global flag_hint
    flag_hint=5
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_square_row にアクセスがあれば実行する
@app.route('/h_square_row')
def h_square_row():
    global flag_hint
    flag_hint=6
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_square_col にアクセスがあれば実行する
@app.route('/h_square_col')
def h_square_col():
    global flag_hint
    flag_hint=7
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_st_loop にアクセスがあれば実行する
@app.route('/h_st_loop')
def h_st_loop():
    global flag_hint
    flag_hint=8
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_wk_loop にアクセスがあれば実行する
@app.route('/h_wk_loop')
def h_wk_loop():
    global flag_hint
    flag_hint=9
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_hidden にアクセスがあれば実行する
@app.route('/h_hidden')
def h_hidden():
    global flag_hidden
    if flag_hidden==0:
        flag_hidden=1
    else:
        flag_hidden=0
    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_left にアクセスがあれば実行する
@app.route('/h_left')
def h_left():
    global flag_core
    if flag_core>2:
        flag_core=flag_core-1

    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /h_right にアクセスがあれば実行する
@app.route('/h_right')
def h_right():
    global flag_core
    if flag_core<6:
        flag_core=flag_core+1

    # ヒント画面に遷移させる
    return redirect('/b-hint')

# /hintclr にアクセスがあれば実行する
@app.route('/hintclr')
def hintclr():
    global flag_hint
    flag_hint=0
    # ヒント画面に遷移させる
    return redirect('/b-hint')



if __name__ == '__main__':
    # サーバーを起動
    app.run(
        host='localhost',
        debug=False,
        threaded=True,
        use_reloader=False
    )

