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

5. An insane amount of toil and divination went into figuring out how to pass
   **api variables** to the lambda as props of the **event** dict.
   I just got lucky, that I found bits and pieces of the answer in obscure places.
   See the `iac/` portion of the git commit attached to this line for more &
   https://medium.com/simple-thoughts-amplified/passing-variables-from-aws-api-gateway-to-lambda-3c5d8602081b

   ```
    event['params']['<paramName>'] — where <paramName> is the name of the
                                     Path parameter set in the Method Request page.

    event['body'] — to reference the request body object.

    event['query']['<paramName1>']['<paramName2>'] ['<paramName…>'] — where <paramName>
     is the name of the Query parameter(s) set in the URL Query String
     Parameters section of the Method Request page.
   ```

