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
            # [MENTOR NOTE]: We now loop through each URL in our list
            for url in Config.UPWORK_URLS:
                logging.info(f"Checking feed: {url}")
                
                # We update the service with the current URL before fetching
                upwork_service.feed_url = url.strip()
                jobs = upwork_service.fetch_latest_jobs()
                
                for job in jobs:
                    # First check: Is it new?
                    if storage.is_new(job.link):
                        
                        # Second check: Does it match our interests?
                        if my_filter.is_match(job):
                            logging.info(f"🎯 MATCH FOUND: {job.title}")
                            
                            # --- PROFESSIONAL FORMATTING ---
                            message = Formatter.format_telegram(job)
                            
                            if tg_service.send_message(message):
                                storage.save(job.link)
                        else:
                            storage.save(job.link)
                    else:
                        pass 

        except Exception as e:
            logging.error(f"⚠️ Error in main loop: {e}")

        
        # Wait for 10 minutes to avoid getting blocked by Upwork
        logging.info("Waiting 10 minutes before next check...")
        time.sleep(600) 

if __name__ == "__main__":
    run_bot()

