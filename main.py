import time 
import logging # The professional way to track app activity
from config import Config 
from logic.telegram import TelegramService 
from services.upwork import UpworkService 
from services.storage import StorageService 
from logic.filter import FilterService # Import our new filter logic

# [MENTOR NOTE]: Setting up basicConfig at the start ensures all logs follow the same format
logging.basicConfig(
    level=logging.INFO, # We only want to see INFO or higher
    format='%(asctime)s - %(levelname)s - %(message)s', # Add timestamps and log levels
    handlers=[
        logging.FileHandler("bot.log"), # Save logs to a file for later review
        logging.StreamHandler() # Also print logs to the terminal
    ]
)

def run_bot():
    # 1. Validation: Stop early if config is broken
    Config.validate()
    logging.info("🚀 Bot is starting up...")
    
    # 2. Initialization: Create our modular services
    tg_service = TelegramService(Config.BOT_TOKEN, Config.CHAT_ID)
    upwork_service = UpworkService(Config.UPWORK_FEED_URL)
    storage = StorageService() # Memory
    my_filter = FilterService(Config.KEYWORDS) # Brain
    
    logging.info(f"Watching for keywords: {Config.KEYWORDS}")

    while True: # Infinite loop for automation
        try:
            logging.info("Checking for new jobs from Upwork...")
            jobs = upwork_service.fetch_latest_jobs()
            
            for job in jobs:
                # First check: Is it new?
                if storage.is_new(job.link):
                    
                    # Second check: Does it match our interests?
                    if my_filter.is_match(job):
                        logging.info(f"🎯 MATCH FOUND: {job.title}")
                        
                        # Use HTML tags for professional Telegram formatting
                        message = f"<b>🎯 NEW MATCH:</b> {job.title}\n\n🔗 <a href='{job.link}'>View Job</a>"
                        
                        # Only save to history if the message was sent successfully
                        if tg_service.send_message(message):
                            storage.save(job.link)
                    else:
                        # [MENTOR TIP]: We save skipped jobs too so we don't re-filter them!
                        storage.save(job.link)
                else:
                    # Job already seen, ignore it
                    pass 

        except Exception as e:
            # If the internet fails, we don't want the bot to stop!
            logging.error(f"⚠️ Error in main loop: {e}")
        
        # Wait for 10 minutes to avoid getting blocked by Upwork
        logging.info("Waiting 10 minutes before next check...")
        time.sleep(600) 

if __name__ == "__main__":
    run_bot()

