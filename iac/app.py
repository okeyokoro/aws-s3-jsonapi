from aws_cdk.core import App

from stack import S3JsonAPIStack


if __name__ == "__main__":

    app, id = App(), "s3-json-api-ii"
    S3JsonAPIStack(app, id)
    app.synth()
