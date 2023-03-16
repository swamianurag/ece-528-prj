import os
from google.cloud import pubsub_v1

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id='ece-528-project',
    sub='door-event-sub2',
)

def callback(message):
    print(message.data)
    print("came here")
    message.ack()

with pubsub_v1.SubscriberClient() as subscriber:
    future = subscriber.subscribe(subscription_name, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()