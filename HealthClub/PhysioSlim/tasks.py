import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Event
import datetime
from celery.decorators import periodic_task
from celery.task.schedules import crontab



@periodic_task(run_every=(crontab(minute='*/1')), name="delete_expired_events", ignore_result=True)
def delete_expired_events():
    print("task: delete expired events")
    events = Event.objects.all()
    for event in events :
        now = datetime.datetime.now()
        days =( now.date() - event.due.date()).days
        time = now.time() < event.due.time()
        if  days > 0 :
            event.delete()
        elif days == 0:
            if time:
                event.delete()
