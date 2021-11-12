#!/usr/bin/python3
import boto3

def list_regions():
    ec2 = boto3.client('ec2')

    # Retrieves all regions/endpoints that work with EC2
    response = ec2.describe_regions()
    regions = response['Regions']
    region_names = []

    for region in regions:
        region_names.append(region['RegionName'])

    # returns regions names in a list
    return region_names

def print_regions(list_regions):
    region_names = list_regions()

    print("######### Regions ##########")
    print("Total available Regions: ", len(region_names))

    for region in region_names:
        print(region)


def list_azs(list_regions):
    region_names = list_regions()
    azs_dict = {}

    # Retrieves availability zones for all available region for the ec2 object
    for region in region_names:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_availability_zones()
        azs = response['AvailabilityZones']

        for az in azs:
            if region not in azs_dict:
                azs_dict[region] = []

            azs_dict[region].append(az['ZoneName'])

    return azs_dict

def print_azs(list_azs):
    azs_dict = list_azs(list_regions)

    print("\n######### Availability Zones ##########")
    for region in azs_dict:
        print("{} ({})".format(region, len(azs_dict[region]) ))
        for az in azs_dict[region]:
            print("\t", az)

print("Getting Available Regions\n")
print_regions(list_regions)
print("\n\nGetting AZs for above listes Regions")
print_azs(list_azs)
