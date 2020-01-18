from celery import Celery
from app.main.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery('project_worker',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND,
                include=['app.main.worker.tasks'])
celery.config_from_object('app.main.worker.celeryconfig')
