import os
from celery import Celery

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

celery_app = Celery(
    'project_service_client',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
)