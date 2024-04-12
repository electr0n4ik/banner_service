from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# with app.connection() as connection:
#     scheduler = PersistentScheduler(app, connection=connection)
#     scheduler.remove('run-every-5-minutes')

app.conf.beat_schedule = {
    'run-every-02-minutes': {
        'task': 'main.tasks.my_periodic_task',
        'schedule': timedelta(minutes=0.2),
        'args': (),
    },
}
