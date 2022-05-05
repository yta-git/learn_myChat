// コードはWebサイト開発でどれもよく利用するものばかりなので丸覚えでも良いかも

// 自分のネットワーク環境に合わせ変更する
// 特にHOSTは自分のPCのプライベートIPアドレスを入れる
const HOST = '192.168.200.52';
const PORT = '3000'

// windowの読み込みが完了したら実行される
window.onload = () => {
    // エンドポイントのURL
    const api_endpoint = `http://${HOST}:${PORT}/message`

    // HTML要素をIDから取得
    const message_container_el = document.getElementById('message-container')
    const submit_button_el = document.getElementById('submit-button')
    const user_name_el = document.getElementById('user-name')
    const message_textarea_el = document.getElementById('message-textarea')

    // メッセージを画面に描写する必要があるかを判定する変数
    // メッセージ総数を格納する変数
    let messages_length = -1

    // APIから受け取ったメッセージを画面に描写する関数
    // messages: Object Array
    /* 一例
    [
        {
            "id": 1,
            "user_name": "user1",
            "message": "message1",
            "date": "2021/11/28 11:25:57",
        },
        {
            "id": 2,
            "user_name": "user2",
            "message": "message2",
            "date": "2021/11/28 11:25:59",
        }
    ]
    */
    const update_message_view = (messages) => {
        // 取得したメッセージ総数に変化がなかったら何もしない
        if (messages_length === messages.length) {
            return
        }
        // 受け取ったメッセージ総数を格納
        messages_length = messages.length
        // 受け取ったすべてのメッセージを描写するためのHTML文字列を生成する
        let updated_html = ''
        // 受け取ったメッセージをループしてそれぞれをupdated_htmlに連携する
        const sanitize = (str) => str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;')
        // サニタイズ関数
        // ユーザの入力はXSSに気をつけよう
        messages.forEach(item => {
            updated_html += `
            <!-- class: message-group 1メッセージごとのグループ -->
            <div class="message-group">
                <!-- class: message-property メッセージのプロパティ情報 -->
                <div class="message-property">
                    <!-- class: message-id メッセージごとのID -->
                    <span class="message-id">${item.id}</span>
                    <!-- class: message-user-name メッセージごとのユーザ名 -->
                    <span class="message-user-name">${sanitize(item.user_name)}</span>
                    <!-- class: message-date メッセージごとの日付 -->
                    <span class="message-date">${item.date}</span>
                </div>
                <!-- class: message-text メッセージのテキスト -->
                <span class="message-text">${sanitize(item.message)}</span>
            </div>`
        })
        // message_container内のHTMLを更新しメッセージを画面に描写する
        message_container_el.innerHTML = updated_html
        // メッセージを画面に描写したら一番下にスクロールする
        message_container_el.scrollTop = message_container_el.scrollHeight
    }

    // メッセージをすべて取得し,メッセージを画面に描写する
    // GET /message
    const get_messages = () => axios.get(api_endpoint)
        .then(response => { // 取得したメッセージを画面に描写する
            const messages = response.data
            update_message_view(messages)
        })
        .catch(error => console.log(error)) // エラー時はエラー内容をコンソールに出力する

    // メッセージを送信する関数
    const post_message = () => {
        // ユーザ名をテキストエリアから取得する
        const user_name = user_name_el.value
        // メッセージをテキストエリアから取得する
        const message = message_textarea_el.value

        // POST /message
        // リクエストボディはJSON形式で次のようなオブジェクトを渡す
        /* 一例
        {
            "user_name": "user1",
            "message": "message1"
        }
        */
        axios.post(api_endpoint, {
                user_name: user_name,
                message: message
            })
            .then(response => get_messages()) //送信したメッセージも含め画面に描写する
            .catch(error => console.log(error))// エラー時はエラー内容をコンソールに出力する
    }

    // Webサイトにアクセスしたら,メッセージをすべて取得し画面に描写する
    get_messages()

    // 1秒ごとにメッセージを取得し,メッセージを上書き描写する
    // 注意: これは普通のシステムではありえないが,ハッカソンなので今回はこうする
    setInterval(() => get_messages(), 1000)

    // メッセージを送信するボタンをクリックしたらメッセージを送信する
    submit_button_el.addEventListener(
        'click', () => post_message()
    )

    // Enterが押されたら,メッセージを送信する
    message_textarea_el.addEventListener(
        'keydown',
        (event) => {
            if (event.key === 'Enter') {
                post_message()
            }
        }
    )
}
