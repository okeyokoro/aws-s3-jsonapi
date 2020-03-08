from collections import namedtuple

from aws_cdk import aws_apigateway

from .abstract_resource import AbstractResource



class ApiGateway(AbstractResource):
    """ - https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway.README.html
        - https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway.html
    """
    def __init__(self, stack_obj, stack_id,
                 cdk_resource=aws_apigateway.RestApi,
                 version="v1",
                ):
        super().__init__(stack_obj, stack_id, cdk_resource)

        self.cdk_resource = cdk_resource(stack_obj,
                                         f"{stack_id}-api-gateway",
                                         rest_api_name=f"{stack_id}-api-gateway",
                                         deploy_options=aws_apigateway.StageOptions(stage_name=version))

    def create_api_endpoint(self, name:str, cors=True):
        new_endpoint_cdk_resource = self.cdk_resource.root.add_resource(name)
        return ApiGatewayEndpoint(new_endpoint_cdk_resource, cors=True)


class ApiGatewayLambdaIntegration:
    """ - https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_apigateway/LambdaIntegration.html
        - ^ request_parameters
        - https://docs.aws.amazon.com/apigateway/latest/developerguide/request-response-data-mappings.html

        The source must be an existing method request parameter or a static value.
        You must enclose static values in single quotation marks and pre-encode
        these values based on their destination in the request.
    """
    def __init__(self, lambda_cdk_resource, request_params=None):

        if not request_params:
            request_params = {}

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
            request_parameters=request_params,
            request_templates={
                "application/json" : """
                    {
                        "body" : $input.json('$'),
                        "headers": {
                            #foreach($header in $input.params().header.keySet())
                            "$header": "$util.escapeJavaScript($input.params().header.get($header))" #if($foreach.hasNext),#end

                            #end
                        },
                        "method": "$context.httpMethod",
                        "params": {
                            #foreach($param in $input.params().path.keySet())
                            "$param": "$util.escapeJavaScript($input.params().path.get($param))" #if($foreach.hasNext),#end

                            #end
                        },
                        "query": {
                            #foreach($queryParam in $input.params().querystring.keySet())
                            "$queryParam": "$util.escapeJavaScript($input.params().querystring.get($queryParam))" #if($foreach.hasNext),#end

                            #end
                        }
                    }
                """
            }
        )


class ApiGatewayEndpoint:
    def __init__(self, cdk_resource, cors=True):
        self.cdk_resource = cdk_resource
        self.has_cors = cors
        if self.has_cors:
            self.enable_cors()

    def handle_verb(self,
        verb:str,
        lambda_integration: ApiGatewayLambdaIntegration,
        request_params=None
        ):

        if not request_params:
            request_params = {}

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
            ],
            request_parameters=request_params
        )

    def extend_endpoint(self, path):
        nested_endpoint = self.cdk_resource.add_resource(path)
        return ApiGatewayEndpoint(nested_endpoint)

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


class ApiGatewayRequestParameterBuilder:
    """ will need  to be passed to:
        - LambdaIntegration,
        - ApiGatewayEndpoint.handle_verb
    """
    Mapping = namedtuple("Mapping", ["integration_string",
                                     "method_string",
                                     "is_required",
                                     "static_value",
                                    ])

    def __init__(self,):
        """ [ ("integration.{}", "method.{}", static_value), ... ]
                ^ the first item in the tuple,
                is actually defining a variable that will be made
                available to the Lambda function
                (through the LambdaIntegration)

                the second item,
                passes a value to the variable we defined earlier,
                in the example above the value is a 'method request parameter'
                but concrete values can be passed in as well: (strings, integers, etc)

                'method request parameters' must be defined when 'adding a method/verb'
                to an API endpoint.
                a definition just involves setting the
                'method request parameter' to True (this would make it a required parameter)
                or
                'method request parameter' to False (this would make it an optional parameter)
        """
        self.mappings = []

    def mapping_template(self, prefix,
        variable_name, is_required=False, static_value=None,
        ):
        return self.Mapping(
            f"integration.request.{prefix}.{variable_name}",
            f"method.request.{prefix}.{variable_name}",
            is_required,
            static_value)

    def _add_thing(self, prefix,
        variable_name, is_required=False, static_value=None,
        ):
        self.mappings.append(
            self.mapping_template(prefix, variable_name, is_required, static_value)
        )
        return self

    def add_path(self, variable_name, is_required=False, static_value=None):
        prefix = "path"
        return self._add_thing(prefix, variable_name, is_required, static_value)

    def add_querystring(self, variable_name, is_required=False, static_value=None):
        prefix = "querystring"
        return self._add_thing(prefix, variable_name, is_required, static_value)

    def add_multivaluequerystring(self, variable_name, is_required=False, static_value=None):
        prefix = "multivaluequerystring"
        return self._add_thing(prefix, variable_name, is_required, static_value)

    def add_header(self, variable_name, is_required=False, static_value=None):
        prefix = "header"
        return self._add_thing(prefix, variable_name, is_required, static_value)

    def add_multivalueheader(self, variable_name, is_required=False, static_value=None):
        prefix = "multivalueheader"
        return self._add_thing(prefix, variable_name, is_required, static_value)

    @property
    def dict_for_handle_verb(self):
        """ just get the method_strings """
        return {
            mapping.method_string : mapping.is_required
            for mapping in self.mappings
        }

    @property
    def dict_for_integration(self):
        """ map the integration_string to the staticvalue if available else method_string """
        return {
            mapping.integration_string : mapping.static_value or mapping.method_string
            for mapping in self.mappings
        }
