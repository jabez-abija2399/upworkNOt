# logic/filter.py

class FilterService:
    def __init__(self, keywords, blacklist=None):
        """
        Initialize with keywords and an optional blacklist.
        """
        self.keywords = [k.lower().strip() for k in keywords if k.strip()]
        self.blacklist = [b.lower().strip() for b in blacklist if b.strip()] if blacklist else []

    def is_match(self, job):
        """
        Returns True if the job matches keywords and is NOT in the blacklist.
        """
        content = (job.title + " " + job.description).lower()
        
        # 1. Check Blacklist first (Early exit if we hate this job)
        for word in self.blacklist:
            if word in content:
                return False
        
        # 2. Check Keywords
        for word in self.keywords:
            if word in content:
                return True
        
        return False

