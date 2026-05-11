# logic/formatter.py
from bs4 import BeautifulSoup # Industry standard for HTML parsing

class Formatter:
    """
    A utility class to handle all text transformations and cleaning.
    Using @staticmethod because these functions don't need to store any state.
    """

    @staticmethod
    def clean_html(raw_html: str) -> str:
        """
        Removes HTML tags and converts special characters (entities) to normal text.
        """
        if not raw_html:
            return ""
            
        # [MENTOR NOTE]: "lxml" is preferred over "html.parser" because it is faster 
        # and more "forgiving" with broken HTML from RSS feeds.
        soup = BeautifulSoup(raw_html, "lxml")
        
        # Get text with space separators to prevent words from sticking together
        clean_text = soup.get_text(separator=" ") 
        
        # Split and join to remove extra whitespace and newlines (\n)
        return " ".join(clean_text.split())

    @staticmethod
    def format_telegram(job) -> str:
        """
        Constructs a premium-looking HTML message for Telegram.
        """
        # 1. Clean the description
        clean_desc = Formatter.clean_html(job.description)
        
        # 2. Limit the length (Telegram has a 4096 char limit, but short is better)
        limit = 400
        short_desc = clean_desc[:limit] + "..." if len(clean_desc) > limit else clean_desc
        
        # 3. Construct the HTML message
        # [MENTOR NOTE]: Using f-strings with multi-line strings is the cleanest way to build messages
        return (
            f"🚀 <b>NEW OPPORTUNITY FOUND</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📌 <b>Title:</b> {job.title}\n\n"
            f"📝 <b>Description:</b>\n<i>{short_desc}</i>\n\n"
            f"🔗 <a href='{job.link}'>Apply on Upwork</a>"
        )
