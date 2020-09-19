## 数独システムの組み立て方
### 使用ハードウェア（各一個） 

1. [Raspberry Pi 3B+](http://akizukidenshi.com/catalog/g/gM-13470/)
2. [7インチ タッチディスプレイ](http://akizukidenshi.com/catalog/g/gM-11674/)
3. microSDカード 8GB以上
4. Picameraモジュール
5. ディスプレイケース(オプション)  
6. Raspberry Pi用電源またはバッテリーチャージャー

- 簡単なセットアップの手順については下記にまとめています。バッテリーチャージャーとRaspberry Piを接続する際は、microUSBコネクタのケーブルが必要です。

### 組み立て方  

- まずOSの準備から始めます。装置組み立て後はSDカードを取り出せないからです。

1. PCにSDカードを直接接続します

2. まずRaspbianをダウンロードします(**2020-02-13-raspbian-buster.zipを使用しました**)。
3. この圧縮ファイルを解凍します。
4. 解凍したイメージファイルを[Etcher](https://www.balena.io/etcher/)を使用してSDカードにコピーします。
5. `/Volumes/boot`下にwpa_supplicant.confを作成します。"YOUR SSID"はあなたのWiFi環境に置き換えて下さい（""は消さないで下さい）。

```config
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev update_config=1
country=JP
network={
    ssid="YOUR SSID"
    psk="YOUR PSK"
    key_mgmt=WPA-PSK
}
```

6. ファイル名sshの空ファイルを作成する

7. SDカードの boot 直下にある config.txt テキストエディタで開き、下記の行を末尾に追加してください。   
      **lcd_rotate=2**

8. SDカードをPC殻取り外し、Raspberry PiにSDカードとカメラを接続します。  
 - カメラケースは使用するとLCDケースに固定することができなくなるので、工夫が必要です。  
 - 私はカメラ基板が剥き出しなのが嫌だったのでカメラケースを取りつけ、両面テープでLCDケースに固定しました。

9. ディスプレイにケースを取り付けます。

10. MicroUSBポートにアダプターかバッテリーチャージャーから電源を接続し、少し間をおいてデスクトップ画面が表示されれば起動完了です。

### ソフトウェアの準備

1. IPアドレスを調べます。  
- ディスプレイの適当な場所をタッチし、WiFiのマークにスライドさせてカーソルを置くことで、IPアドレスが確認できます (そのままタッチすると接続できるSSIDの一覧が表示されます) 。

2. SSHログインを行います。  
 - VSCodeからRaspberry PiのターミナルにSSHログインします。

3. 接続先を登録します。  
- ターミナルから下記を実行する  
$ ssh pi@YOUR_IP_ADDRESS -o StrictHostKeyChecking=no

4. 登録内容確認(config)  
Host YOUR_IP_ADDRESS
HostName YOUR_IP_ADDRESS
 User pi
StrictHostKeyChecking no

5. Raspberry Piの基本設定を行います。  
<1> raspi-configメニューからPicameraの有効化を行って下さい。  
<2> raspi-configメニューからホストネームを下記に変更して下さい。  
**aidev-5**  
(他の名称でも構いませんが、他の関連するコードも変更する必要があります。)

6. 再度SSH接続を行い、下記コマンドを実行し、カメラの接続を確認  
<1> $ vcgencmd get_cameraを実行  
<2> supported=1 detected=1となることを確認