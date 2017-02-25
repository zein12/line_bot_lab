# line_auth_init.py
# encoding=UTF-8
import os
import sys
from linebot import (
    LineBotApi, WebhookHandler
)

CHANNEL_ACCESS_TOKEN = os.getenv('3/cEBpOR0mjAMUtnHKrSrx3N6FnMVNPYfXBIwMO6HNGaljxuxTxZz2fGrmZYFwqfV3dvAWMa7FEGrmOONfbZ7or1wxYgpjbtFMS0Mkk+RftjvYSrUpThxAHGiivf2M662z2zM5P8BSKby0dJiBG3GQdB04t89/1O/w1cDnyilFU=', None)
CHANNEL_SECRET = os.getenv(' a6b4b1a80d9f25eb0a719fc92cef7d86 ', None)

if CHANNEL_ACCESS_TOKEN is None:
    print('(Error) Need to specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if CHANNEL_SECRET is None:
    print('(Error) Need Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
