# logic/filter.py

class FilterService:
    def __init__(self, keywords):
        """
        Initialize the filter with a list of keywords.
        We lowercase and strip whitespace from each keyword.
        """
        # [MENTOR NOTE]: List comprehensions are a professional way to process lists in one line
        self.keywords = [k.lower().strip() for k in keywords]

    def is_match(self, job):
        """
        Checks if any of our keywords exist in the job title or description.
        """
        # We combine title and description so we only have to search once
        content = (job.title + " " + job.description).lower()
        
        # We use a loop to check each keyword
        for word in self.keywords:
            if word in content:
                # If we find a match, we return True immediately (early exit)
                return True
        
        # If the loop finishes without finding anything, return False
        return False
