from os import environ
from typing import Dict

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, Source, TextMessage, TextSendMessage
from openai.error import InvalidRequestError, OpenAIError

from app.gpt.client import ChatGPTClient
from app.gpt.constants import PROBLEM_OCCURS_TITLE, Model, Role
from app.gpt.message import Message

load_dotenv(".env", verbose=True)

app = Flask(__name__)

if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")

if not (channel_secret := environ.get("LINE_CHANNEL_SECRET")):
    raise Exception("channel secret is not set as an environment variable")

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(channel_secret)

chatgpt_instance_map: Dict[str, ChatGPTClient] = {}


@app.route("/", methods=["GET"])
def index() -> str:
    return "Hello, ChatGPT LINEBot Python."


@app.route("/callback", methods=["POST"])
def callback() -> str:
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent) -> None:
    text_message: TextMessage = event.message
    source: Source = event.source
    user_id: str = source.user_id

    if text_message.text == "リセットして":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{PROBLEM_OCCURS_TITLE}\n\n会話をリセットするよ。"),
        )

    if (gpt_client := chatgpt_instance_map.get(user_id)) is None:
        gpt_client = ChatGPTClient(model=Model.GPT35TURBO)

    gpt_client.add_message(
        message=Message(role=Role.USER, content=text_message.text)
    )

    try:
        res = gpt_client.create()
        res_text: str = res["choices"][0]["message"]["content"]
    except InvalidRequestError as e:
        res_text = f"{PROBLEM_OCCURS_TITLE}\n\n問題が発生したよ。\n一度会話をリセットするよ。\n\n{e.user_message}"
        gpt_client.reset()
    except OpenAIError as e:
        res_text = f"{PROBLEM_OCCURS_TITLE}\n\n問題が発生したよ。\n\n{e.user_message}"

    chatgpt_instance_map[user_id] = gpt_client

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=res_text.strip())
    )
