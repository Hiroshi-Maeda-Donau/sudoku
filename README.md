# 数独システム

数独問題の作成や、自動回答を行うシステムです。

デバイス前面            | デバイス裏面
:-------------------:|:---------------------:
![デバイス前面](./images/front_view.jpeg) | ![デバイス裏面](./images/rear_view.jpeg)

## このシステムで出来ること

数独問題の作成:

- 数独問題を雑誌や新聞からカメラで取り込む
- 数独問題を画面から入力する
- 数独問題を自動で作成する

数独問題を解く:

- 自動で問題を解く
- 問題のヒントを見ながら手動で解いていく

## インストール手順

数独システムを動かすために必要なライブラリのインストール手順です。  
＜前提条件＞  
- Raspberry Pi 3B+の使用。  
- 数独システムの組み立てが終わり（[装置のセットアップ](./docs/setup.md)参照）、PCとのSSH接続が完了していること。

### 必要なライブラリのインストール  
#### Visual Studio Codeで数独システムとSSH接続を行い、ターミナルから下記の作業を行ってください。  
作業するディレクトリー名は自由です。  
はじめに、パッケージマネージャを更新します。

```shell
sudo apt-get update
```

OCR用のソフトウェアをインストールします。

```shell
sudo apt-get -y install tesseract-ocr
```

OpenCVの依存ライブラリをインストールします。

```shell
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 libatk1.0-0 
sudo apt install -y libcairo-gobject2 lib$
sudo apt install -y libwebp6 libtiff5 libjasper1 libgdk-pixbuf2.0-0
sudo apt install -y libopenexr23 libilmb$
sudo apt install -y libavutil56 libavcodec58 libavformat58 libswscale5
sudo apt install -y libgtk-3-0 libgst$
sudo apt install -y libqtcore4 libqtgui4 libqt4-test
```

### 必要なPythonモジュールのインストール

pipのインストールを行います。

```shell
sudo apt install -y python3-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
```

依存するPythonモジュールをインストールします。

```shell
pip3 install opencv-python==3.4.6.27 -i https://piwheels.org/simple
pip3 install numpy -i https://www.piwheels.org/simple
pip3 install  flask pyocr
pip3 install scipy -i https://www.piwheels.org/simple
```

## 数独システムのインストール

はじめに`git`コマンドをインストールします。

```
sudo apt install git
```


`git clone`コマンドで数独システムをダウンロードします。

```shell
git clone https://github.com/Hiroshi-Maeda-Donau/sudoku.git
cd sudoku/
```

## 自動起動の設定と解除

別資料にある『[自動起動の設定](./docs/automation.md)』を実施してください。

上記が完了したら下記を入力して数独システムを起動します。数独システムの電源を切って再投入しても同じです。

```shell
sudo reboot
```

LCDに冒頭の基本画面が表示されたら完了です。  

自動立ち上げを解除したいときは下記のようにターミナルから入力してください。
```shell
sudo systemctl disable daily-squat.service
```
またVScodeのターミナルから操作ができるようになります。  
再度自動起動の設定を行いたい場合は、下記のコマンドだけでOKです。　　
```shell
sudo systemctl daemon-reload
sudo systemctl enable daily-squat.service
```
## 詳細情報

装置の組み立て方や数独システムの使い方など、詳しい情報はこちらを確認してください。

- [装置のセットアップ](./docs/setup.md)
- [システムの使い方1](./docs/usage.md)
- [システムの使い方2](./docs/usage2.md)
- [カメラでの撮影のコツ](./docs/usage3.md)
- [自動起動の設定](./docs/automation.md)
- [開発情報](./docs/development.md)
- [数独システムのアルゴリズム](./docs/algorithm.md)

## その他

- 本システムはデアゴスティーニの*もっと本気で学ぶIOT*講座で提供されたデバイス、ソフトウェアをベースに私が開発したものです。
- コードについては講座で提供されたものを私が改造したもの、ネットから入手したものを私が改造したもの、私が独自に開発したものが混在しています。
- 本システムはPC自体に移植することはそれほど難しくないと思いますが、私はやっていません。LCDパネルなどの投資が必要ないので自信のある方はお試しください。

## 開発者

- Donauhiro
