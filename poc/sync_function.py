from google.cloud import storage
import os


client = storage.Client.from_service_account_json('piyush-chaudhari-fall2023-8f85ee7dc13d.json')
gcs_bucket_name = 'eccfsbucket'
bucket = client.get_bucket(gcs_bucket_name)


blobs = list(bucket.list_blobs())
root = "mount1"

print("blobs:", blobs)

for blob in blobs:
    local_path = os.path.join(root, blob.name)
    if local_path.endswith('/'):
        os.makedirs(local_path, exist_ok=True)
    else:
        # Download the object if it's a file
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        blob.download_to_filename(local_path)
