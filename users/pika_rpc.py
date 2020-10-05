import pika, time, uuid, json

from django.conf import settings

class ResponseTimeout(Exception):pass

class RpcClient(object):
    def __init__(self, response_exchange_name, vhost='vhost'):
        self.connection = pika.BlockingConnection(
            settings.RPC_PARAMETERS
            )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.queue_bind(self.callback_queue, response_exchange_name)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response            
            )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response=body           

    def call(self, exchange, routing_key, body, timeout=5):    
        # LOGGER.info('Publishing')    
        self.response=None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,            
            body=json.dumps(body),
            properties=pika.BasicProperties(content_type='application/json' ,correlation_id=self.corr_id, reply_to=self.callback_queue)
            )
        start = time.time()
        while self.response is None:
            if(start+timeout)<time.time():
                raise ResponseTimeout()
            self.connection.process_data_events()        
        return(json.loads(self.response))

    def close(self):
        self.connection.close()