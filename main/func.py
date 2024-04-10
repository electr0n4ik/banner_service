from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.utils import timezone
from celery import shared_task

@shared_task
def create_periodic_task():
    PeriodicTask.objects.filter(name__startswith='i').delete()
    schedule, _ = IntervalSchedule.objects.get_or_create(
            every=300,
            period=IntervalSchedule.SECONDS,
        )
    task = PeriodicTask.objects.create(
        interval=schedule,
        name = f'importing_banners_{timezone.now()}',
        task='main.func.update_banner_cache'
    )
    task.save()