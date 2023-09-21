import os 
from celery import Celery

BROKER_URI = os.environ['BROKER_URI']
BACKEND_URI = os.environ['BACKEND_URI']
celery_app = Celery(
    "task_queue", 
    broker=BROKER_URI,
    backend=BACKEND_URI,
    )
celery_app.control.purge()

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))