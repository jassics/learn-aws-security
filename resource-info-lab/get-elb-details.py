#!/usr/bin/python
import sys
import boto3
import time

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    print("python script-name profile-type\n")
    exit(0)

env_type = sys.argv[1]

ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

timestr = time.strftime("%Y%m%d-%H%M%S")

elb_file = open("elb-"+env_type+"-list-"+timestr+".txt", "w")

for region in regions:
    profile = boto3.session.Session(profile_name=env_type, region_name=region)
    elbList = profile.client('elb')
    ec2 = profile.resource('ec2')

    bals = elbList.describe_load_balancers()

    for elb in bals['LoadBalancerDescriptions']:
        elb_file.write(elb['DNSName'] + ", " + elb['Scheme']+"\n")
        for ec2Id in elb['Instances']:
            running_instances = \
                ec2.instances.filter(Filters=[{'Name': 'instance-state-name'
                                 , 'Values': ['running']},
                                 {'Name': 'instance-id',
                                 'Values': [ec2Id['InstanceId']]}])
            for instance in running_instances:
                if(instance.public_ip_address):
                    elb_file.write("Instance: " + instance.instance_id + ", " + instance.public_ip_address + "\n");
