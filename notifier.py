import requests

class Notifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_alert(self, asset, signal):
        message = f"{signal['signal']} {asset} @ {signal['entry']:.4f}\nTP: {signal['tp']:.4f}\nSL: {signal['sl']:.4f}"
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Telegram error: {e}")