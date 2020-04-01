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
# lambda stack ✔️
# rds aurora stack ✔️
#
# security group to keep them together

# adapters
# --------
# api gateway aggregate  ->  connects to the private subnet (where the lambda is)
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

        env_dict = {
            "DB_URL" : (f"postgresql://"
                        f"s3jsonapi" # user
                        f":"
                        f"{db_aggregate.aurora.cdk_resource.secret.secret_value.to_string()}" # password
                        f"@"
                        f"{db_aggregate.aurora.cdk_resource.cluster_endpoint.hostname}"       # hostname
                        f":"
                        f"{db_aggregate.aurora.cdk_resource.cluster_endpoint.port}"           # port
                        f"/"
                        f"s3jsonapi" # db
                        ),

            "S3_BUCKET_URL" : s3_aggregate.s3.cdk_resource.bucket_website_url,
            "S3_BUCKET_NAME" : s3_aggregate.s3.cdk_resource.bucket_name,
        }

        api_gw_lambda_aggregate = ApiGwLambdaAggregate(
            self, id,
            s3_aggregate,
            vpc_aggregate,
            db_aggregate,
            security_group,
            env_dict=env_dict,
        )

        for key,value in env_dict.items():
            CfnOutput(
                self,
                key,
                value=value,
            )

