# chatGPT LineBot Python

Python で chatGPT の LINEBot を作ってみた件

## Supported Python version

- 3.8
- 3.9
- 3.10
- 3.11

## Related Documents

このリポジトリでは chatGPT, LINEBot, ngrokを使用しているよ。

- chatGPTのAPIキーの取得

    <https://platform.openai.com/account/api-keys>

    上記のURLからAPIキーを取得してね。アカウントを作ってない人は作ってね。

- LINEBotの作成、および設定

    <https://qiita.com/nanato12/items/25e2db9461bb6ac2b8c5>

    APIを使用してLINEBotを動かすための作成方法や設定を記事にしているから、まだBot用のアカウントを作成してない人は作成してね。

- ngrokが使えるようにする

    <https://ngrok.com/download>

    上記のリンクにダウンロード方法がOS別に載ってるからセットアップしてね。

## Setup

最初に実行してね

```bash
$ python -m venv venv
$ . venv/bin/activate
$ make init
```

## Set environment variables

`.env` に以下の情報を書き込んでね

- chatGPTのAPIキー
- LINE公式アカウントのチャンネルシークレット
- LINE公式アカウントのアクセストークン

## Run

### 1. flask でアプリを起動

```bash
$ make run
```

or

```bash
$ python main.py
```

### 2. 別タブで `ngrok` を起動

```bash
$ make ngrok
```

or

```bash
$ ngrok http 3000
```

[LINE Developer Console](https://developers.line.biz/console/) にアクセスして、使用するアカウントの Webhook URL に ngrokで出力された https の `Forwarding` リンクを貼り付ければOK

エンドポイントは `/callback` なので注意

例:

```plain
ngrok by @inconshreveable                                                                                                                                                      (Ctrl+C to quit)

Session Status                online
Account                       ななといつ (Plan: Free)
Update                        update available (version 2.3.41, Ctrl-U to update)
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://ccd5-194-195-89-90.ngrok.io -> http://localhost:3000
Forwarding                    https://ccd5-194-195-89-90.ngrok.io -> http://localhost:3000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

↑の場合、webhook URLは `https://ccd5-194-195-89-90.ngrok.io/callback` となる。
