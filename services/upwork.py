import feedparser 
from dataclasses import dataclass 

@dataclass
class Job:
    """A simple container for our job data"""
    title: str
    link: str
    description: str

class UpworkService:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_latest_jobs(self) -> list[Job]:
        feed = feedparser.parse(self.feed_url)
        
        jobs = []
        for entry in feed.entries[:10]: 
            new_job = Job(
                title=entry.get('title', 'No Title'),
                link=entry.get('link', ''),
                description=entry.get('description', '')
            )
            jobs.append(new_job)
            
        return jobs
