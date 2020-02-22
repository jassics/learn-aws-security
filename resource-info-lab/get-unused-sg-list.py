#!/usr/bin/python3
import boto3
import argparse
import time

# This script will take profile and region name as a parameter and 
# will fetch all unused security group by looking at EC2, ELBs, ALBs, RDS
# Improvement suggested by Prabhakar : check if security group is referenced by
# another security group or not.
# Improvement suggested by Yogi: Check Lambda, ElasticSearch etc for few more
# security groups. Could be less but can be more useful if we have this case.


# get a full list of the available regions
client = boto3.client('ec2')
regions_dict = client.describe_regions()
region_list = [region['RegionName'] for region in regions_dict['Regions']]

# parse arguments
parser = argparse.ArgumentParser(description="Show unused security groups count")

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-r", "--region", type=str, required=True, help="The list of available regions are as follows: %s" % sorted(region_list))
parser.add_argument("-p", "--profile", type=str, default='default', help="profile required to run the script i.e. dev|prod|beta etc. Default profile is 'default' ")
args = parser.parse_args()

if args.region:
    region = args.region

if args.profile:
    profile = args.profile


# open a file, create if not exists with timestamp in it
timestr = time.strftime("%Y%m%d-%H%M%S")
unused_sg_file = open("orphan-sg-" + profile + timestr+".txt", "w")

session = boto3.session.Session(profile_name=profile, region_name=region)
ec2 = session.client('ec2')
all_groups = []
security_groups_in_use = []

# Get ALL security groups ids
security_groups_dict = ec2.describe_security_groups()
security_groups = security_groups_dict['SecurityGroups']
for groupobj in security_groups:
    if groupobj['GroupName'] == 'default' and groupobj['GroupName'] not in security_groups_in_use:
        security_groups_in_use.append(groupobj['GroupId'])
    all_groups.append(groupobj['GroupId'])

# Get all security groups used by instances
instances_dict = ec2.describe_instances()
reservations = instances_dict['Reservations']

network_interface_count    = 0
ec2_instance_sg_count      = 0
elb_sg_count               = 0
elb2_sg_count              = 0
rds_sg_count               = 0
network_interface_sg_count = 0
public_ec2_count           = 0
public_elb_count           = 0
public_rds_count           = 0

for i in reservations:
    for j in i['Instances']:
        for k in j['SecurityGroups']:
            if k['GroupId'] not in security_groups_in_use:
                security_groups_in_use.append(k['GroupId'])
                try:
                    if j['PublicIpAddress']:
                        public_ec2_count +=1
                except KeyError:
                    pass
                ec2_instance_sg_count += 1
        # Security groups used by network interfaces
        for m in j['NetworkInterfaces']:
            network_interface_count += 1
            for n in m['Groups']:
                if n['GroupId'] not in security_groups_in_use:
                    security_groups_in_use.append(n['GroupId'])
                    network_interface_sg_count += 1

# Security groups used by classic ELBs
elb_client = session.client('elb')
elb_dict = elb_client.describe_load_balancers()
for i in elb_dict['LoadBalancerDescriptions']:
    for j in i['SecurityGroups']:
        if j not in security_groups_in_use:
            security_groups_in_use.append(j)
            elb_sg_count += 1
            if(i['Scheme'] == 'internet-facing'):
                public_elb_count += 1

# Security groups used by ALBs
elb2_client = session.client('elbv2')
elb2_dict = elb2_client.describe_load_balancers()
for i in elb2_dict['LoadBalancers']:
    for j in i['SecurityGroups']:
        if j not in security_groups_in_use:
            security_groups_in_use.append(j)
            elb2_sg_count += 1
            if(i['Scheme'] == 'internet-facing'):
                public_elb_count += 1

# Security groups used by RDS
rds_client = session.client('rds')
rds_dict = rds_client.describe_db_security_groups()

for i in rds_dict['DBSecurityGroups']:
    for j in i['EC2SecurityGroups']:
        if j['EC2SecurityGroupId'] not in security_groups_in_use:
                security_groups_in_use.append(j['EC2SecurityGroupId'])
                rds_sg_count += 1

unused_sgs = []
for group in all_groups:
    if group not in security_groups_in_use:
        unused_sgs.append(group)

if(len(unused_sgs)):
    unused_sg_file.write("The list of unused security groups.\n")
for group in sorted(unused_sgs):
    unused_sg_file.write("   " + group + "\n")

unused_sg_file.write("---------------\n")
unused_sg_file.write("Activity Report\n")
unused_sg_file.write("---------------\n")

unused_sg_file.write(u"Total number of EC2 Instances evaluated: {0:d}\n".format(len(reservations)))
unused_sg_file.write(u"Total number of public EC2 Instances evaluated: {0:d}\n".format(public_ec2_count))
unused_sg_file.write(u"Total number of Load Balancers evaluated: {0:d}\n".format(len(elb_dict['LoadBalancerDescriptions']) + len(elb2_dict['LoadBalancers'])))
unused_sg_file.write(u"Total number of public Load Balancers evaluated:{0:d}\n".format(public_elb_count))
unused_sg_file.write(u"Total number of Network Interfaces evaluated: {0:d}\n".format(network_interface_count))
unused_sg_file.write(u"Total number of RDS Instances evaluated: {0:d}\n".format(len(rds_dict['DBSecurityGroups'])))
unused_sg_file.write(u"\nTotal number of Security Groups: {0:d}\n".format(len(all_groups)))
unused_sg_file.write(u"Total number of Security Groups in use: {0:d}\n".format(len(security_groups_in_use)))
unused_sg_file.write(u"Total number of EC2 Security Groups in use: {0:d}\n".format((ec2_instance_sg_count)))
unused_sg_file.write(u"Total number of ELB Security Groups in use: {0:d}\n".format((elb_sg_count)))
unused_sg_file.write(u"Total number of ALB Security Groups in use: {0:d}\n".format((elb2_sg_count)))
unused_sg_file.write(u"Total number of RDS Security Groups in use: {0:d}\n".format((rds_sg_count)))
unused_sg_file.write(u"Total number of Network Interface Security Groups in use: {0:d}\n".format((network_interface_sg_count)))
unused_sg_file.write(u"\nTotal number of orphan security groups: {0:d}\n".format(len(unused_sgs)))

# Ratio of unused security groups.
ratio_unused_sg = str((len(unused_sgs)/len(all_groups))*100.0)
unused_sg_file.write("Ratio of unused Security Group: " + str(round(float(ratio_unused_sg))) + "% \n")

unused_sg_file.close()
