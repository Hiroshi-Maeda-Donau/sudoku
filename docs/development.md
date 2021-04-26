## ファイル名と中身の簡単な説明
### 1. SUDOKUディレクトリー直下に置くファイル
- _detect_corners.py 　　数独問題をカメラで読む時の画像調整コード
- _trim_board.py　　　　同上
- convert_web.py　　 　 カメラで読んだ数独問題の画像を81個に分割する
- ocr_web.py　　   　　　81個に分割した画像をデジタル化する
 (上記四つのコードはネットからコピペして私なりに改造したものです。)
- s_access2.py　　　　 カメラで読んだり手入力した数独問題を保存するコード
- s_ceate_web5.py　　　数独問題を発生させるコード
- sudoku_web4.py　　　数独問題を解くコード
- server.py　　　　　　サーバー全体をコントロール
- s_mondai.txt　　　　　数独問題を保存するファイル  
### 2. "templates"ディレクトリの下に置くファイル
- index.html　　　　　メイン画面
- squat.html　　　　　カメラ撮影を行う画面
- hint.html 　　　　　ヒント画面
- anaimage.html 　　撮影した数独問題の画像をを9X9に分割するときの進捗画面
- anaimage2.html 　　9X9に分割した画像をOCRにかける時の進捗画面
- anaimage3.html 　　最終結果の確認画面
- prog.html 　　　　　数独問題自動作成の時表示される画面  
### 3. "static"ディレクトリの下に置くファイル
- style.css　　　　　　CSSファイル
### 4. コードの中で自動生成されるワークファイル ＞
- q_temp.txt　　　　　数独問題を一時保管するファイル
- q_temp2.txt 　　　　OCRで画像を読み取っている途中のデータを一時保存するファイル（進捗表示用）
- q_answer.txt　　　　数独問題の回答を一時保管するファイル
- qptr.txt　　　　　　s_mondai.txtに保存された問題を読み書きする時のポインタ
- message.txt　　　　各コードで発生するメッセージを一時保存するファイル 
- sudoku.png 　　　　カメラで撮影した画像を保存するファイル 
- 1.png~81.png 　　　OCRにかけるために分割した81個の画像

以上のほかにもコード実行中に自動生成されるワークファイルがあります。