
from config import Config 
from logic.telegram import TelegramService 

def run_bot():
    Config.validate()
    tg_service = TelegramService(Config.BOT_TOKEN, Config.CHAT_ID)
    print("Starting bot...")
    tg_service.send_message("<b>Bot Started!</b> I am now watching for jobs.")

if __name__ == "__main__":
    run_bot()
