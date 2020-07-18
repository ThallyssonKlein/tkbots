from flask import Flask, request
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
if os.environ.get('DEV', None):
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)

@app.route('/carbonara_webhook/', methods=['POST'])
def carbonara_webhook():
    update = request.get_json()
    message = update.get('message')
    if message and message['text'] != '/start':
        image = requests.post(url='https://carbonara.now.sh/api/cook', json={'code' : message['text'], 'backgroundColor': '#1F816D'}).content
        t_request = requests.post(url='https://api.telegram.org/bot' + os.environ.get('TELEGRAM_TOKEN') + '/sendPhoto', data={'chat_id' : message['chat']['id']}, files={'photo' : image})
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
