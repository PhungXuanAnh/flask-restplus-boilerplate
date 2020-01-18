import logging
from app.main.worker.celery_app import celery as app

LOG = logging.getLogger('celery')


@app.task
def add(x, y):
    # FIXME: this task can not be called, fix this
    LOG.debug('###################### -------------- this is task add')
    return x + y
