# myresume
deploying my resume


# Welcome to CloudmyTribe Community Project Challenges! 🤝

## Table of Contents
1. [Introduction](#introduction-)
2. [Your Cloud Resume Challenge: Host Your Static Website on AWS](#your-cloud-resume-challenge-host-your-static-website-on-aws)
   - [Milestone 1: Deploying with the AWS Console](#milestone-1--deploying-with-the-aws-console-)
     - [Step-by-Step Guide](#step-by-step-guide)
       - [Prepare Your Tools](#prepare-your-tools)
       - [Explore AWS Documentation](#explore-aws-documentation)
       - [Build Your Architecture Diagram](#build-your-architecture-diagram)
       - [Create Your HTML Resume](#create-your-html-resume)
       - [Style Your Resume with CSS](#style-your-resume-with-css)
       - [Deploy Your Resume as a Static Website on S3](#deploy-your-resume-as-a-static-website-on-s3)
       - [Enable HTTPS with CloudFront](#enable-https-with-cloudfront)
       - [Set Up Custom DNS with Route 53](#set-up-custom-dns-with-route-53)
       - [Configure IAM for Access Management](#configure-iam-for-access-management)
       - [Document Your Progress](#document-your-progress)
       - [Create a Screen Recording or Deploy a Live Website (Optional)](#create-a-screen-recording-or-deploy-a-live-website-optional)
     - [Deliverables](#deliverables-)
   - [Sneak Peak to Milestone 2](#sneak-peak-to-milestone-2-provisioning-your-infrastructure-as-code-)

## Introduction 👋

Welcome to the CloudmyTribe Cloud Challenge projects! This initiative is designed to help you build cloud-based products using AWS services. Whether you're just getting started with cloud technologies or looking to sharpen your skills, these projects offer a comprehensive, hands-on experience.

---

# Your Cloud Resume Challenge: Host Your Static Website on AWS

## MILESTONE 1 -> Deploying with the AWS Console 🚀

### Step-by-Step Guide

#### Prepare Your Tools
- **Action**: Ensure you have the necessary tools and accounts set up, including an **AWS account**, **GitHub account**, and a **gitpod** as your recommended CDE all connected to offer a seamless coding space.
- **Outcome**: Prepared environment for development and deployment.

#### Explore AWS Documentation
- **Action**: Dive into AWS documentation to familiarize yourself with the services needed for this challenge. Focus on:
  - [Amazon S3 (for static website hosting)](https://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html)
  - [AWS CloudFront (for CDN)](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
  - [Route 53 (for DNS management)](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
  - [IAM (for access management)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- **Outcome**: Knowledge of the services you'll be using, including best practices and configurations.

#### Build Your Architecture Diagram
- **Action**: Design an architecture diagram that outlines the structure of your static website hosting solution. Use tools like [draw.io](https://www.diagrams.net/), [Lucidchart](https://www.lucidchart.com/), or any diagramming tool you're comfortable with.
  - Include components like S3 bucket, CloudFront distribution, Route 53, and IAM roles/policies.
- **Outcome**: A comprehensive architecture diagram that visually represents the infrastructure.

#### Create Your HTML Resume
- **Action**: Write your resume in [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML). Not a Word doc, not a PDF. [Example](https://codepen.io/emzarts/pen/OXzmym).
- **Outcome**: A basic HTML file containing your resume.

#### Style Your Resume with CSS
- **Action**: Apply styling to your resume using [CSS](https://www.w3schools.com/css/). It doesn't have to be fancy, but it should be more than just raw HTML. Feel free to get creative.
- **Outcome**: A styled HTML resume file.

#### Deploy Your Resume as a Static Website on S3
- **Action**: Follow the steps below to deploy your HTML resume as a static website on S3.
  - **Create an S3 Bucket**:
    ```bash
    aws s3 mb s3://your-bucket-name
    ```
  - **Upload Your Website Files**:
    ```bash
    aws s3 cp /path/to/your/resume s3://your-bucket-name/ --recursive
    ```
  - **Configure the Bucket for Static Website Hosting**:
    ```bash
    aws s3 website s3://your-bucket-name/ --index-document index.html
    ```
  - **Set Permissions**:
    ```bash
    aws s3api put-bucket-policy --bucket your-bucket-name --policy '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": "s3:GetObject",
          "Resource": "arn:aws:s3:::your-bucket-name/*"
        }
      ]
    }'
    ```

- **Outcome**: Your resume hosted on an S3 static website.

#### Enable HTTPS with CloudFront
- **Action**: Use the following steps to enable HTTPS for your S3 website using CloudFront.
  - **Create a CloudFront Distribution**:
    ```bash
    DISTRIBUTION_ID=$(aws cloudfront create-distribution --origin-domain-name your-bucket-name.s3.amazonaws.com --default-root-object index.html --query 'Distribution.Id' --output text)
    ```
  - **Request an SSL Certificate**:
    ```bash
    aws acm request-certificate --domain-name yourdomain.com --validation-method DNS
    ```
  - **Retrieve Certificate ARN**:
    ```bash
    CERTIFICATE_ARN=$(aws acm list-certificates --query "CertificateSummaryList[?DomainName=='yourdomain.com'].CertificateArn" --output text)
    ```
  - **Update CloudFront Distribution with SSL**:
    ```bash
    aws cloudfront update-distribution --id $DISTRIBUTION_ID --default-root-object index.html --origins Quantity=1,Items=[{Id=1,DomainName=your-bucket-name.s3.amazonaws.com,OriginPath=,CustomHeaders={Quantity=0},S3OriginConfig={OriginAccessIdentity=}},DefaultCacheBehavior={TargetOriginId=1,ViewerProtocolPolicy=redirect-to-https,AllowedMethods={Quantity=2,Items=[GET,HEAD]},ForwardedValues={QueryString=false,Cookies={Forward=none}},TrustedSigners={Enabled=false,Quantity=0},ViewerCertificate={ACMCertificateArn=$CERTIFICATE_ARN,SSLSupportMethod=sni-only,MinimumProtocolVersion=TLSv1.2_2019},DefaultCacheBehavior={TargetOriginId=1,ViewerProtocolPolicy=redirect-to-https}}]
    ```

- **Outcome**: Your resume accessible over HTTPS.

#### Set Up Custom DNS with Route 53
- **Action**: Configure a custom domain to point to your CloudFront distribution using Route 53.
  - **Register a Domain**:
    ```bash
    aws route53 create-hosted-zone --name yourdomain.com --caller-reference $(date +%s)
    ```
  - **Retrieve Hosted Zone ID**:
    ```bash
    HOSTED_ZONE_ID=$(aws route53 list-hosted-zones-by-name --dns-name yourdomain.com --query "HostedZones[0].Id" --output text | cut -d'/' -f3)
    ```
  - **Create an Alias Record**:
    ```bash
    aws route53 change-resource-record-sets --hosted-zone-id $HOSTED_ZONE_ID --change-batch '{
      "Changes": [
        {
          "Action": "CREATE",
          "ResourceRecordSet": {
            "Name": "yourdomain.com",
            "Type": "A",
            "AliasTarget": {
              "HostedZoneId": "Z2FDTNDATAQYW2",  # CloudFront hosted zone ID
              "DNSName": "your-distribution.cloudfront.net",
              "EvaluateTargetHealth": false
            }
          }
        }
      ]
    }'
    ```

- **Outcome**: Your resume accessible at your custom domain.

#### Configure IAM for Access Management
- **Action**: Set up IAM roles and policies to manage access to your AWS resources.
  - **Create an IAM Role**:
    ```bash
    aws iam create-role --role-name S3AccessRole --assume-role-policy-document '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }'
    aws iam attach-role-policy --role-name S3AccessRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
    ```
  - **Create an IAM User**:
    ```bash
    aws iam create-user --user-name S3AccessUser
    aws iam attach-user-policy --user-name S3AccessUser --policy-arn arn:aws:iam::aws:policy/A
