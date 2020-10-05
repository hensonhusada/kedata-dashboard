from django.conf import settings
from users.pika_rpc import RpcClient

SECRET_KEY = settings.RABBIT_SECRET_KEY
RESPONSE_EXCHANGE_NAME = 'elastic.responses.direct'

def call_pika_exchange(exc, que, body):
    try:
        client = RpcClient(RESPONSE_EXCHANGE_NAME, vhost='elastic_vhost')
        response = client.call(exc, que, body)
        client.close()
        return response
    except:
        return None