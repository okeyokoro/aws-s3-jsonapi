from aws_cdk import aws_ec2

from aws_cdk.core import Stack

from .resources import S3


class S3Stack(Stack):
    def __init__(self, app, id, vpc: aws_ec2.Vpc) -> None:
        super().__init__(app, f"{id}-s3-stack")
        vpc.add_gateway_endpoint(
            "s3-bucket-vpc-gateway",
            service=aws_ec2.GatewayVpcEndpointAwsService.S3,
        )
        self.s3 = S3(self, id, vpc)
