  ## 自動立ち上げの設定方法
   1. 数独システムが自動で立ち上がるようにする  
      <タッチディスプレイを用いて画面操作を行うため、マウスは非表示にしておく>  
     a. $ sudo apt install -y unclutter  
      <autostart ファイルを格納するディレクトリを作成>  
     b. $ mkdir -p ~/.config/lxsession/LXDE-pi  
     c. Ctrl + N (MacならCmd + N) を入力し、新規ファイルをエディタに開く。  
        ファイルには次の内容を記述する。  
          @xset s off  
          @xset -dpms  
          @unclutter -idle 0  
          @chromium-browser --incognito --kiosk http://localhost:5000  
     d. b.で作成したディレクトリに上記コードをautostart というフ ァイル名で保存する。

   2. WEBサーバーの常駐化  
       <Systemdを使い、Raspberry Piの起動後にWEBサーバーが自動的に立ち上がるように設定します>  
       <nano エディタや vi エディタを使い、Systemd に登録するサービスファイルを記述します>  
       a. $ sudo nano /etc/systemd/system/daily-squat.service  
　　　　 <ファイルの内容は下記の通り>  
                1. [Unit]  
                2. Description=Daily Squat App  
                3. [Service]  
                4. ExecStart=/usr/bin/python3 /home/pi/aikit4/server.py  
                5. Restart=always  
                6. Type=simple  
                7. User=pi  
                8. WorkingDirectory=/home/pi/aikit4  
                9. [Install]  
               10. WantedBy=multi-user.target  

   3. 下記二つのコマンドを実行して下さい。  
       a. $ sudo systemctl daemon-reload  
       b. $ sudo systemctl enable daily-squat.service