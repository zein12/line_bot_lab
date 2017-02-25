# bot_app.py
# encoding=UTF-8
"""
Line bot practice
"""
import os
import re
import sys
from argparse import ArgumentParser
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import line_auth_init
from botactions import bot_actions

user_guide_desc = '''
Hei, aku Runner, saya hanya bisa membiarkan Anda menggunakan kamus, penggunaan adalah: \ n
Awal dic pertarungan + Ingin memeriksa sebuah kata, misalnya,: dic apple apple akan dapat mengetahui interpretasi Cina
'''


class ParseAction():
    """Keep parse result and mapping to related function"""
    def __init__(self):
        self.language = None
        self.text_msg = None
        self.kw_args = {}
        self.is_support = False
        self.to_do_function = None

    def check_support(self, language):
        self.language = language
        self.is_support = True

    def preprocess_text_msg(self, text):
        if text:
            self.text_msg = text.strip()

    def assign_function(self, function_name):
        if function_name:
            self.to_do_function = function_name


app = Flask(__name__)

#For Test
@app.route("/", methods=["GET"])
def index():
    return "Hello World", 200

#Line API Callback Entrance
@app.route("/callback", methods=["POST"])
def callback():
    """Line Bot API callback entrance"""
    # get X-Line-Signature header
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: "+ body)

    # handle webhook body
    try:
        line_auth_init.handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@line_auth_init.handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Process for incoming message"""
    msg = event.message.text
    # 以物件來接是為了讓回應時可以同時支援單一物件或串列2種api參數
    replyObj = None
    reply = ''
    parse_result = init_parse_text(msg)
    if not parse_result.is_support:
        reply = user_guide_desc
        replyObj = TextSendMessage(text=reply)
    elif parse_result.to_do_function:
        replyObj = getattr(bot_actions, parse_result.to_do_function)(parse_result.text_msg, event)
    else:
        reply = 'Kakek saya tidak tahu apa yang ingin Anda lakukan, tapi untuk mengulang apa yang Anda katakan teman ~ \ n'+ msg
        replyObj = TextSendMessage(text=reply)

    if replyObj:
        print(replyObj) #For server log
        line_auth_init.line_bot_api.reply_message(
            event.reply_token,
            replyObj)


def init_parse_text(text):
    """Parse incoming text message and mapping function.
    Args:
        text: pure utf-8 text
    Return:
        Object of ParseAction type
    """
    parse_text = ParseAction()
    print("variable text:"+text) #For debug
    parse_text.preprocess_text_msg(text)
    # if is empty message, return silence
    if len(parse_text.text_msg) == 0:
        parse_text.assign_function('silence')
        parse_text.check_support('zh-TW')

    if re.match(r'^[Dd][Ii][Cc] ', parse_text.text_msg):
        parse_text.assign_function('lookup_eng_dic')
        parse_text.check_support('en-US')

    if re.match(r'^Siapakah Aku |^Siapakah akus', parse_text.text_msg) or re.match(r'^[Pp]rofile$', parse_text.text_msg):
        parse_text.assign_function('get_profile')
        parse_text.check_support('zh-TW')

    if re.match(r'^你是誰|^你誰', parse_text.text_msg):
        parse_text.assign_function('general_qa')
        parse_text.check_support('zh-TW')

    return parse_text

# run app
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    #port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', debug=options.debug, port=options.port)
