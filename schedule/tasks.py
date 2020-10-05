from django.conf import settings

from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_periodic_task, lock_task, db_task

from . import view_funcs
from datetime import datetime

from .models import ScheduleList
import uuid

SECRET_KEY = settings.RABBIT_SECRET_KEY

@db_task()
def make_schedule(media, new_id):
    if media == 'twitter':
        response = view_funcs.call_pika_exchange(
            'elastic.twitter.summary.worker.direct',
            'twitter.summary.worker',
            '')
    elif media == 'instagram':
        response = view_funcs.call_pika_exchange(
            'elastic.instagram.summary.worker.every.direct',
            'instagram.summary.worker.every',
            '')
    elif media == 'news':
        response = view_funcs.call_pika_exchange(
            'elastic.olnews.summary.worker.direct',
            'olnews.summary.worker',
            '')
    if not response:
        return

    item = ScheduleList.objects.create(
        id=new_id,
        media=media,
        date=datetime.now(),
        state='pending',
        response='OK'
        )

    
    
@db_task()    
def finish_schedule(id):
    try:
        ScheduleList.objects.filter(id=id).update(state='done')
    except:
        pass