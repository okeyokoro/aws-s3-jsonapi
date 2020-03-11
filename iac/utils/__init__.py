from aws_cdk import (
    aws_ec2,
    core,
)


def print_resource_id(stack_obj, title:str, cdk_resource_id):
    core.CfnOutput(
        stack_obj,
        title,
        value=cdk_resource_id
    )


def get_subnet_type(name:str):
    SUBNET_TYPES = {
        "public" : aws_ec2.SubnetType.PUBLIC,
        "private" : aws_ec2.SubnetType.PRIVATE,
        "isolated" : aws_ec2.SubnetType.ISOLATED,
    }
    return SUBNET_TYPES[name]

