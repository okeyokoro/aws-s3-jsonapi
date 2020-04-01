from aws_cdk import aws_s3, aws_ec2

from abcs import AbstractResource



class S3(AbstractResource):
    cdk_construct = aws_s3.Bucket

    def __init__(self, stack_obj, stack_id,
                 name="default",
                ):
        super().__init__(stack_obj, stack_id)

        # self.sg = aws_ec2.SecurityGroup(
        #     stack_obj,
        #     id=f"{stack_id}-s3-security-group",
        #     vpc=vpc,
        #     security_group_name="s3-security-group"
        # )

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-{name}-s3-bucket",
        )

        # self.sg.add_ingress_rule(
        #     peer=aws_ec2.Peer.ipv4("10.0.0.0/16"),
        #     connection=aws_ec2.Port.tcp(2049)
        # )
