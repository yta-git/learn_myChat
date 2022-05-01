# APIサーバはPythonでなくても開発できるので
# 特に覚えてほしいのはコードではなく,APIサーバの作り方や関連知識

# 外部ライブラリ
# flaskと呼ばれ人気のあるWebアプリケーションフレームワーク
# flaskの使い方
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
from flask import Flask, jsonify, request

# flask_corsと呼ばれるflaskの拡張モジュールで,CORSを扱うのに利用
# CORSとは
# https://developer.mozilla.org/ja/docs/Web/HTTP/CORS
# flask_corsの使い方
# https://flask-cors.readthedocs.io/en/latest/
from flask_cors import CORS

# 標準ライブラリ
# 日付を扱う
from datetime import datetime

# HTTP Response Status Codeの定数宣言
# HTTP Status とは
# https://developer.mozilla.org/ja/docs/Web/HTTP/Status
from http import HTTPStatus

# JSONと呼ばれるデータフォーマットを扱う
# JSONとは
# https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global_Objects/JSON
import json


# メッセージを保存するためJSONファイル
# 本来のシステムはメッセージを保存するためのデータベースを持つが,
# 今回は開発の速さを優先してJSONファイルを利用する
db_json_path = "db.json"

# flaskのインスタンスを生成
app = Flask(__name__)

# CORSの設定
# 今回は外部からの全てのリクエストを許可する
CORS(app)

# file_path: str
# JSONファイルのパスを指定してファイルを読み込み,返り値としてディクショナリを返す
def read_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


# db_json: dict or dict list
# 引数として渡されたJSONディクショナリをDB.jsonに書き込む
def update_db_json(db_json):
    with open(db_json_path, "w") as f:
        json.dump(db_json, f, indent=4)


# req_body_json: dict
# /message APIにPOSTリクエストで渡されたJSON Object(HTTP Request Body)
# にidを追加し,それをdb.jsonに書き込む
# req_body_jsonの一例
"""
{
    "id": 2,
    "user_name": "Taro",
    "message": "Bye!",
    "date": "2020/01/02 00:00:00"
}
"""


def insert_message_to_db_json(req_body_json):
    # db.json(JSON配列)を読み込む
    db_json = read_json(db_json_path)
    # db_jsonの一例
    """
    [
        {
            "id": 1,
            "user_name": "Hanako",
            "message": "Hello!",
            "date": "2020/01/01 00:00:00"
        }
    ]
    """

    # req_body_json(JSON Array)にmessage_idを追加する
    # 初期IDは1でそれ以降は最新のID+1をIDとする
    message_id = 1
    if len(db_json) > 0:
        message_id = db_json[-1]["id"] + 1
    req_body_json["id"] = message_id

    # db_jsonにreq_body_jsonを追加する
    db_json.append(req_body_json)

    # ファイルdb.jsonを更新
    update_db_json(db_json)

    # この時点でのdb.jsonの中身
    """
    [
        {
            "id": 1,
            "user_name": "Hanako",
            "message": "Hello!",
            "date": "2020/01/01 00:00:00"
        },
        {
            "id": 2,
            "user_name": "Taro",
            "message": "Bye!",
            "date": "2020/01/02 00:00:00"
        }
    ]
    """


# HTTP Requestとは
# https://developer.mozilla.org/ja/docs/Web/HTTP/Methods

# エンドポイント /message
# メソッド: GET
# リクエストヘッダ: 無し
# リクエストボディ: 無し
# レスポンスとしては,db.jsonの中身をJSON配列として返す
# レスポンスの例
"""
[
    {
        "id": 1,
        "user_name": "Hanako",
        "message": "Hello!",
        "date": "2020/01/01 00:00:00"
    },
    {
        "id": 2,
        "user_name": "Taro",
        "message": "Bye!",
        "date": "2020/01/02 00:00:00"
    }
]
"""


@app.route("/message", methods=["GET"])
def get_message():
    # db.json(JSON配列)を読み込む
    db_json = read_json(db_json_path)
    # ディクショナリをJSON配列に変換し,レスポンスとして返す
    return jsonify(db_json)


# エンドポイント: /message
# メソッド: POST
# リクエストヘッダ: 無し
# リクエストボディー: JSON Object
# リクエストボディーの一例
"""
{
    "id": 2,
    "user_name": "Taro",
    "message": "Bye!",
    "date": "2020/01/02 00:00:00"
}
"""
# レスポンスとしては,正常に処理が終了した場合
# {"status": "ok"} を返す
# エラーが発生した場合は,{"status": "ng", "message": "エラー詳細"}を返す
@app.route("/message", methods=["POST"])
def post_message():
    # リクエストボディーをJSON Objectとして取得
    request_json = request.json

    # 受け取ったJSON Objectからuser_nameを受け取る
    user_name = request_json.get("user_name")
    # user_nameが文字列であるか確認
    if type(user_name) is not str:
        # user_nameが文字列でない場合はエラーを返す
        return (
            jsonify({"status": "ng", "message": "user_name is invalid"}),
            HTTPStatus.BAD_REQUEST,
        )
    message = request_json.get("message")
    # messageが文字列であるか確認
    if type(message) is not str:
        # messageが文字列でない場合はエラーを返す
        return (
            jsonify({"status": "ng", "message": "message is invalid"}),
            HTTPStatus.BAD_REQUEST,
        )

    # messageがresetであった場合は,メッセージをすべて削除する
    if message == "reset":
        # db.jsonを空にする
        update_db_json([])
        # 削除完了
        return jsonify({"status": "ok"}), HTTPStatus.OK
    # メッセージが送信されたときの日付文字列を取得
    date_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # 受け取ったJSON Objectをdb.jsonに追加
    insert_message_to_db_json(
        {"user_name": user_name, "message": message, "date": date_str}
    )

    # メッセージを正常に追加したことを知らせる
    return jsonify({"status": "ok"}), HTTPStatus.OK


if __name__ == "__main__":
    # メッセージをすべて削除する
    update_db_json([])
    # ローカルに3000番ポートでサーバーを起動
    # デバッグモードは有効にする
    app.run(host="xxx.xxx.xxx.xxx", port=3000, debug=True)
