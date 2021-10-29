import time
from google.cloud import storage
import sys
import os

storage_client = storage.Client()

BUCKET_NAME = "checkpoint3-bucketti"
FILE_NAME = "checkpoint.txt"


def download_blob(bucket_name, source_blob_name, destination_file_name, line_count):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print_lines(FILE_NAME, line_count)
    # print(f"Downloaded storage object {source_blob_name} from bucket {bucket_name} to local file {destination_file_name}")


def print_lines(filename, line_count):
    max_time_to_wait = 5
    start_time = time.time()

    while os.path.isfile(filename) is False:
        if time.time() - start_time >= max_time_to_wait:
            break
        time.sleep(0.5)
    try:
        with open(filename) as teksti:
            lines = teksti.read().splitlines()
            lines.sort(key=lambda x: (len(x), x))
            for i in range(0, line_count):
                print(lines[i])
    except FileNotFoundError:
        print("Tiedostoa ei löytynyt")


download_blob(BUCKET_NAME, FILE_NAME, FILE_NAME, int(sys.argv[1]))
