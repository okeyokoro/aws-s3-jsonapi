from aws_cdk.core import Stack

import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling

from .resources import VPC, SubnetConfigBuilder


# make VPC
#
# make private subnet:  s3, RDS Serverless
# make public subnet :  api gateway, lambda



class TwoTierVPCStack(Stack):
    def __init__(self, app, id) -> None:
        super().__init__(app, f"{id}-two-tier-vpc-stack")

        sb = SubnetConfigBuilder()
        sb.make_public(id)
        sb.make_private(id)
        self.vpc = VPC(self, id, sb)


        ec2_type = "t2.micro"
        linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                        edition=ec2.AmazonLinuxEdition.STANDARD,
                                        virtualization=ec2.AmazonLinuxVirt.HVM,
                                        storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                        )

        # Create ALB
        # self.alb = elb.ApplicationLoadBalancer(
        #     self, "myALB",
        #     vpc=self.vpc.cdk_resource,
        #     internet_facing=True,
        #     load_balancer_name="myALB"
        # )
        self.alb = elb.ApplicationLoadBalancer(
            self,
            "myNLB",
            vpc=self.vpc.cdk_resource,
            internet_facing=True,
            load_balancer_name="myNLB"
        )

        self.alb.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80),
            "Internet access ALB 80"
        )
        listener = self.alb.add_listener("my80",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(
            self, "myASG",
            vpc=self.vpc.cdk_resource,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
            instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
            machine_image=linux_ami,
            desired_capacity=2,
            min_capacity=2,
            max_capacity=2,
        )

        self.asg.connections.allow_from(
            self.alb,
            ec2.Port.tcp(80),
            "ALB access 80 port of EC2 in Autoscaling Group"
        )
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])