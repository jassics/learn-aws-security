from collections import defaultdict
import boto3

# Instance count client interface
ec2 = boto3.client('ec2', region_name='us-east-1')
idesc = ec2.describe_instances()
total = len(idesc['Reservations'])
print ("Total: ", total)

# Resource Interface 
ec2 = boto3.resource('ec2', region_name='us-east-1')
for instance in ec2.instances.all():
    print (instance, instance.tags)


"""
A tool for retrieving basic information from the running EC2 instances.
"""

# Connect to EC2
ec2 = boto3.resource('ec2', region_name='us-east-1')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = defaultdict()
for instance in running_instances:
    name = "NA"
    for tag in instance.tags or []:
        if 'Name'in tag['Key']:
            name = tag['Value']
    # Add instance info to a dictionary         
    ec2info[instance.id] = {
        'Name': name,
        'Type': instance.instance_type,
        'State': instance.state['Name'],
        'Private IP': instance.private_ip_address,
        'Public IP': instance.public_ip_address,
        'Launch Time': instance.launch_time
        }

attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
for instance_id, instance in ec2info.items():
    for key in attributes:
        print("{0}: {1}".format(key, instance[key]))
    print("------")
