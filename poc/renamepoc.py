from google.cloud import storage
client = storage.Client.from_service_account_json('piyush-chaudhari-fall2023-8f85ee7dc13d.json')
gcs_bucket_name = 'eccfsbucket'
bucket = client.get_bucket(gcs_bucket_name)

old_prefix = "mudit/one/one.txt"
new_prefix = "mudit/one.txt"
objects_to_rename = list(bucket.list_blobs(prefix=old_prefix))
print(objects_to_rename)

if (len(objects_to_rename) > 0):
    print("directory hai")
    # its a directory
    old_itself_indx = -1
    for indx in range(len(objects_to_rename)):
        blob = objects_to_rename[indx]
        new_blob_name = new_prefix + blob.name[len(old_prefix):]
        if blob.name[len(old_prefix):] == '/':
            old_itself_indx = indx
            continue
        # Copy the content from the old object to the new object
        new_blob = bucket.blob(new_blob_name)
        new_blob.upload_from_string(blob.download_as_string())        
        # Delete the old object
        blob.delete()

    if (old_itself_indx != -1):
        objects_to_rename[old_itself_indx].delete()

else:
    # logic only for file
    print("file hai")
    source_blob = self.bucket.blob(old[1:])
    blob_copy = self.bucket.copy_blob(source_blob, self.client.bucket(self.gcs_bucket_name), new[1:])
    self.bucket.delete_blob(old[1:])

print("done")