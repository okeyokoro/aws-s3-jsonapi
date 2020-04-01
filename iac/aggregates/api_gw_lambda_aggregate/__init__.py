from resources import (
    ApiGatewayLambdaIntegration,
    ApiGateway,
    ApiGatewayRequestParameterBuilder,
    Lambda,
)


class LambdaCreationMixin:

    def create_lambda(self, file_name, directory="../src", request_params=None):

        lambda_fn = Lambda(self.stack, id,
                           file_name=file_name,
                           directory=directory,
                           vpc=self.vpc,
                           security_group=self.security_group,
                           env_dict=self.env_dict)

        lambda_fn = lambda_fn.cdk_resource

        self.s3.s3.cdk_resource.grant_read_write(lambda_fn)

        lambda_fn = ApiGatewayLambdaIntegration(lambda_fn, request_params)
        lambda_fn = lambda_fn.cdk_resource
        return lambda_fn


    def create_api_endpoint(self, name):
        endpoint = (
            self.api_gateway
            .create_api_endpoint(name, cors=True)
        )
        return endpoint


class ApiGwLambdaAggregate(LambdaCreationMixin):

    def __init__(self, stack, id,
        s3,
        vpc_aggregate,
        db,
        security_group,
        env_dict=None,
    ):
        if not env_dict:
            env_dict = {}

        self.env_dict = env_dict

        self.stack = stack
        self.vpc = vpc_aggregate.vpc.cdk_resource
        self.security_group = security_group

        self.s3 = s3
        self.db = db

        self.api_gateway = ApiGateway(stack, id,)

        buckets = self.create_api_endpoint("s3-buckets",)
        bucket = buckets.extend_endpoint("{bucket_name}")

        # -----------------------
        # GET /s3-buckets/<name>/
        # -----------------------
        request_params = (
            ApiGatewayRequestParameterBuilder()
            .add_path("bucket_name",
                      is_required=True)
        )
        lambda_fn = self.create_lambda(
            "s3_bucket_get",
            request_params=request_params.dict_for_integration
        )
        bucket.handle_verb(
            "GET", lambda_fn,
            request_params.dict_for_handle_verb
        )

        # -----------------------
        # GET /s3-buckets/
        # -----------------------
        rds_get_lambda_fn = self.create_lambda("rds_db_get",)
        buckets.handle_verb("GET", rds_get_lambda_fn)

