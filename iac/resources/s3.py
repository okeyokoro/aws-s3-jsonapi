from aws_cdk import aws_s3

from .abstract_resource import AbstractResource



class S3(AbstractResource):

    def __init__(self, stack_obj, stack_id,
                 cdk_resource=aws_s3.Bucket,
                 name="default"
                ):
        super().__init__(stack_obj, stack_id, cdk_resource)

        self.cdk_resource = cdk_resource(stack_obj,
                                         f"{stack_id}-{name}-s3-bucket",)
