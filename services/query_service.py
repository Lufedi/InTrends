from linkedin_api import Linkedin

from app import db
from app import app
from models.Terms import Term
from models.Jobs import Job




# Authenticate using any Linkedin account credentials
def query_updates():
    app.logger.info('running query updates')
    api = Linkedin('pipediaz94@hotmail.com', 'prueba1020')
    location_name = 'Estados Unidos'
    location_id = 'us:0'
    terms = Term.query.all() 
    for term in terms:
        _total = api.searchTotal({
            'keywords': term.term, 
            'location': location_name, 
            'locationId': location_id, 
            'type': 'JOBS', 'query': 'search',
        })
        job = Job(location=location_id, total=_total, term=term)
        app.logger.info(f'updated {term.term} : {_total}')
        db.session.add(job)
        db.session.commit()
    app.logger.info("finished querying")