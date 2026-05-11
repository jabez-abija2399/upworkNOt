import requests
import feedparser



feed_url = "https://www.upwork.com/ab/feed/jobs/rss?q=reactjs"

feed = feedparser.parse(feed_url)

for entry in feed.entries[:5]:
    title = entry.title
    link = entry.link

    message = f"New Upwork Job:\n{title}\n{link}"

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message}
    )