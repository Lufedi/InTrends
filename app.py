from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask import request
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from models import Terms, Jobs
from cron import cron
from services import query_service

from dto.dtos import *
from services.term_service import TermService
termService = TermService()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/terms")
def terms():
    terms = termService.get_terms()
    schema = TermSchema(many=True)
    result = schema.dump(terms).data
    return jsonify(result)

@app.route("/terms/records")
def jobs():
    term = request.args.get('t')
    schema = JobsSchema(many=True)
    jobs = termService.get_jobs(term)
    result = schema.dump(jobs).data
    return jsonify(result)


@app.route("/query")
def query():
    query_service.query_updates()
    return "done"



'''


'''

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


