## LAMBDA GOTCHAS

1. You need to have all lambdas at the root of the directory.
   This is just the easiest way to to ensure that all your supporting modules get packaged along with it.
   See https://www.reddit.com/r/aws/comments/93jhgi/how_can_i_add_third_party_python_dependencies_to/e3dudw0?utm_source=share&utm_medium=web2x

2. You need to install dependencies within the directory with the lambdas.
   Do this with `pip install -r requirements.txt -t .`.
   See https://www.reddit.com/r/aws/comments/93jhgi/how_can_i_add_third_party_python_dependencies_to/e3eayz2?utm_source=share&utm_medium=web2x

3. You'll want to give your lambda function a custom `timeout` duration (in the aws cdk/cloudformation).
   Default is 3 seconds.

4. You'll want to grant your lambda any IAM Roles/PolicyStatements it needs to talk to other AWS resources.
   Personally, I keep forgetting to do this, and find it to be a pain in the ass
