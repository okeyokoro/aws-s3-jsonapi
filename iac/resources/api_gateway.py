from aws_cdk import aws_apigateway

from .abstract_resource import AbstractResource



class ApiGateway(AbstractResource):

    def __init__(self, stack_obj, stack_id,
                 cdk_resource=aws_apigateway.RestApi,
                ):
        super().__init__(stack_obj, stack_id, cdk_resource)

        self.cdk_resource = cdk_resource(stack_obj,
                                         f"{stack_id}-api-gateway",
                                         rest_api_name=f"{stack_id}-api-gateway",)

    def create_api_endpoint(self, name:str, cors=True):
        new_endpoint_cdk_resource = self.cdk_resource.root.add_resource(name)
        return ApiGatewayEndpoint(new_endpoint_cdk_resource, cors=True)


class ApiGatewayLambdaIntegration:

    def __init__(self, lambda_cdk_resource):
        self.cdk_resource = aws_apigateway.LambdaIntegration(
            lambda_cdk_resource,
            proxy=False,
            integration_responses=[
                {
                    'statusCode': '200',
                    'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': "'*'",
                    }
                }
            ],
        )


class ApiGatewayEndpoint:
    def __init__(self, cdk_resource, cors=True):
        self.cdk_resource = cdk_resource
        self.has_cors = cors
        if self.has_cors:
            self.enable_cors()

    def handle_verb(self, verb:str, lambda_integration: ApiGatewayLambdaIntegration):

        self.cdk_resource.add_method(
            verb,
            lambda_integration,
            method_responses=[
                {
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': True,
                    }
                }
            ]
        )

    def enable_cors(self):
        # TODO: this shares a lot of code with `handle_verb`
        #       perhaps, make a helper function, that abstracts the shared code
        self.cdk_resource.add_method(
            'OPTIONS',
            aws_apigateway.MockIntegration(
                integration_responses=[
                    {
                        'statusCode': '200',
                        'responseParameters': {
                            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
                            'method.response.header.Access-Control-Allow-Origin': "'*'",
                            'method.response.header.Access-Control-Allow-Methods': "'GET,OPTIONS'"
                        }
                    },
                ],
                passthrough_behavior=aws_apigateway.PassthroughBehavior.WHEN_NO_MATCH,
                request_templates={"application/json":"{\"statusCode\":200}"},
            ),
            method_responses=[
                {
                    'statusCode': '200',
                    'responseParameters': {
                            'method.response.header.Access-Control-Allow-Headers': True,
                            'method.response.header.Access-Control-Allow-Methods': True,
                            'method.response.header.Access-Control-Allow-Origin': True,
                        }
                },
            ],
        )

