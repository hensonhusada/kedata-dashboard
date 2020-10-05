from django.conf import settings
from django.http import Http404
from django.db.models import Count

from users.models import KedataUsers, UsageKeywordListening, UsageKeywordComparison, UsageKeywordMultikey
from users.pika_rpc import RpcClient

from datetime import datetime
import string, random

SECRET_KEY = settings.RABBIT_SECRET_KEY
RESPONSE_EXCHANGE_NAME = 'endgraf.responses.direct'

# Generate random alphanumerical password
def random_password_generator(length=8):
    printable = f'{string.ascii_letters}{string.digits}'
    printable = list(printable)
    random.shuffle(printable)
    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    return random_password

# Bulk update objects to database (limit to 100 queries)
def bulk_update_to_db(test, items, update_list, match_field, i=0):
    while True:
        if i+100 > len(items):
            test.objects.bulk_update_or_create(
            items[i:],
            update_list,
            match_field=match_field
            )            
            break

        test.objects.bulk_update_or_create(
            items[i:i+100],
            update_list,
            match_field=match_field
            )
        i += 100
        # print(i)

# Generic pika RPC
def call_pika_exchange(exc, qu, body):
    try:
        client = RpcClient(RESPONSE_EXCHANGE_NAME)
        response = client.call(exc, qu, body)
        client.close()
        return response
    except:
        return None

# Specific for KedataUsers RPC (return a list of KedataUsers objects)
def call_pika_exchange_users():
    res_off = 0
    input_list_status = {
        'secret_key':SECRET_KEY
    }
    items = []
    try:
        client_test = RpcClient(RESPONSE_EXCHANGE_NAME)
    except Exception as e:
        print("Error, ", e)
        return None
    while True:
        input_list_status['result_offset'] = str(res_off)
        response = client_test.call(
            'endgraf.dashboard.list_status.retrieve',
            'kedata.dashboard.list_status.retrieve',
            input_list_status
            )
        if not 'content' in response:
            return None
        for data in response['content']['data']:
            items.append(
                KedataUsers(
                    user_id= data['id'],
                    email= data['email'],
                    name= data['name'],
                    subscription= data['subscription'],
                    project_name= data['project_name'],
                    last_login= datetime.fromtimestamp(data['last_login']),
                    created_at= datetime.fromtimestamp(data['created_at'])
                    )
                )

        if not response['content']['data']:
            break
        res_off += 25
    client_test.close()
    return items

# Get users count base on field variable
def get_user_report_data(field):
    labels = []
    datas = []
    count = KedataUsers.objects.values(field).annotate(the_count=Count(field))
    for c in count:
        labels.append(c[field])
        datas.append(c['the_count'])
    return(labels, datas)
