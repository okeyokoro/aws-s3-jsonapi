from aws_cdk.core import Stack, CfnOutput

import aws_cdk.aws_ec2 as ec2

from aggregates import (
    S3Aggregate,
    TwoTierVPCAggregate,
    ApiGwLambdaAggregate,
    RdsServerlessAggregate,
)


# VPC stack ✔️

# private subnet
# --------------
# rds aurora stack ✔️
# lambda stack ✔️
#
# security group to keep them together

# adapters
# --------
# api gateway aggregate  ->  connects to public subnet (where the lambda is)
# s3 aggregate           ->  connects to (public-subnet? vpc-endpoint?) (where the lambda is)




class S3JsonAPIStack(Stack):
    def __init__(self, app, id:str, **kwargs):
        super().__init__(app, f"{id}", **kwargs)

        vpc_aggregate = TwoTierVPCAggregate(self, id)

        security_group = ec2.SecurityGroup(
            self, f"{id}-security-group",
            vpc=vpc_aggregate.vpc.cdk_resource,
            security_group_name=f"{id}-security-group",
        )

        db_aggregate = RdsServerlessAggregate(
            self, id,
            vpc_aggregate.vpc.cdk_resource,
            security_group,
        )

        s3_aggregate = S3Aggregate(
            self, id,
            vpc_aggregate.vpc.cdk_resource
        )

        # postgres db url
        # DB_URL = (f"mongodb://"
        #           f"{db_aggregate.aurora.cdk_resource.master_user}:"
        #           f"{db_aggregate.aurora.cdk_resource.master_user_password}@"
        #           f"{db_aggregate.aurora.cdk_resource.attr_endpoint}:"
        #           f"{db_aggregate.aurora.cdk_resource.attr_port}")
        # S3_URL = ""
        # API_URL = ""
        # ^ pass these to the lambda through env variables

        api_gw_lambda_aggregate = ApiGwLambdaAggregate(
            self, id,
            s3_aggregate,
            vpc_aggregate,
            db_aggregate,
            security_group,
        )

        # core.CfnOutput(
        #     self, "DatabaseOut",
        #     description="Database URL",
        #     value=DB_URL
        # )