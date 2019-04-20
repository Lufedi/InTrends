from models.Jobs import Job

class JobService(object):
    def get_jobs(self):
        jobs = Job.query.all()
        return jobs
    def total(self):
        jobs = Job.query.all()
        return len(jobs)