import os
from adapters import S3Service


def get_files_and_directories_in_s3_bucket(bucket_name="",):

    if not bucket_name or bucket_name == "default":
        bucket_name = os.getenv("S3_BUCKET_NAME")

    # TODO: handle permission exceptions
    return S3Service(bucket_name).list_contents()

