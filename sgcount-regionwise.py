#!/usr/bin/python
import boto3
import sys
import time

# Ex: python sgcount-regionwise.py <profile>   profile can be dev|prod|ds
# 1. Get region names in an array
# 2. for each region_name loop through the regions and print sg count

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    print("You should pass the argument.\nEx: python " + sys.argv[0] + " profile-type(dev|prod|ds)\n")
    exit(0)

# 1. Get Region Names in an array
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# 2. for each profile and region, loop through to print sg count
# open a file, create if not exists with timestamp in it
timestr = time.strftime("%Y%m%d-%H%M%S")
f = open("sgcount-" + profile + "-active-"+timestr+".txt", "w")

session = boto3.Session(profile_name=profile)
total_count = 0
# loop through regions followed by security group loop
for region in regions:
    ec2 = session.client('ec2', region_name=region)
    #sgs = ec2.describe_security_groups()
    #for sg in sgs:
        #print(sg)
    count = 0
    for sg in ec2.describe_security_groups()["SecurityGroups"]:
        count = count + 1
    total_count += count
    f.write(region + ": " + str(count) + "\n")
f.write("Total count: " +  str(total_count) + "\n")

f.close()
