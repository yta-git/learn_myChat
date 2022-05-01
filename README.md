# MyChat🍻
Webサイト開発勉強用教材

## Webアプリケーション画面
<img src="https://user-images.githubusercontent.com/24666428/143727528-c9384b52-7fa9-4dc9-b1c4-676590432ce3.jpg" width="70%">

## 構成要素とその役割
<img src="https://user-images.githubusercontent.com/24666428/166128021-1b53da61-2de7-46b4-bc24-883104d2df97.jpg" width="70%">


## 依存
- Python3
    インストール参考 https://www.python.org/downloads/
    - pip3 がインストールされていなければ,インストールする
        インストール参考 https://www.python.jp/install/ubuntu/pip.html

## 起動
1. 端末を開く
1. 端末で自分のPCのプライベートIPアドレスを確認する
1. 
    ```sh
    $ ifconfig # 実行結果の一例.今回の場合プライベートIPは192.168.1.50
    ...
    en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        options=400<CHANNEL_IO>
        ether f0:18:98:0c:6e:50 
        inet6 fe80::1853:acf6:2bdf:c5cd%en0 prefixlen 64 secured scopeid 0x6 
        inet 192.168.1.50 netmask 0xffffff00 broadcast 192.168.1.255
        nd6 options=201<PERFORMNUD,DAD>
        media: autoselect
        status: active
    ```
1. 自分のPCのプライベートIPアドレスは `192.168.50` であるという前提で以降の話を進める。
1. 端末で以下を実行しプロジェクトをクローン
    ```sh
    $ git clone https://github.com/TakuKitamura/myChat.git
    ```
1. カレントディレクトリをmyChatに移動
    ```sh
    $ cd myChat
    ```
1. 依存モジュールをインストール
    ```sh
    $ sudo pip3 install -r requirements.txt # flask, flask_cors
    ```
1. `./www/static/mychat.js`をエディタで開きコード1行目の、`const HOST = 'xxx.xxx.xxx.xxx'`という行を`const HOST = '192.168.1.50'`に変更する
1. 端末(myChatディレクトリにいることを確認)で以下を実行しWebサーバーを起動
    ```sh
    $ sudo python3 -m http.server --bind 192.168.1.50 --directory www 80
    ```
1. `./api.py`をエディタで開きコード最終行の、`app.run(host="xxx.xxx.xxx.xxx", port=3000, debug=True)`を`app.run(host="192.168.1.50", port=3000, debug=True)`に変更。
1. 新たな端末(myChatディレクトリにいることを確認)で以下を実行しAPIサーバーを起動
    ```sh
    $ sudo python3 api.py
    ```
9. スマホやPCで http://192.168.1.50 にアクセスする。注意点として、スマホとPCはどちらも同一ネットワーク上(例えば、どちらも同じWi-Fiアクセスポイントに接続しているなど)にいることを確認する。
すると、myChatのWebサイトが表示されるので、メッセージを送信してみるなどする
10. 開発が楽になるようにメッセージで文字列`reset`を送信(ユーザ名は何でも良い)すると、メッセージが全て削除される機能もあるのでそれも試すと良い
11. PWA(Webサイトだけどアプリっぽく使える)にも対応しているので、ぜひお試しを
- ios(参考 https://www.ipodwave.com/iphone/howto/website_home.html)
- android (参考 https://support.google.com/chrome/answer/9658361?hl=ja&co=GENIE.Platform%3DAndroid)
