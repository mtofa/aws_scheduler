import os
import json
from typing import Dict, Any, Union
import boto3
from scheduler.models import Regions


def run():
    pre_defined_region_country: Dict[Union[str, Any], Union[str, Any]] = {
        'ap-northeast-1': 'Asia Pacific (Tokyo)',
        'ap-northeast-2': 'Asia Pacific (Seoul)',
        'ap-south-1': 'Asia Pacific (Mumbai)',
        'ap-southeast-1': 'Asia Pacific (Singapore)',
        'ap-southeast-2': 'Asia Pacific (Sydney)',
        'ca-central-1': 'Canada (Central)',
        'eu-central-1': 'EU (Frankfurt)',
        'eu-north-1': 'EU (Stockholm)',
        'eu-west-1': 'EU (Ireland)',
        'eu-west-2': 'EU (London)',
        'eu-west-3': 'EU (Paris)',
        'sa-east-1': 'South America (São Paulo)',
        'us-east-1': 'US East (N. Virginia)',
        'us-east-2': 'US East (Ohio)',
        'us-west-1': 'US West (N. California)',
        'us-west-2': 'US West (Oregon)',
    }

    ec2_client = boto3.client('ec2', 'ap-southeast-2')
    response = ec2_client.describe_regions()

    for region in response['Regions']:
        region_location = pre_defined_region_country.get(region['RegionName'])
        r, created = Regions.objects.update_or_create(name=region['RegionName'], defaults={'active': True,
                                                                                           'location': region_location
                                                                                           })
        if created:
            print('{} Created'.format(region['RegionName']))
        else:
            print('{} exists'.format(region['RegionName']))
    print(Regions.objects.values())
