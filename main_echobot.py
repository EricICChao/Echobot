import json, io, re

from collections import(
    OrderedDict, UserString
)

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, SourceUser
)

app = Flask(__name__)

line_bot_api = LineBotApi('CtiHx1FNF2hRlp3LPiIJ1DvTc5BRQ+XrcMxLQNwompS8SEd3ebWOpDpQL4yX8ZsX+uD1aPfwFbmW6ZEtEgYVD6gp4xFiH05rMo7Gu3LHDWsTseQK9QvPbH+a3VSkGA7DdLyylZzSi8Iif0woNVQvyQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4d8be238bb3516e034acb0d3829eb56d')

#Line的webhook，只接受和回傳str	
#啟動webhook
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body
    body = request.get_data(as_text=True)
    body2 = request.get_json(cache=True)
    app.logger.info("Request body: " + body)


    var = body2['events']
    f = open("user_id.txt", 'wt', encoding = 'utf-8')
    take_user_id = var[0]['source']['userId']
    f.writelines(take_user_id)
    f1 = open("user_message.txt", 'wt', encoding = 'utf-8')
    take_user_message = var[0]['message']['text']
    f1.writelines(take_user_message)
    f.close()
    f1.close()



    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'



"""
	TODO: 
	user_txt_message放到模型
	產生的response
	傳到下面的訊息回覆處理的TextSendMessage()
"""



#處理訊息的回覆
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    take_user_id = 'user_id'  #請輸入使用者id，要用字串
    take_user_message = ''
    f1 = open("user_message.txt", 'rt', encoding = 'utf-8')
    take_user_message = f1.read()
    f1.close()

    line_bot_api.push_message(take_user_id, TextSendMessage(text = take_user_message))



	
@app.route('/')
def root():
    return "伺服器打開了"
if __name__ == "__main__":
    app.run("127.0.0.1", 8000, debug = True)
