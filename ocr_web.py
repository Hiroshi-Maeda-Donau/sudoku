# tesseractを使用したOCR
# for web

import copy
from PIL import Image
import sys
import pyocr
import pyocr.builders
import cv2
import numpy as np

def main_ocr():

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)

    tool = tools[0]
    lang = 'eng'

    row_list = []
    res_list = []

    print("画像読み取り中")

    # 9X9の表作成
    WX=np.zeros(shape=[9,9],dtype='int')
    #WX=np.zeros(shape=[9,9],dtype='unicode')
    rstr=""

    for x in range(9):
        for y in range(9):

            z=9*x+y+1

            img=cv2.imread("./raw_img/{}.png".format(z))

            # 白黒反転
            img2=cv2.bitwise_not(img)

            # RGB変換と白黒変換
            img3=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)
            img4=cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)

            # 画像データをモデルの入力形式に合わせる
            img5=cv2.resize(img4,(50,50))

            # 空欄判定：白ドットの数<20,000
            num=np.sum(img5)

            #print("カラム番号",z,"=",end="")	#******************************

            if num<20000:
                rstr=rstr+"0"
                print("カラム番号",z,"=空欄")	#*****************************************

                # for anaimage.html
                #f=open("./templates/q_temp2.txt", "w")
                #f.write(rstr)
                #f.close 

                yield rstr

            else:

                # 画像の前処理を実行
                text = tool.image_to_string(
                Image.open("./raw_img/{}.png".format(z)),
                lang=lang,
                # builder=pyocr.builders.DigitBuilder()
                #6 = Assume a single uniform block of text.
                builder=pyocr.builders.DigitBuilder(tesseract_layout=6)
                #builder=pyocr.builders.TextBuilder(tesseract_layout=6)
                #builder=pyocr.builders.DigitBuilder(tesseract_layout=4)
                )

                # 表入力
                if text=='1' or text=='2' or text=='3' or text=='4' or text=='5' or text=='6' or text=='7' or text=='8' or text=='9':
                    WX[x,y]=text
                    rstr=rstr+str(text)
                    print("カラム番号",z,"=",text)	#************************************
                else:
                    print("カラム番号",z,"=不明")
                    rstr=rstr+"0"

                # for anaimage.html
                #f=open("./templates/q_temp2.txt", "w")
                #f.write(rstr)
                #f.close 

                yield rstr

    f=open("./templates/q_temp2.txt", "w")
    f.write(rstr)
    f.close 

    #print(WX)
    np.savetxt('q_temp.txt' , WX)

