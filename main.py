import time 
import logging # The professional way to track app activity
from config import Config 
from logic.telegram import TelegramService 
from services.upwork import UpworkService 
from services.storage import StorageService 
from logic.filter import FilterService # Import our new filter logic
from logic.formatter import Formatter # Import our new formatting tool

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
    upwork_service = UpworkService(Config.UPWORK_URLS[0])
    storage = StorageService() # Memory
    my_filter = FilterService(Config.KEYWORDS, Config.BLACKLIST) # Brain
    
    logging.info(f"Watching for keywords: {Config.KEYWORDS}")

    while True: # Infinite loop for automation
        try:
            # [MENTOR NOTE]: We now loop through each URL in our list
            for url in Config.UPWORK_URLS:
                logging.info(f"🔍 Checking feed: {url}")
                
                upwork_service.feed_url = url.strip()
                jobs = upwork_service.fetch_latest_jobs()
                
                if not jobs:
                    logging.warning(f"⚠️ No jobs found at all in this feed URL.")

                for job in jobs:
                    # Check if already sent
                    if not storage.is_new(job.link):
                        logging.debug(f"⏭️ Skipping (Already Seen): {job.title[:30]}...")
                        continue
                    
                    # Check if it matches our keywords/blacklist
                    if my_filter.is_match(job):
                        logging.info(f"✅ MATCH FOUND: {job.title}")
                        
                        message = Formatter.format_telegram(job)
                        if tg_service.send_message(message):
                            storage.save(job.link)
                    else:
                        # Log WHY it was skipped (This is the fix for the "silence"!)
                        logging.info(f"❌ Skipping (No Keyword Match): {job.title[:40]}...")
                        storage.save(job.link) # Still save it so we don't re-scan


        except Exception as e:
            logging.error(f"⚠️ Error in main loop: {e}")

        
        # Wait for 10 minutes to avoid getting blocked by Upwork
        logging.info("Waiting 10 minutes before next check...")
        time.sleep(600) 

if __name__ == "__main__":
    run_bot()

