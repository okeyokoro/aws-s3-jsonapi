from aws_cdk.core import Stack

from .resources import AuroraServerless


class RdsServerlessStack(Stack):
    def __init__(self, app, id, vpc) -> None:
        super().__init__(app, f"{id}--rds-serverless-stack")

        self.aurora = AuroraServerless(self, id, vpc, "private")
