from collections import defaultdict
import boto3
import sys
import time

# Ex: python get-ec2-publicips.py <profile>   profile can be dev|prod|ds
# 1. Get region names in an array
# 2. for each region_name loop through the regions and print public IP address
#    for the instances which are in running state.

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    print("You should pass the argument.\nEx: python " + sys.argv[0] + " profile-type(dev|prod|ds)\n")
    exit(0)

# 1. Get Region Names in an array
# Retrieves all regions/endpoints that work with EC2
# List all regions
ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

# 2. for each profile and region, loop through to print publicIP
# open a file, create if not exists with timestamp in it
timestr = time.strftime("%Y%m%d-%H%M%S")
f = open("ec2-" + profile + "-publicip-"+timestr+".txt", "w")

# loop through the regions
for region in regions:
    # Connect to EC2
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')

    # Get information for all running instances
    running_instances = ec2.instances.filter(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['running']}])

    ec2info = defaultdict()
    for instance in running_instances:
        # Add instance info to a dictionary         
        ec2info[instance.id] = {
            'Public IP': instance.public_ip_address,
            }

    attributes = ['Public IP']
    
    for instance_id, instance in ec2info.items():
        for key in attributes:
            if(instance[key]!= None):
                f.write("{0}".format(instance[key])+"\n")
f.close()

