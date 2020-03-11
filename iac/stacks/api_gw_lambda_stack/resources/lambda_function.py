from aws_cdk import aws_lambda, core

from abcs import AbstractResource



class Lambda(AbstractResource):
    cdk_construct = aws_lambda.Function

    def __init__(self, stack_obj, stack_id,
                 file_name,
                 directory,
                 vpc,
                 function_name="main",
                 runtime=aws_lambda.Runtime.PYTHON_3_7,
                ):
        super().__init__(stack_obj, stack_id)

        self.cdk_resource = self.cdk_construct(
            stack_obj,
            f"{stack_id}-{file_name}-lambda-function",
            code=aws_lambda.Code.asset(directory),
            handler=f"{file_name}.{function_name}",
            runtime=runtime,
            timeout=core.Duration.seconds(20),
            vpc=vpc
        )
