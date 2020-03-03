Feature: List contents of s3 bucket

    As a User,
    I want to make a GET request to an endpoint (specifying an S3 bucket name)
    So that I can see the contents of the s3 bucket in JSON:API format

    Scenario: User wants to see the contents of an S3 bucket in JSON:API format
        Given I have access to the S3 bucket specified
        When I make a GET request
        Then I get returned the contents of the S3 bucket in JSON:API format
