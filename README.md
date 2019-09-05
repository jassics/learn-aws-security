# AWS Security and its automation Related Scripts :shipit:

## Purpose of this repo
A repo to cover AWS and its Security through various hands-on scripts. We will try to cover AWS Security automation as well, wherever it's possible.

_**Note:**_ One can use these perl/python scripts separately as well. Few script might have some dependencies on other scripts.  

## AWS Security and its Automation
This repo covers the security aspects of AWS. We will deal with EC2 instances, S3, VPC, IAM etc. and related security tools and scripts available in AWS like Inspector, CloudTrail, CloudWatch, GuardDuty, TrustedAdvisor, Config

## How do I run these script? Any prerequisites?

## MacOS

### Python3
Python version should be >= python3.7.x to run these scripts without any error

Check Python version, Usually it will be python 2.x.x
`python --version`

#### Install python3 (My Favorite :heart:)
In Mac `brew install python3` and `brew postinstall python3`

Note: It will automagically install pip3 too!

#### pip
Check if pip is installed by running below command:
`pip --version`

*Ex: pip 19.0.2 from /usr/local/lib/python2.7/site-packages/pip (python 2.7)*

**Same for pip3:**

`pip3 --version`

It should show Python3.x in that result.

Ex: `pip 19.0.2 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)`

### boto3
Install using `pip3 install boto3`

## AWS CLI
You should have installed aws cli in your local machine. Please check if `aws configure` works for you. If yes, means its installed in your machine. if not, follow below instructions:

`pip3 install awscli` or `pip install awscli`

And check if following command works: `aws --version`

It should result like: `aws-cli/1.11.190 Python/2.7.10 Darwin/18.2.0 botocore/1.7.48`

### Setting up profile :closed_lock_with_key:
Once awscli is installed. Make sure you have access key and secret key is ready to run `aws configure` command
Once you are done with `aws configure` successfully, You would see ~/.aws directory. 
You should have two files `config` and `credentials`. config file saves default region and default output format for various profiles. credentials saves aws secret key and access key

To setup the profile like dev, test, prod, staging etc. (default is be default setup there). Open `~/.aws/credentials` file and add something like below for various profiles. (profile is the keyword that you see inside 2 sqaure brackets).

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

# Overview of AWS resources and tasks that we will cover
1. EC2
2. IAM
3. S3
4. VPC
5. Route53
6. Security Config
7. Serverless Review
8. Walkthrough of Inspector, CloudTrail, CloudWatch, TrustedAdvisor, Macie etc.
9. Security Automation using AWS CI/CD tools and Ansible, Terraform, CloudFormation etc.

# ToDOs
- [x] Create README.md
- [x] List details of EC2 instance having public IP with CIDR 0.0.0.0/0
- [x] List all EC2 instances and get public IPs
- [x] List Security groups
- [x] Audit Security groups
- [x] List orphan security groups
- [ ] More to go here

# Troubleshoot :trollface:
## Issue 1:
If you get permission denied error while installing, run command with sudo.
Example: We got error while running `pip3 install awscli --upgrade --user` or `pip install awscli --upgrade --user`

*ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/Users/username/Library/Python/3.7'
Check the permissions.*

*Solution:* `sudo pip3 install awscli --upgrade --user` or `sudo pip install awscli --upgrade --user`

## Issue 2:
If you have somehow messed with brew and python installation.I am more concerned for Python3 though.
Run below command in Mac for fresh installation.
You might have installed python from the official site instead of via brew. Open a terminal window and let's try to fix this: 

1. First, let's uninstall previous Python versions:

    `sudo rm -rf /Library/Frameworks/Python.framework`
    
    `sudo rm -rf /usr/local/bin/python3`
2. Then, remove the previous frameworks from the $PATHvariable:

    `nano ~/.bash_profile`
  
 You will see something like that:

    # Setting PATH for Python 2.7
    # The original version is saved in .bash_profile.pysave
    PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
    export PATH

    # Setting PATH for Python 3.7
    # The original version is saved in .bash_profile.pysave
    PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:${PATH}"
    export PATH`

This is the problem: These paths don't exist. Comment the $PATH editions (or erase them):

    # Setting PATH for Python 2.7
    # The original version is saved in .bash_profile.pysave
    # PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
    # export PATH

    # Setting PATH for Python 3.6
    # The original version is saved in .bash_profile.pysave
    # PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:${PATH}"
    # export PATH
    
3. Restart the computer and install via Homebrew Python 2 and 3:

    `brew update`
    
    `brew install python`
    
    `brew install python3`

Now, if type python3 --version I get Python 3.7.0, and everything works fine :)

4. If it says it’s already installed and you just need to link it. Then do the below steps:

*Error:* 
    `brew install python3`
	Warning: python 3.7.4 is already installed, it's just not linked
	You can use `brew link python` to link this version.

*Solution:* `brew link python`
	Linking /usr/local/Cellar/python/3.7.4... 33 symlinks created

Test if it showing usr/local/bin/python3 now?
`which python3`
	/usr/local/bin/python3
	
## Issue 3:
If some module is not installed and got an error. 
*Error*:
```Traceback (most recent call last):
 File "some-filename.py", line 6, in <module>
   import dns.resolver #import the module
ModuleNotFoundError: No module named 'dns'
```
*Solution*:
`pip3 install dnspython`

# Contact us
[jassics]
