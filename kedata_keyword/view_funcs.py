from django.conf import settings
from users.pika_rpc import RpcClient

from users.models import UsageKeywordListening, KedataUsers, UsageKeywordComparison, UsageKeywordMultikey, LastUpdateTime

from datetime import datetime

SECRET_KEY = settings.RABBIT_SECRET_KEY
RESPONSE_EXCHANGE_NAME = 'endgraf.responses.direct'

# Bulk Update to DB (every 50 queries)
def keyword_update_to_db(test, items,update_list,match_field, i=0):
    while True:
        if i+50 > len(items):
            test.objects.bulk_update_or_create(
            items[i:],
            update_list,
            match_field=match_field
            )            
            break

        test.objects.bulk_update_or_create(
            items[i:i+50],
            update_list,
            match_field=match_field
            )
        i += 50

# Generic pika RPC
def call_pika_exchange(exc, qu, body):
    try:
        client = RpcClient(RESPONSE_EXCHANGE_NAME)
        response = client.call(exc, qu, body)
        client.close()
        return response
    except:
        return None
    
# Specific RPC for LogKeyword (return two list for LogKeywordCount updates)
def call_pika_keyword_log():
    res_off = 0
    update_list_media = {}
    update_list_id = {}
    body = {
        'secret_key': SECRET_KEY,
        'fields': 'log'
    }
    try:
        client_test = RpcClient(RESPONSE_EXCHANGE_NAME)
    except Exception as e:
        print("Error, ", e)
        return None, None
    while True:
        body['resultOffset'] = str(res_off)
        response = client_test.call(
            'endgraf.dashboard.usage_keyword.retrieve', 
            'kedata.dashboard.usage_keyword.retrieve',
            body
            )
        if not 'content' in response:
            return None, None
        if not response['content']['results']['listening']:
            break
        res_off += 25

        for data in response['content']['results']['listening']:
            if not data['media'] in update_list_media.keys():
                update_list_media[str(data['media'])] = 1
            else:
                update_list_media[str(data['media'])] += 1

            if not data['name'] in update_list_id.keys():
                update_list_id[str(data['name'])] = 1
            else:
                update_list_id[str(data['name'])] += 1

        # if res_off >= 20:
        #     break
        
    client_test.close()
    return update_list_media, update_list_id

# Specific RPC for KeywordUsage objects
def get_keyword_report_data_usage(iterate=True):
    res_off = 0
    lis_items = []
    mul_items = []
    com_items = []
    try:
        client_test = RpcClient(RESPONSE_EXCHANGE_NAME)
    except Exception as e:
        print('Error: ', e)
        return None, None, None
    body = {'secret_key': SECRET_KEY, 'fields': 'usage'}
    while True:
        body['resultOffset'] = str(res_off)
        response = client_test.call(
            'endgraf.dashboard.usage_keyword.retrieve', 
            'kedata.dashboard.usage_keyword.retrieve',
            body
            )
        if not 'content' in response:
            return None, None, None
        if not response['content']['results']['listening'] and not response['content']['results']['comparison'] and not response['content']['results']['multi']:
            break
        res_off += 25        
            
        clean_response = response['content']['results']
        
        for data_key in clean_response:
            for data in clean_response[data_key]:
                if data_key == 'listening':
                    try:
                        lis_items.append(
                            UsageKeywordListening(
                                keyword_id=data['id'],
                                text=data['text'],
                                media=data['media'],
                                key_type=data['type'],
                                timestamps=datetime.fromtimestamp(data['timestamps']),
                                count=data['count'],
                                state=data['state'],
                                user_id=KedataUsers.objects.get(user_id=data['foreignKey'])
                                )
                            )
                    except:
                        pass
                elif data_key == 'comparison':
                    try:
                        com_items.append(
                            UsageKeywordComparison(
                                keyword_id=data['id'],
                                name=data['name'],
                                media=data['media'],
                                key_type=data['type'],
                                timestamps=datetime.fromtimestamp(data['timestamps']),
                                count=data['count'],
                                state=data['state'],
                                user_id=KedataUsers.objects.get(user_id=data['foreignKey'])
                                )
                            )
                    except:
                        pass
                elif data_key == 'multi':
                    try:
                        mul_items.append(
                            UsageKeywordMultikey(
                                keyword_id=data['id'],
                                name=data['name'],
                                media=data['media'],                           
                                timestamps=datetime.fromtimestamp(data['timestamps']),
                                count=data['count'],
                                state=data['state'],
                                user_id=KedataUsers.objects.get(user_id=data['foreignKey'])
                                )
                        )
                    except:
                        pass
                else:
                    pass
        if not iterate:
            break            
        
    client_test.close()
    return lis_items, com_items, mul_items
