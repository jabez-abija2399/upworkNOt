
import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """
    A class to hold our configuration values. 
    Using a class keeps things organized and prevents global variable mess.
    """
    BOT_TOKEN = os.getenv("BOT_TOKEN") 
    CHAT_ID = os.getenv("CHAT_ID")
    UPWORK_FEED_URL = "https://www.upwork.com/ab/feed/jobs/rss?q=reactjs"

    @staticmethod
    def validate():
        """Helper to ensure we have everything we need to start"""
        if not Config.BOT_TOKEN or not Config.CHAT_ID:
            raise ValueError("❌ BOT_TOKEN or CHAT_ID missing in .env file!")
