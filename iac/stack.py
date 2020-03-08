from aws_cdk import core

from resources import (
    S3,
    Lambda,
    ApiGatewayLambdaIntegration,
    ApiGateway,
)


class Stack(core.Stack):
    """ All the cloud resources are assembled/initialized in this 1 Stack """

    def __init__(self, app, id:str, **kwargs):
        super().__init__(app, id, **kwargs)

        self.s3 = S3(self, id,)

        self.api_gateway = ApiGateway(self, id,)

        endpoint = self.create_api_endpoint("s3-buckets",) # TODO: /v1/s3-buckets

        # GET /s3-buckets/<name>/
        # -----------------------
        lambda_fn = self.create_lambda("s3_bucket_get",)
        endpoint.handle_verb("GET", lambda_fn)


    def create_lambda(self, file_name, directory="../src",):

        lambda_fn = Lambda(self, id,
                           file_name=file_name,
                           directory=directory,)
        lambda_fn = lambda_fn.cdk_resource

        self.s3.cdk_resource.grant_read_write(lambda_fn)

        lambda_fn = ApiGatewayLambdaIntegration(lambda_fn)
        lambda_fn = lambda_fn.cdk_resource
        return lambda_fn


    def create_api_endpoint(self, name):
        endpoint = (
            self.api_gateway.create_api_endpoint(
                name,
                cors=True))
        return endpoint

