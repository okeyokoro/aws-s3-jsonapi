# s3-json-api

## TEST IT OUT LIVE

hit https://aw9z3rf567.execute-api.us-east-1.amazonaws.com/v1/s3-buckets/default

## DEPLOY IT YOURSELF

```sh
cd s3-json-api
pipenv install
# pipenv shell

cd iac

# display the CloudFormation template that is generated
aws okta exec {role} -- cdk synth

# the bootstrap command only creates an S3 bucket to store our CloudFormation
# we only need to run this command once (on our first go)
aws-okta exec {role} -- cdk bootstrap

aws-okta exec {role} -- cdk deploy

# * make some changes locally *

aws-okta exec {role} -- cdk deploy

# see the stack in the aws console

aws-okta login {role}
```

## DESIGN

Each "Part" will be in a separate branch

### Part 1

AWS CDK for:

- **API Gateway**

- **Lambda**

- **S3 bucket**


The **Lambda** function is an API endpoint

- use `flask-smorest` to get api documentation for free
- `GET /v1/s3-buckets/default/` will list files in the default s3-bucket
- `GET /v1/s3-buckets/random-s3-bucket-name` will try to access the s3 bucket and list files
   - the user has the option of passing in AWS credentials as HTTP Headers
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
- all responses are in **JSON:API** format with `marshmallow-json-api`
- will use **boto** to access S3
- 
- status codes:
   - `200` success
   - `404` bucket does not exist
   - `402` unauthorized request (tried to access private bucket without creds)


The **S3** bucket created will be a default

- it should be a private/secured s3 bucket
- s3 data will be added manually from the command-line
   - `aws-okta exec -- aws s3 cp ... ...`
   - ^ you have to use the same profile you used to create the cloudformation stack


The **API Gateway** will be created to connect the **Lambda** to the internet

- should just have some routing rules



### Part 2

AWS CDK for:

- **VPC**

- **RDS Serverless**


The **RDS db** will need some design

- let's just have a db table called `s3_buckets`
   - it will store the `name` of all the s3 buckets this api has tried to reach
   - a `default` column (for the default s3 bucket)
   - `last_api_call_status_code` column (whether we could reach it or not)
   - `last_updated` column


The **Lambda** will need a new endpoint for:

- listing records from the RDS database
   - `GET /v1/s3-buckets/`
   - just data from the s3_bucket table of the database
   - in JSON:API format


The **VPC** for connecting the **Lambda** to the **RDS** instance



### Part 3

AWS CDK for:

- **CodePipeline**

- **CodeDeploy**

- **CodeBuild**


The **Lambda** will need a new endpoint for:

- creating data
   - `PUT /v1/s3-buckets/default`
   - ^ this will:
      - upload file to s3
      - update/create a record in the RDS db `s3_buckets` table


**CodePipeline** for X

- notes


**CodeDeploy** for X

- notes


**CodeBuild** for X

- notes
