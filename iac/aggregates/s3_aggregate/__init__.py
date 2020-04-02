from aws_cdk import aws_ec2

from resources import S3


class S3Aggregate:
    def __init__(self, stack, id, vpc: aws_ec2.Vpc) -> None:

        vpc.add_gateway_endpoint(
            "s3-bucket-vpc-gateway",
            service=aws_ec2.GatewayVpcEndpointAwsService.S3,
        )
        self.s3 = S3(stack, id, vpc)
