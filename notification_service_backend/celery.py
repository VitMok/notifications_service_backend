import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification_service_backend.settings')

app = Celery('notification_service_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# Celery beat tasks
app.conf.beat_schedule = {
    'send_statistic_every_day': {
        'task': 'apps.notifications.tasks.send_message_with_statistic',
        'schedule': crontab(hour='*/24'),
    }
}