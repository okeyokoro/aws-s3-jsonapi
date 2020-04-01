import boto3


class S3Service:
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#examples
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

    - https://stackoverflow.com/questions/36438085/what-is-the-difference-between-an-s3-object-and-an-objectsummary
    """
    s3 = boto3.resource("s3")

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(self.bucket_name)

    def list_contents(self) -> list:
        """ returns a list of `s3.ObjectSummary` objects
        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#objectsummary
        """
        return [ object_summary.Object() for object_summary in self.bucket.objects.all() ]
