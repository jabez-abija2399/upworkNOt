import time 
from config import Config 
from logic.telegram import TelegramService 
from services.upwork import UpworkService 
from services.storage import StorageService 

def run_bot():
    Config.validate()
    
    # Initialize all services
    tg_service = TelegramService(Config.BOT_TOKEN, Config.CHAT_ID)
    upwork_service = UpworkService(Config.UPWORK_FEED_URL)
    storage = StorageService()
    
    print("🚀 Bot is running and watching for jobs...")

    while True:
        try:
            print("\nChecking for new jobs...")
            jobs = upwork_service.fetch_latest_jobs()
            
            for job in jobs:
                if storage.is_new(job.link):
                    message = f"<b>NEW JOB:</b> {job.title}\n\n🔗 <a href='{job.link}'>View Job</a>"
                    
                    if tg_service.send_message(message):
                        storage.save(job.link)
                        print(f"✅ Sent and Saved: {job.title}")
                else:
                    pass 

        except Exception as e:
            print(f"⚠️ An error occurred: {e}")
        
        print("Waiting 10 minutes...")
        time.sleep(600) 

if __name__ == "__main__":
    run_bot()
