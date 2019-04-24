from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask import request
from flask_cors import CORS

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
CORS(app)

from models import Terms, Jobs
from cron import cron
from services import query_service

from dto.dtos import *
from services.term_service import TermService
from services.job_service import JobService


term_service = TermService()
job_service = JobService()

@app.route("/")
def hello():
    return "Welcome to InTrends"

@app.route("/schedules")
def schedules():
    return jsonify(cron.get_schedules())

@app.route("/terms")
def terms():
    terms = term_service.get_terms()
    schema = TermSchema(many=True)
    result = schema.dump(terms).data
    return jsonify(result)

@app.route("/terms/records")
def jobs_by_term():
    term = request.args.get('t')
    schema = JobsSchema(many=True)
    jobs = term_service.get_jobs(term)
    result = schema.dump(jobs).data
    return jsonify(result)


@app.route("/query")
def query():
    query_service.query_updates()
    return "done"


@app.route("/jobs")
def jobs():
    schema = JobsSchema(many=True)
    jobs = job_service.get_jobs()
    result = schema.dump(jobs).data
    return jsonify(result)

@app.route("/jobs/total")
def total_jobs():
    return str(job_service.total())

'''t = Term.query.get(1)
j = Job(location='us:0', total=100000, term=t)
db.session.add(j)
db.session.commit()'''



'''from app.models.Terms import Term
from app.models.Jobs import Job

terms = ['django', '.net core', 'gcp', 'google cloud', 'azure', 'android', 'spring boot']
for te in terms:
    t = Term(term=te)
    db.session.add(t)
    db.session.commit()'''


