#!/usr/bin/python
import boto3
import sys
import time

# IMPROVEMENT
# Need to add instance id as well.
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
sg_file = open("sg-" + profile + "-list-"+timestr+".txt", "w")

session = boto3.Session(profile_name=profile)

# loop through regions followed by security group loop
for region in regions:
    ec2 = session.client('ec2', region_name=region)
    response = ec2.describe_security_groups()

    for i in response['SecurityGroups']:
       sg_file.write("\nSecurity Group Name: "+i['GroupName']+"\n")
       sg_file.write("Security Group Id: "  +i['GroupId']+"\n")
       sg_file.write("Region: "  +region+"\n")
       
       sg_file.write("Egress:"+"\n")
       for j in i['IpPermissionsEgress']:
           sg_file.write("IP Protocol: "+j['IpProtocol']+"\n")
           for k in j['IpRanges']:
              sg_file.write("IP Ranges: "+k['CidrIp']+"\n")
       
       sg_file.write("\nIngress\n")
       for j in i['IpPermissions']:
           sg_file.write("IP Protocol: "+j['IpProtocol']+"\n")
           iprange = []
           try:
              sg_file.write("PORT: "+str(j['FromPort'])+"\n")
              for k in j['IpRanges']:
                  iprange.append(k['CidrIp'])
              sg_file.write("IP Ranges: " + ';'.join( iprange ) + "\n")
           except Exception:
              sg_file.write("No value for ports and ip ranges available for this security group"+"\n")
              continue

sg_file.close()
