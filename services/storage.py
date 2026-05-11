import json 
import os 

class StorageService:
    def __init__(self, filename="sent_jobs.json"):
        self.filename = filename
        self.sent_jobs = self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return [] 

    def save(self, job_id):
        if job_id not in self.sent_jobs:
            self.sent_jobs.append(job_id)
            with open(self.filename, "w") as f:
                json.dump(self.sent_jobs, f, indent=4)

    def is_new(self, job_id):
        return job_id not in self.sent_jobs
