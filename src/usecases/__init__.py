import os
from adapters import S3Service
from adapters.db.models import S3Buckets


def get_files_and_directories_in_s3_bucket(bucket_name="", session):
    default = os.getenv("S3_BUCKET_NAME")

    if not bucket_name or bucket_name == "default":
        bucket_name = default

    entry = S3Buckets(name=bucket_name,
                      was_default=bucket_name==default)
    session.add(entry)
    session.commit()

    # TODO: handle permission exceptions
    return S3Service(bucket_name).list_contents()


def get_records_from_rds(session):
    buckets = session.query(S3Buckets).all()
    return buckets
