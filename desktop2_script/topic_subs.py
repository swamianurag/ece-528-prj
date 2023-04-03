import os
from google.cloud import pubsub_v1
import json
import time
generation = ''
subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id='ece-528-project',
    sub='door-event-sub2',
)

def callback(message):
    global generation
    jmsg = json.loads(message.data)
    try:
        if generation == jmsg['generation']:
            return
    except KeyError:
        print('Unsupport key message payload')
        return
    print("Got a message. time:", time.time())
    generation = jmsg['generation']
    print(message.data)
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    future = subscriber.subscribe(subscription_name, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()