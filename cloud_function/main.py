import base64
from google.cloud import pubsub_v1
from google.cloud import vision
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

def detect_lable(bucket, image):
    print("came to detect lable:bucket", bucket, " image:",image )
    print("GCP file location:",f"gs://{bucket}/{image}" )
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    # Use the Vision API to extract text from the image
    image = vision.Image(source=vision.ImageSource(gcs_image_uri=f"gs://{bucket}/{image}"))
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    violence = False;
    print('Labels:')
    for label in labels:
        #print(label.description)
        if ('Gun' in label.description):
            violence = True
        elif ('Arms' in label.description):
            violence = True
    # Performs safe search on the image file
    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    violence_likelihood = ['POSSIBLE', 'LIKELY', 'VERY_LIKELY']

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation
    scene = 'No threat detected'
    print('Safe search:')
    print('violence: {}'.format(likelihood_name[safe.violence]))
    res = [i for i in violence_likelihood if likelihood_name[safe.violence] in i]
    if (violence or len(res) > 0):
        scene = 'Possible violence scene'
        print(scene)

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: ''https://cloud.google.com/apis/design/errors'.format(response.error.message))
    payload = {"scene" : scene, "timestamp": time.time()}
    print(f"Sending payload: {payload}.")
    push_payload(payload, topic_id, project_id)

def on_image_upload(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    jmsg = json.loads(pubsub_message)
    detect_lable(jmsg['bucket'], jmsg['name'])
    #payload = {"scene" : scene, "timestamp": time.time()}
    #print(f"Sending payload: {payload}.")
    #push_payload(payload, topic_id, project_id)

