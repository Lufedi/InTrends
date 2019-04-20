
from models.Terms import Term
from models.Jobs import Job

class TermService(object):
    def get_terms(self):
        terms = Term.query.all()
        return terms
    
    def get_jobs(self, termId):
        jobs = Job.query.filter_by(term_id = termId).all()
        print(jobs)
        return jobs