import os
from adapters import S3Service, db_init
from adapters.db.models import S3Buckets


def get_files_and_directories_in_s3_bucket(bucket_name="",):
    default = os.getenv("S3_BUCKET_NAME")

    if not bucket_name or bucket_name == "default":
        bucket_name = default

    session = db_init()
    entry = S3Buckets(name=bucket_name,
                      was_default=bucket_name==default)
    session.add(entry)
    session.commit()

    # TODO: handle permission exceptions
    return S3Service(bucket_name).list_contents()


def get_records_from_rds():
    session = db_init()
    buckets = session.query(S3Buckets).all()
    return buckets
