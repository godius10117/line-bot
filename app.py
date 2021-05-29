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

line_bot_api = LineBotApi('7xG2VUTUNTnlalFJ6fx6k5P1pAalY5BQg0+G/VwAzJZZ5iE5+naGsclPVJ35duwuYfudKoNfkdARe/ojmD2xbY3EQ5ott+zxPdBpUWtUG8953mQEzSTFeBIqynptpBZGH9+O4yEEoBNIZ2QM5xmVcAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('8bf8bd66af30a83ab268a105ccf9dbd3')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()