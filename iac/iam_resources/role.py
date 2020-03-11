from aws_cdk import aws_iam

from .abstract_resource import AbstractResource



class IAMRole(AbstractResource):
    def __init__(self, stack_obj, stack_id,
                 name, resource_url,
                 cdk_resource=aws_iam.Role,
                ):
        super().__init__(stack_obj, stack_id, cdk_resource)
        self.cdk_resource = (
            cdk_resource(
                stack_obj,
                name,
                assumed_by=aws_iam.ServicePrincipal(resource_url)
            )
        )

    def add_policy_statement(self, policy_statement):
        self.cdk_resource.add_to_policy(
            aws_iam.PolicyStatement(
                resources=["*"],
                actions=["lambda:InvokeFunction"]
            )
        )

