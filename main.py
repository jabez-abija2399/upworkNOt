from config import Config 
from logic.telegram import TelegramService 
from services.upwork import UpworkService 

def run_bot():
    Config.validate()
    
    tg_service = TelegramService(Config.BOT_TOKEN, Config.CHAT_ID)
    upwork_service = UpworkService(Config.UPWORK_FEED_URL)
    
    print("Fetching jobs...")

    jobs = upwork_service.fetch_latest_jobs()
    
    # 4. Process the jobs
    for job in jobs:
        message = f"<b>{job.title}</b>\n\n🔗 <a href='{job.link}'>View Job</a>"
        tg_service.send_message(message)
        print(f"Sent: {job.title}")

if __name__ == "__main__":
    run_bot()
