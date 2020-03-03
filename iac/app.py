from aws_cdk import core

from stack import Stack


if __name__ == "__main__":
    app = core.App()
    Stack(app, "s3-json-api")
    app.synth()
