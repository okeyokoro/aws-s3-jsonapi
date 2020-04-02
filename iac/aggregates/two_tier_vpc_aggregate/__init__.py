import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling

from resources import VPC, SubnetConfigBuilder


# make VPC
#
# make private subnet: RDS Serverless
# make public subnet : Lambda


class TwoTierVPCAggregate:
    def __init__(self, stack, id) -> None:
        sb = SubnetConfigBuilder()
        sb.make_public(id)
        sb.make_private(id)
        self.vpc = VPC(stack, id, sb)
