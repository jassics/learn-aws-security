#!/usr/bin/python
import sys
import boto3
import time
import re
import dns.resolver #import the module

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    print("python script-name profile-type\n")
    exit(0)

env_type = sys.argv[1]

ec2_client = boto3.client('ec2')
regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

timestr = time.strftime("%Y%m%d-%H%M%S")

elb_file = open("elb-publicip-"+env_type+"-list-"+timestr+".txt", "w")

elb_dns = []

for region in regions:
    profile   = boto3.session.Session(profile_name=env_type, region_name=region)
    elbList   = profile.client('elb')
    applbList = profile.client('elbv2')

    bals    = elbList.describe_load_balancers()
    appbals = applbList.describe_load_balancers()

    for elb in bals['LoadBalancerDescriptions']:
        if(elb['Scheme'] == "internet-facing"):
            elb_dns.append(elb['DNSName'])

    
    for elb in appbals['LoadBalancers']:
        if(elb['Scheme'] == "internet-facing"):
            elb_dns.append(elb['DNSName'])

for elb in elb_dns:
    myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
    try:
        myAnswers = myResolver.query(elb, "A") #Lookup the 'A' record(s) for google.com
        elb_file.write(elb+"\n")
    except dns.resolver.NXDOMAIN:
        pass
    for rdata in myAnswers: #for each response
        if(re.search("^10\.", str(rdata))):
            continue
        elb_file.write("\t"+str(rdata)+"\n") #print the data

