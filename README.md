# Lambda@Edge Work-arounds

This repository illustrates three ways of passing parameters to AWS Lambda@Edge function in a Serverless Application Model template. A common use-case is passing names and ARNs of AWS resources that the function uses, like S3 buckets, DynamoDB tables or Cognito User Pools.

## Motivation

Lambda@Edge functions impose several restrictions, in particular environment variables and layers supported by ordinary Lambda functions are not available in Lambda@Edge. If for example, you are writing a Lambda@Edge function for user authorisation that requires access to Cognito User Pool you are no longer able to save the pool ID in an environmental variable that the function can access. While considering different options for overcoming this limitation I often found myself in a vicious circle situation where in order to pass a parameter into the function I needed to first pass another parameter.

The problem is easily solved by using CI/CD infrastructure, spliting your resources into multiple stacks and using build scripts. For smaller projects with simple architectures you might not want to use CI/CD and need other solutions. In this repository three such options are illustrated: inlining the code into a template, using CloudFront custom headers, and saving parameters in AWS Secrets Manager.

## Prerequisites

It is assumed that you have a AWS SAM CLI [installed and configured](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) in your system. Please check that SAM has sufficient credentials to create IAM roles, CloudFront distributions and secrets in Secrets Manager.

The example code uses Python 3.9 runtime which SAM CLI should be able to access to package dependencies.

## Installation

After you cloned the repository you should be good to go.

## Building and Deploying

First, build the code with SAM CLI:

```bash
sam build
```

To deploy the application run:

```bash
sam deploy --guided
```

The only option that you need to change from default values is the name of your SAM AWS profile (the default is `sam`). Creating a CloudFront distribution is a great undertaking and requires several minutes to complete.

## Testing the Deployment

Check the output of the `deploy` command. It should contain the URL of the CloudFront distribution, something like `d65sht5q5cgs1e.cloudfront.net`. Open this URL in the browser.

When you navigate to either of the two links you should see a text document in YAML format with the name of the bucket, the name, size and date its objects and their total size. On creation the bucket is empty.

Try uploading some files into the `resource-accessed-from-edge-lambda` bucket. If you use AWS CLI you can run:

```bash
aws s3 cp README.md s3://resource-accessed-from-edge-lambda --profile sam
```

to copy this README.md file into the bucket. Here we use `sam` profile to upload the file as it should have the required permissions. Alternatively, use AWS S3 console, locate the bucket and upload some files manually.

Reload the the page and you should see the updated bucket content.

## Clean up

First, empty the bucket:

```bash
aws s3 rm s3://resource-accessed-from-edge-lambda --recursive --profile sam
```

Then delete your stack:

```bash
sam delete
```

You are going to get an error message regarding deleting replicated Lambda@Edge functions. Unfortunately, they can not be immediately deleted by CloudFormation. Please see [AWS Documentation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/lambda-edge-delete-replicas.html) for details. To make sure the resources are deleted go CloudFormation console and delete the stack manually. You can choose to retain the three lambda functions we've created and delete the rest of the stack, then come back a few hours later and check at the Lambda console if you still need to delete the functions.

## Resources

A detailed discussion of the project can be found in the accompanying [post](blog.kosobrodov.net).
If you found this information useful please give this repository a star on GitHub.
