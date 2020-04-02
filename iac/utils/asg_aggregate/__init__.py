from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling

ec2_type = "t2.micro"

linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )
)


class CdkEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Bastion
        # bastion = ec2.BastionHostLinux(
        #     self, "myBastion",
        #     vpc=vpc,
        #     subnet_selection=ec2.SubnetSelection(
        #         subnet_type=ec2.SubnetType.PUBLIC
        #     ),
        #     instance_name="myBastionHostLinux",
        #     instance_type=ec2.InstanceType(instance_type_identifier="t2.micro")
        # )

        # Setup key_name for EC2 instance login if you don't use Session Manager
        # bastion.instance.instance.add_property_override("KeyName", key_name)

        # bastion.connections.allow_from_any_ipv4(
        #     ec2.Port.tcp(22), "Internet access SSH")

        # Create ALB
        # alb = elb.ApplicationLoadBalancer(self, "myALB",
        #                                   vpc=vpc,
        #                                   internet_facing=True,
        #                                   load_balancer_name="myALB"
        #                                   )
        # alb.connections.allow_from_any_ipv4(
        #     ec2.Port.tcp(80), "Internet access ALB 80")
        # listener = alb.add_listener("my80",
        #                             port=80,
        #                             open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "myASG",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                desired_capacity=2,
                                                min_capacity=2,
                                                max_capacity=2,
                                                )

        self.asg.connections.allow_from(
            alb,
            ec2.Port.tcp(80),
            "ALB access 80 port of EC2 in Autoscaling Group"
        )

        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

