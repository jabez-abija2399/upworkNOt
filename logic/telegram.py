
import requests

class TelegramService:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        # We create the base URL once to avoid rebuilding it every time
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, text):
        """Sends a text message via the Telegram Bot API."""
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML" 
        }
        
        try:
            response = requests.post(self.api_url, data=payload)
            response.raise_for_status() 
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False
