from aws_cdk import aws_lambda

from .abstract_resource import AbstractResource



class Lambda(AbstractResource):

    def __init__(self, stack_obj, stack_id,
                 file_name,
                 directory,
                 function_name="main",
                 runtime=aws_lambda.Runtime.PYTHON_3_7,
                 cdk_resource=aws_lambda.Function,
                ):
        super().__init__(stack_obj, stack_id, cdk_resource)

        self.cdk_resource = cdk_resource(stack_obj,
                                         f"{stack_id}-{file_name}-lambda-function",
                                         #
                                         code=aws_lambda.Code.asset(directory),
                                         #
                                         handler=f"{file_name}.{function_name}",
                                         #
                                         runtime=runtime,)