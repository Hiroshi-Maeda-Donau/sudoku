#Hough+dilation+rosion
# for import
import cv2
from _detect_corners import *
from _trim_board import *
from server import *

def show_fitted(img, x):
    cntr = np.int32(x.reshape((4, 2)))
    blank = np.copy(img)
    cv2.drawContours(blank, [cntr], -1, (0,255,0), 2)
    return blank

def split_image(img, x, y, line):
    height, width  = img.shape
    h = height//y
    w = width//x
    line_h = round(h*line)
    line_w = round(w*line)
    counter = 0
    for split_y in range(1, y+1):
        for split_x in range(1, x+1):
            counter += 1
            clp = img[ (h*(split_y-1))+line_h:(h*(split_y))-line_h, (w*(split_x-1))+line_w:(w*(split_x))-line_w]
            cv2.imwrite("./raw_img/{}.png".format(counter), clp)
    return counter


#if __name__ == "__main__":
def main_conv():
    raw_img = cv2.imread("./templates/sudoku.png")
    fit_img = fit_size(raw_img, 500, 500)

    print("枠線検出開始")

# 試行範囲***************************************************⬇️

    # グレースケール
    # gray = cv2.cvtColor(fit_img, cv2.COLOR_BGR2GRAY)

    # 閾値の設定
    # threshold = 100
    # threshold = 120     # modified from 100

    # 二値化(閾値100を超えた画素を255にする。)
    # ret,gray2 = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
# 試行範囲****************************************************⬆️

    polies = convex_poly(fit_img, False)#original
    print("枠検出終了")	#***********************************

    # 枠検出の結果チェック
    msg=msg_read()
    print("msg3=",msg)#****************************************

    if msg=="ok":
        poly = select_corners(fit_img, polies)
        print("select corners")	#*********************
        msg=msg_read()
        print("msg2=",msg)#******************************
        if msg=="ok":
            x0 = poly.flatten()
            img = show_fitted(fit_img, x0)
            print("convex_poly_fitted")	#************
            rect, score = convex_poly_fitted(img)
            print("convex_poly_fittedの後")#************
            msg=msg_read()
            print("msg=",msg)#*************************
            if msg=="ok":

                print("画像トリム中")

                trimed = trim_board(raw_img, normalize_corners(rect) * (raw_img.shape[0] / img.shape[0]))

                img=trimed
                img2 = img
                img3 = img

                print("画像変換中")

                # グレースケール
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # 閾値の設定
                # threshold = 100 # original
                threshold = 120	# modified from 100

                # 二値化(閾値100を超えた画素を255にする。)
                ret,gray2 = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)


                ## 反転 ネガポジ変換
                gray3=cv2.bitwise_not(gray2)

#***************膨張・収縮******************************
                kernel = np.ones((5,5),np.uint8)
                dilation = cv2.dilate(gray3,kernel,iterations = 1)
                erosion = cv2.erode(dilation ,kernel,iterations = 1)

##  再反転*****************************************************
                gray4=cv2.bitwise_not(erosion)
                lines = cv2.HoughLinesP(erosion, rho=1, theta=np.pi/360, threshold=80, minLineLength=100, maxLineGap=5)

                print("画像分割中")

                for line in lines:
                    x1, y1, x2, y2 = line[0]

                # 線を消す(白で線を引く)
                    no_lines_img = cv2.line(gray4, (x1,y1), (x2,y2), (255,255,255), 20)

                fimg=no_lines_img

                currentdata=split_image(fimg, 9, 9, 0)

            else:
                currentdata=0
                print("no part1")#********************

        else:
            currentdata=0
            print("no part2")#*************************

    else:
        currentdata=0
        print("msg=",msg)

    return currentdata
