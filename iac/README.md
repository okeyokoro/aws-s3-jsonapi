## OVERVIEW

AWS CDK infrastructure as code

## LEARNING RESOURCES

- https://github.com/aws-samples/aws-modern-application-workshop/tree/python-cdk/module-2

- https://github.com/aws-samples/aws-cdk-examples

- https://docs.aws.amazon.com/cdk/api/latest/python/index.html

- https://github.com/aws-samples/aws-cdk-examples/blob/master/python/docker-app-with-asg-alb/

- https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html

- https://blog.codecentric.de/en/category/cloud-architecture/

- https://www.techopedia.com/definition/6157/bastion-host

- https://aws.amazon.com/about-aws/whats-new/2017/11/amazon-api-gateway-supports-endpoint-integrations-with-private-vpcs/

- https://aws.amazon.com/blogs/compute/using-api-gateway-with-vpc-endpoints-via-aws-lambda/

- https://www.youtube.com/watch?v=zysuUVNfhAE

- https://www.youtube.com/channel/UCSLIvjWJwLRQze9Pn4cectQ/playlists

- https://www.youtube.com/watch?v=Lnv9QCRGiMs&list=PLGyRwGktEFqcU7hnjdB08zpBasQcBcz82

- https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_rds.README.html


## Stacks as Bounded Contexts (DDD)

Within each Stack you have 1 or more Resources
Resources are just (thin) wrappers on top of actual aws(-cdk)-resources/services

A Stack on the other hand is a bounded context,
A bounded context is a stand-alone, logically-internally-coherent
role/entity/concept (group of resources)
that could actually be swapped out with a stack from another vendor

e.g. an AWS CI/CD Stack would consist of CodePipeline, CodeCommit, Code Deploy
But we could imagine swapping the above stack out for:
a Hand-rolled CI/CD Stack consisting of Gitlab services

Other stacks include:

- user_iam stack ( AWS Cognito )

- static_site stack ( Cloudfront + S3 )

- vpc stack (VPC, Subnets [Public, Private, AZs] )

- ecr stack

- ci_cd stack

- api_gw_lambda stack ( API Gateway + Lambda )

- s3 stack
- rds stack
- rds serverless stack
- dynamodb stack

- alb_fargate stack

- kafka stack

Then we can have a shared module of IAM resources

IMPORTANT NOTE:

Resources will strive to remain flexible, composible

But Stacks are concrete (not generalizible) and very limited in composability

### Rule of Thumb

You should be able to copy any file in the `resources` folder into a new project
without having to `edit` any of the classes (obeying the Liskov Substitution Principle)
but perhaps being able to `extend` classes

The above is untrue for Stacks as they are concrete classes with specific
orchestration details. You may only be able to port them across projects (without editing)
if you are truly following the same specific use-case across the two projects
