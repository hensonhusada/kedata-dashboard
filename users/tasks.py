from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import periodic_task, task, db_periodic_task, lock_task, db_task
from users.models import KedataUsers, LastUpdateTime, UsageKeywordComparison, UsageKeywordListening, UsageKeywordMultikey
from datetime import datetime

# Pika functions
from . import view_funcs

SECRET_KEY = settings.RABBIT_SECRET_KEY

# Update users periodically
@db_periodic_task(crontab(minute='*/5'))
def update_kedata_users_periodically():
    items = view_funcs.call_pika_exchange_users() # Return a list of KedataUsers objects
    update_list = ['email', 'name', 'subscription', 'project_name', 'last_login', 'created_at']
    view_funcs.bulk_update_to_db(KedataUsers, items, update_list, 'user_id')
    LastUpdateTime.objects.update_or_create(id=1, defaults={'last_updated_user': datetime.now()})

# Update users task
@db_task()
def update_kedata_users():
    items = view_funcs.call_pika_exchange_users()
    update_list = ['email', 'name', 'subscription', 'project_name', 'last_login', 'created_at']
    view_funcs.bulk_update_to_db(KedataUsers, items, update_list, 'user_id')
    LastUpdateTime.objects.update_or_create(id=1, defaults={'last_updated_user': datetime.now()})

# New user task
@task()
def new_user_pika(message):
    response = view_funcs.call_pika_exchange(
        'endgraf.dashboard.register_account.retrieve',
        'kedata.dashboard.register_account.register',
        message
        )
    # if response:
    #     messages.add_message(self.request, messages.WARNING, 'Error')        
    # messages.add_message(self.request, messages.SUCCESS, 'Success')

# Upgrade user task
@db_task()
def upgrade_user_pika(message):
    response = view_funcs.call_pika_exchange(
        'endgraf.dashboard.upgrade_status.retrieve',
        'kedata.dashboard.upgrade_status.retrieve',
        message
        )
    print(response)
    # if response['content']['message'] != 'success':
    #     messages.add_message(request, messages.ERROR, 'Error')
    # else:
    #     update_id = response['content']['data']['user_id']
    #     KedataUsers.objects.filter(user_id=update_id).update(subscription=status['add_status'])
    #     messages.add_message(request, messages.SUCCESS, 'Success')
