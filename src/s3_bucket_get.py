import json
from usecases import get_files_and_directories_in_s3_bucket
from schemas.s3_bucket import s3_contents_schema


def main(event, context):
    contents_of_bucket = get_files_and_directories_in_s3_bucket("default")
    return s3_contents_schema.dump(contents_of_bucket)
