import os

from decouple import config
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE"))
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# CELERY_BEAT_SCHEDULE = {
#     'perform_database_backup': {
#         'task': 'path.to.perform_database_backup',
#         'schedule': crontab(minute=0, hour='*/6'), 
#     },
# }
