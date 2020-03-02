Goals: Increase capabilities and knowledge of AWS

End state - deploy a simple app backend that has an HTTP API

This is self directed learning

Start in the console to learn the concepts

The week of March 2nd present your code to the team:
- Show a working curl/postman script for 2.2 and 2.3
- Explain any difficultly and how it was overcome if it was
- Share any particular lessons learned or things you thought were neat and/or not-neat
- Share any questions

1. Understand the primitives: compute, storage, networking
	1. Build a Lambda (using python) that outputs the files and directories from an S3 bucket in JSON:API format that is reachable from the internet
		- Concepts and things in doing this:
			- Lambda
			- S3
			- boto3
			- API Gateway
			- JSON:API

	2. Build a VPC wherein a Lambda can connect to an RDS Serverless (mysql or postgres) database and list some records
		- Concepts and things in doing this:
			- VPCs
			- Subnets
			- CIDR
			- RDS
			- Security Groups
			- Secrets management

2. Building on the primitives: CloudFormation, Code<Blah>
	1. Create the infrastructure for 1.1 using CloudFormation and ensure the application works; the S3 data can be added manually
		- Concepts and things in doing this:
			- CloudFormation

	2. Create the infrastructure for 1.2 using CloudFormation, ensure the application is setup during the pipeline; the app works
		- Concepts and things in doing this:
			- CloudFormation
			- CodePipeline
			- CodeDeploy
			- CodeBuild

	3. Create the infrastructure for (2) and add an endpoint to create the data
		- Concepts and things in doing this:
			- Everything thus far

- Optionally complete Architecting Serverless Solutions https://www.aws.training/Details/eLearning?id=42594
