import time
import atexit
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from services.query_service import query_updates


scheduler = BackgroundScheduler()
scheduler.add_job(func=query_updates, trigger="interval", seconds=3600, next_run_time=datetime.datetime.now())
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())