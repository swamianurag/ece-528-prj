from google.cloud import storage
import time

# Setting credentials using the downloaded JSON file

client = storage.Client().from_service_account_json(json_credentials_path='../ece-528-project-d4286d2dd5b1.json')
# Creating bucket object
bucket = client.get_bucket('ece-528-image')
# Name of the object to be stored in the bucket
object_name_in_gcs_bucket = bucket.blob('wakeupcat_'+str(time.time())+".jpg")
# Name of the object in local file system
object_name_in_gcs_bucket.upload_from_filename('weapon.jpg')