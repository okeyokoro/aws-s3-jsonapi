from aws_cdk.core import Stack

# from .resources import 


class GitHubCICDStack(Stack):

    def __init__(self, app, id:str, s3, **kwargs):
        super().__init__(app, id, **kwargs)

        pass
