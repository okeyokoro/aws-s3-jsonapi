from aws_cdk import aws_lambda, core

from abcs import AbstractResource



class Lambda(AbstractResource):
    cdk_construct = aws_lambda.Function

    def __init__(self, stack_obj, stack_id,
                 file_name,
                 directory,
                 vpc,
                 security_group,
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
            vpc=vpc,
            security_group=security_group,
        )

"""
class Function(scope: aws_cdk.core.Construct, id: str, code: "Code", handler: str, runtime: "Runtime", allow_all_outbound: typing.Optional[bool]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, events: typing.Optional[typing.List["IEventSource"]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List["ILayerVersion"]]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, tracing: typing.Optional["Tracing"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, max_event_age: typing.Optional[aws_cdk.core.Duration]=None, on_failure: typing.Optional["IDestination"]=None, on_success: typing.Optional["IDestination"]=None, retry_attempts: typing.Optional[jsii.Number]=None)
Deploys a file from from inside the construct library as a function.

The supplied file is subject to the 4096 bytes limit of being embedded in a CloudFormation template.

The construct includes an associated role with the lambda.

This construct does not yet reproduce all features from the underlying resource library.


"""