import requests
from .loader import BOT_TOKEN, ADMIN_ID

def send_telegram_message(bot_token, chat_ids, message):
    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=payload)
        return response.json()

