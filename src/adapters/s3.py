import boto3


class S3Service:
    """
       https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
    """
    s3 = boto3.resource("s3")

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(self.bucket_name)

    def list_contents(self) -> list:
        return [ object_summary.Object() for object_summary in self.bucket.objects.all() ]
