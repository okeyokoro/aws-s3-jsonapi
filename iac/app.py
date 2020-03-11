from aws_cdk import core

from stacks import (
    TwoTierVPCStack,
    ApiGwLambdaStack,
    RdsServerlessStack,
    S3Stack,
)


# vpc stack ✔️

# private subnet
# --------------
# s3 stack ✔️
# rds aurora stack ✔️

# public subnet
# -------------
# api gateway lambda stack ✔️



if __name__ == "__main__":

    app = core.App()
    id = "s3-json-api"

    vpc_stack = TwoTierVPCStack(app, id)
    db_stack = RdsServerlessStack(app, id, vpc_stack.vpc.cdk_resource)

    s3_stack = S3Stack(app, id, vpc_stack.vpc.cdk_resource)

    api_gw_lambda_stack = ApiGwLambdaStack(
        app, id, s3_stack, vpc_stack, db_stack
    )

    app.synth()
