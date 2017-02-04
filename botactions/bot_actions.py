# bot_actions.py
# encoding=UTF-8
import requests
from bs4 import BeautifulSoup as bs
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom
)
import line_auth_init

def lookup_eng_dic(text, event):
    """
    :param text: Valid word in utf-8 format for looking up dictionary
    :param event: Event passed by Line message event
    :return: Object of TextSendMessage with look up result
    """
    # 目前前端的合法呼叫是:dic ${word}
    search_word = text.split(' ')
    dictionary_url = 'http://tw.dictionary.search.yahoo.com/search?p='
    dictionary_source = '(資料來源: Yahoo奇摩字典)'
    res = requests.get(dictionary_url+search_word[1])
    soup = bs(res.content, 'html.parser')
    parse_web = soup.find_all('ul', attrs={'class':'compArticleList mb-15 ml-10'})
    output_string = ''
    if parse_web:
        for i in parse_web:
            output_string += (i.text + '\n')
        output_string += dictionary_source
    else:
        output_string = search_word[1]+'在字典中找不到耶'
    return TextSendMessage(text=output_string)


def blahblash(text, event):
    return TextSendMessage(text='??')


def silence(text, event):
    return TextSendMessage(text='...')


def get_profile(text, event):
    result = []
    if isinstance(event.source, SourceUser):
        profile = line_auth_init.line_bot_api.get_profile(event.source.user_id)
        result.append(TextSendMessage(text='我當然知道你是誰，你是' + profile.display_name + '嘛'))
        result.append(TextSendMessage(text='你的名言是~' + profile.status_message))
    else:
        result.append(TextSendMessage(text='抱歉 你哪位?'))
    return result


def general_qa(text, event):
    result = []
    result.append(TextSendMessage(text='我是阿虎啦'))
    result.append(TextSendMessage(text='你應該是想問我可以幹麼，我可以幫你查單字\n開頭打dic + 想查的單字，例如: dic pineapple就能查出pineapple的中文解釋'))
    return result