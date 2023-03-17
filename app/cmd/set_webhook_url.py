import sys
from os import environ

from dotenv import load_dotenv
from linebot import LineBotApi

load_dotenv(".env", verbose=True)

if not (access_token := environ.get("LINE_CHANNEL_ACCESS_TOKEN")):
    raise Exception("access token is not set as an environment variable")

LineBotApi(access_token).set_webhook_endpoint(sys.argv[1] + "/callback")
