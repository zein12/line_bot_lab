# line_auth_init.py
# encoding=UTF-8
import os
import sys
from linebot import (
    LineBotApi, WebhookHandler
)

CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET', None)

if CHANNEL_ACCESS_TOKEN is None:
    print('(Error) Need to specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
if CHANNEL_SECRET is None:
    print('(Error) Need Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)