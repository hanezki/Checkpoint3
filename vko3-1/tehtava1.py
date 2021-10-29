import requests
from google.cloud import storage

storage_client = storage.Client()

BUCKET_NAME = "checkpoint3-bucketti"
FILE_NAME = "checkpoint.txt"


def get_json():
    request = requests.get("https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json")
    data = request.json()
    write_to_text(data)


def write_to_text(data):
    parameters = []
    for i in sorted(data["items"], key=lambda x: x["number"]):
        parameters.append(i["parameter"])

    new_text = open(FILE_NAME, "w+")
    for i in parameters:
        new_text.write(f"{i}\n")
    new_text.close()

    create_bucket(BUCKET_NAME)
    upload_blob(BUCKET_NAME, FILE_NAME, FILE_NAME)


def create_bucket(bucket_name):
    if check_if_bucket_exists(BUCKET_NAME):
        # if bucket exists already, dont create a new one
        pass
    else:
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "COLDLINE"
        new_bucket = storage_client.create_bucket(bucket, location="us")

        print(
            f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}")


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}")


def check_if_bucket_exists(bucket_name):
    bucket = [bucket_name]
    for i in bucket:
        BUCKET = storage_client.bucket(i)
        try:
            if BUCKET.exists():
                return True
        except:
            return False


if __name__ == "__main__":
    get_json()
