from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('gMDOldxiyq7fAe1/yvy8a+0WInjRDEou1C2hfAOZooCPrb0YttgJh0WQ3Yh3tkgSjZoE2Y2ku/WYAFhtHH0Qh7UKUWpGSvjqvDk8QIO/fUs23dvJ/1aRZ8U4xjRmfHnqOQ6fy2xa6+5K24658uyOVQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('71e18ded19f29f7ea9af660cd1423695')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，您說什麼'

    if msg in ['hi', 'Hi', 'hello', 'Hello']:
        r = '嗨!'
    elif msg == '天氣如何':
        r = '請看氣象報告'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '想訂位是嗎?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()