from google.cloud import storage
import time

#upload files
# Example call uploadImageToBucket(bucketName,os.path.join(filePath,'MyTestDocument.txt'),'NameInCloud')
def uploadImageToBucket(bucketName,filePath,blonNameInCloud):
    try:
        bucket = client.get_bucket(bucketName)
        b = bucket.blob(blonNameInCloud)
        b.upload_from_filename(filePath)
        print("File Uploaded Sccussfully")
        return True
    except Exception as e:
        print("there is some error resolve it!")
        print(e)
        return False

def createBucket(bucketName):
    try:
        bucket = client.bucket(bucketName)
        bucket.versioning_enabled = False
        bucket.enable_logging(bucketName)
        bucket = client.create_bucket(bucket)
        print("bucket created scussfully")
    except Exception as e:
        print(e)
        return False

def removeFileFromBucket(bucketName,fileName):
    try:
        bucket = client.get_bucket(bucketName)
        bucket.delete_blob(fileName)
        print("File Deleted Scussfylly")
    except Exception as e:
        print(e)
        return False  

#Example call downloadFromBucket(bucketName,os.path.join(os.getcwd(),'fileFromCloud.txt'),'NameInCloud')
def downloadFromBucket(bucketName,filePath,blonNameInCloud):
    try:
        bucket = client.get_bucket(bucketName)
        b = bucket.blob(blonNameInCloud)
        with open(filePath,'wb') as f:
            client.download_blob_to_file(b,f)
        print("Downloaded File from Cloud")
        return True        
    except Exception as e:
        print(e)
        return False  

# Setting credentials using the downloaded JSON file
client = storage.Client().from_service_account_json(json_credentials_path='../ece-528-project-d4286d2dd5b1.json')
def push_image_cloud(image):
    # get the bucket object
    bucket = client.get_bucket('ece-528-image')
    # Name of the object to be stored in the bucket
    rpl = "_"+str(time.time())+".jpg"
    x_image = image.replace(".jpg", rpl)
    object_name_in_gcs_bucket = bucket.blob(x_image)
    # Name of the object in local file system
    object_name_in_gcs_bucket.upload_from_filename(image)
    print("time of image push:",time.time())

def main(argv):
    if 0 == len(argv):
        print("usage: 'python push_image_to_gcp.py <image_file>'")
        return
    push_image_cloud(argv[0])

if __name__ == "__main__":
   main(sys.argv[1:])
