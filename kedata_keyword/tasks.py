from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_periodic_task, db_task

from . import view_funcs
from users.models import KedataUsers, LastUpdateTime, UsageKeywordComparison, UsageKeywordListening, UsageKeywordMultikey
from .models import LogKeywordCount

from datetime import datetime
from django.conf import settings

from django.core.mail import EmailMultiAlternatives, send_mail
import json

SECRET_KEY = settings.RABBIT_SECRET_KEY

# Update Log Keyword periodically
@db_periodic_task(crontab(minute='*/5'))
def keyword_log_count_update():    
    recently = view_funcs.call_pika_keyword_log()
    if recently[0]:
        update_list_media = json.dumps(recently[0])
        update_list_id = json.dumps(recently[1])    
        LogKeywordCount.objects.update_or_create(
            id=1,
            defaults={
                'json_data_media': update_list_media,
                'json_data_name': update_list_id,
                'update_time': datetime.now()
                }
            )
       
# UsageKeyword Periodic Updates
@db_periodic_task(crontab(minute='*/2'))
def usage_keyword_update_periodic():
    lis_items, com_items, mul_items = view_funcs.get_keyword_report_data_usage(iterate=False)
    if not lis_items:
        return
    view_funcs.keyword_update_to_db(UsageKeywordListening, lis_items, ['text', 'media', 'key_type', 'timestamps', 'count', 'state', 'user_id'], 'keyword_id')
    view_funcs.keyword_update_to_db(UsageKeywordComparison, com_items, ['name', 'media', 'key_type', 'timestamps', 'count', 'state', 'user_id'], 'keyword_id')
    view_funcs.keyword_update_to_db(UsageKeywordMultikey, mul_items, ['name', 'media', 'timestamps', 'count', 'state', 'user_id'], 'keyword_id')
    LastUpdateTime.objects.update_or_create(id=1, defaults={'last_updated_keyword': datetime.now()})

# Force updates on UsageKeyword
@db_task()
def usage_keyword_update():
    lis_items, com_items, mul_items = view_funcs.get_keyword_report_data_usage()
    if not lis_items:
        return
    view_funcs.keyword_update_to_db(UsageKeywordListening, lis_items, ['text', 'media', 'key_type', 'timestamps', 'count', 'state', 'user_id'], 'keyword_id')
    view_funcs.keyword_update_to_db(UsageKeywordComparison, com_items, ['name', 'media', 'key_type', 'timestamps', 'count', 'state', 'user_id'], 'keyword_id')
    view_funcs.keyword_update_to_db(UsageKeywordMultikey, mul_items, ['name', 'media', 'timestamps', 'count', 'state', 'user_id'], 'keyword_id')
    LastUpdateTime.objects.update_or_create(id=1, defaults={'last_updated_keyword': datetime.now()})

@task()
def send_email(mess):
    subject = '[Kedata Dashboard] Issue Keyword'
    text_content = "Issuing keyword:\n\n" + mess +'\n\n  Do not reply!'
    sender = "kedata.dashboard@kedata"
    receipient = "henzonlol@gmail.com"
    msg = EmailMultiAlternatives(subject, text_content, sender, [receipient])
    response = msg.send()
    