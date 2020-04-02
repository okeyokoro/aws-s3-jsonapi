from usecases import get_files_and_directories_in_s3_bucket
from schemas.s3_bucket import s3_contents_schema

from . import session


def main(event, context):
    bucket_name = event["params"]["bucket_name"]
    contents_of_bucket = get_files_and_directories_in_s3_bucket(bucket_name, session)
    return s3_contents_schema.dump(contents_of_bucket)
