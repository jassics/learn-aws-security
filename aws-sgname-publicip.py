#!/usr/bin/python
import boto3
import json

all_ec2 = {}
filters = [{'Name':'instance.group-name', 'Values':['*ssh*']}]

# To list all the available regions in AWS
region_names = [x['RegionName'] for x in boto3.client('ec2').describe_regions()['Regions']]

# print security group which contains preprod keyword and associated public IP
# address, if exists
for region_name in region_names:
    print("Looking for instances with security group having ssh keyword in region: " + region_name + " .")
    for reservation in boto3.client('ec2', region_name=region_name).describe_instances(Filters=filters)['Reservations']:
        for instance in reservation['Instances']:
            for sg in instance.get('SecurityGroups', []):
                all_ec2[instance['InstanceId']] = instance
                print(sg)
                print(instance['PrivateIpAddress'])

