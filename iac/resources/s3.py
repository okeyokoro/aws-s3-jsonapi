from aws_cdk import aws_s3, aws_ec2, core

from abcs import AbstractResource


class S3(AbstractResource):
    cdk_construct = aws_s3.Bucket

    def __init__(self, stack_obj, stack_id,
                 name="default",
                ):
        super().__init__(stack_obj, stack_id)

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-{name}-s3-bucket",
            removal_policy=core.RemovalPolicy.DESTROY
        )

