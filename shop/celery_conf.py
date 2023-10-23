from celery import Celery
from datetime import timedelta
import os

celery_app = Celery('shop')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')



celery_app = Celery('shop')
# Below command runs tasks that they are in task.py module(in apps).
celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://guest:guest@0.0.0.0:5672'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 4
