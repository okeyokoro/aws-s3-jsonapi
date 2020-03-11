from aws_cdk.core import Stack

from aws_cdk.aws_apigateway import VpcLink

from .resources import (
    Lambda,
    ApiGatewayLambdaIntegration,
    ApiGateway,
    ApiGatewayRequestParameterBuilder,
)

""" TODO: Pass in S3 as parameter instead ! """

class ApiGwLambdaStack(Stack):

    def __init__(self, app, id, s3, vpc_stack, db):
        super().__init__(app, f"{id}--api-gw-lambda-stack")
        self.vpc = vpc_stack.vpc.cdk_resource

        self.s3 = s3
        self.db = db


        # GET /s3-buckets/<name>/
        # -----------------------
        request_params = (
            ApiGatewayRequestParameterBuilder()
            .add_path("bucket_name", is_required=True)
            # TODO: add AWS_SECRET_KEY header
            # TODO: add AWS_ACCESS_KEY header
        )
        lambda_fn = self.create_lambda(
            "s3_bucket_get",
            request_params=request_params.dict_for_integration
        )

        self.api_gateway = ApiGateway(self, id, lambda_fn)

        self.vpc_link = VpcLink(self, f"{id}--vpc-link", targets=[vpc_stack.alb])

        buckets = self.create_api_endpoint("s3-buckets",)
        # TODO:
        # buckets.handle_verb("GET", lambda_that_looks_at_RDS)
        bucket = buckets.extend_endpoint("{bucket_name}")

        bucket.handle_verb(
            "GET", lambda_fn,
            request_params.dict_for_handle_verb
        )


    def create_lambda(self, file_name, directory="../src", request_params=None):

        lambda_fn = Lambda(self, id,
                           file_name=file_name,
                           directory=directory,
                           vpc=self.vpc)
        lambda_fn = lambda_fn.cdk_resource

        self.s3.s3.cdk_resource.grant_read_write(lambda_fn)
        # self.db.aurora.cdk_resource

        lambda_fn = ApiGatewayLambdaIntegration(lambda_fn, request_params)
        lambda_fn = lambda_fn.cdk_resource
        return lambda_fn


    def create_api_endpoint(self, name):
        endpoint = (
            self.api_gateway.create_api_endpoint(
                name,
                cors=True))
        return endpoint

