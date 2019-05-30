# AWS Security and its automation Related Scripts :shipit:

## Purpose of this repo
A repo to cover AWS and its Security through various hands-on scripts. We will try to cover AWS Security automation as well, wherever it's possible.

_**Note:**_ One can use these perl/python scripts separately as well. Few script might have some dependencies on other scripts.  

## AWS Security and its Automation
This repo covers the security aspects of AWS. We will deal with EC2 instances, S3, VPC, IAM etc. and related security tools and scripts available in AWS like Inspector, CloudTrail, CloudWatch, GuardDuty, TrustedAdvisor, Config

## How do I run these script? Any prerequisites?

## MacOS

### Python
Python version should be >= python3.7.x to run these scripts without any error

Check Python version, Usually it will be python 2.x.x
`python --version`

#### Install python3 (My Favorite :heart:)
In Mac `brew install python3` and `brew postinstall python3`

Note: It will automagically install pip3 too!

### pip
Check if pip is installed by running below command:
`pip --version`

*Ex: pip 19.0.2 from /usr/local/lib/python2.7/site-packages/pip (python 2.7)*

**Same for pip3:**

`pip3 --version`

It should show Python3.x in that result.

Ex: `pip 19.0.2 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)``

### boto3
Install using `pip3 install boto3`

## AWS CLI
You should have installed aws cli in your local machine. Please check if `aws configure` works for you. If yes, means its installed in your machine. if not, follow below instructions:

`pip3 install awscli` or `pip install awscli`

And check if following command works: `aws --version`

It should result like: `aws-cli/1.11.190 Python/2.7.10 Darwin/18.2.0 botocore/1.7.48`

### Setting up profile :closed_lock_with_key:
Once awscli is installed. You would see ~/.aws directory.
You should have two files `config` and `credentials`

To setup the profile like dev, test, prod, staging etc. (default is be default setup there)

```
[default]
aws_access_key_id = XXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXX

[dev]
aws_access_key_id = XXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXX

[prod]
aws_access_key_id = XXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXX

[staging]
aws_access_key_id = XXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXX
```

# Troubleshoot


# Overview of AWS resources that we will cover
1. EC2
2. IAM
3. S3
4. VPC
5. Route53
6. Security Config
7. Walkthrough of Inspector, CloudTrail, CloudWatch, TrustedAdvisor etc.
8. Security Automation using AWS CI/CD tools like Ansible, Terraform, CloudFormation

# ToDOs
- [x] Create README.md
- [x] List details of EC2 instance having public IP with CIDR 0.0.0.0/0
- [x] List all EC2 instances and get public IPs
- [ ] List s3 bukets and associated policies
- [x] List Security groups
- [x] Audit Security groups
- [ ] List all MFA enabled users
- [ ] Get Security config in json format
- [ ] Audit S3 buckets
- [x] Get ELB details
- [x] Get ELB Public IPs
- [x] List orphan security groups
- [ ] More to go here

# Troubleshoot :trollface:
If you get permission denied error while installing, run command with sudo.

Example: We got error while running `pip3 install awscli --upgrade --user` or `pip install awscli --upgrade --user`

*ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/sjaiswal/Library/Python/3.7'
Check the permissions.*

*Solution:* `sudo pip3 install awscli --upgrade --user` or `sudo pip install awscli --upgrade --user`

# Contact us
[jassics]
