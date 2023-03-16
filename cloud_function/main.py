import base64
from google.cloud import pubsub_v1
import json
import os
import time

topic_id = "door-event"
project_id='ece-528-project'

def push_payload(payload, topic, project):        
    publisher = pubsub_v1.PublisherClient() 
    topic_path = publisher.topic_path(project, topic)        
    data = json.dumps(payload).encode("utf-8")           
    future = publisher.publish(topic_path, data)
    print(future.result())
    print("Pushed message to topic.") 

def on_image_upload(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    payload = {"data" : "Payload data", "timestamp": time.time()}
    print(f"Sending payload: {payload}.")
    push_payload(payload, topic_id, project_id)

