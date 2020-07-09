from flask import Flask, request
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
if os.getenv('DEV'):
    from flask_ngrok import run_with_ngrok
    run_with_ngrok(app)

@app.route('/carbonara_webhook/', methods=['POST'])
def carbonara_webhook():
    update = request.get_json()
    message = update.get('message')
    if message:
        image = requests.post(url='https://carbonara.now.sh/api/cook', json={'code' : message['text'], 'backgroundColor': '#1F816D'}).content
        img_bb = requests.post(url='https://api.imgbb.com/1/upload?expiration=60&key=' + os.getenv('IMGBB_KEY'), files={'image' : image}).text
        t_request = requests.post(url='https://api.telegram.org/bot' + os.getenv('TELEGRAM_TOKEN') + '/sendPhoto', json={'chat_id' : message['chat']['id'], 'photo' : json.loads(img_bb)['data']['url']})
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
