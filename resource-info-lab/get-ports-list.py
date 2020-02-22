#!/usr/bin/python3
import boto3
import sys
import time

# check if argument is passed
if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    print("You should pass the arguments. \nEx: python " + sys.argv[0] + " profile-type(dev|prod|ds)\n")
    exit(0)

# Get Region Names in an array
# Retrieves all regions/endpoints that work with EC2
# List all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# open a file, create if not exists with timestamp in it
timestr = time.strftime("%Y%m%d-%H%M%S")
sg_file = open("sg-" + profile + "-ports-"+timestr+".txt", "w")

session = boto3.Session(profile_name=profile)

port_list = []

# loop through regions followed by security group loop
# get port lists from sg group based on profile like for dev,prod,ds
for region in regions:
    ec2 = session.client('ec2', region_name=region)
    response = ec2.describe_security_groups()

# save it in a file with unique ports in sorted order
    for i in response['SecurityGroups']:
       for j in i['IpPermissions']:
           try:
               if j['FromPort'] == 0:
                  continue 
               port_list.append(j['FromPort'])
           except Exception:
              continue


# numeric sorting
port_list.sort(key=int)

# unique listing
unique_port = list(set(port_list))

# Unique and sorted
unique_port.sort(key=int)

for port in unique_port:
    sg_file.write(str(port) + "\n")

sg_file.close()

