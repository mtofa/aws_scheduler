# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from scheduler.services.currentlocaltime import *
from scheduler.services.timetable import *
import os
import json
import boto3
from pprint import pprint
import time
import json
import IPython
from scheduler.models import *

# Tag key is case sensitive
# Both Tag key and value need to match
def custom_filters():
    filters = {}
    for tag in ScheduleTags.objects.all():
        key_name = 'tag:{}'.format(tag.key_name)
        filters[tag.id] = [{
            'Name': key_name,
            'Values': [tag.value]}]
    return filters

@task()
def get_ec2_by_tags():
    for row_filters in custom_filters().items():
        row_value = {}
        row_id = row_filters[0]
        tag = row_filters[1]
        print(' ----------------------------------------------------------')
        print('  Tag:  {}'.format(tag))
        for region in Regions.objects.all():
            resource = boto3.resource('ec2', region.name)
            response = list(resource.instances.filter(Filters=tag))
            instances = []
            for instance in response:
                instances.append(instance.id)
            if len(response) > 0:
                row_value[region.name] = instances
                print('Region: {} | Instances: {}'.format(region.name, instances))
                # IPython.embed()
                ScheduleTags.objects.filter(id=row_id).update(instances=json.dumps(row_value))



@task()
def start_ec2_ins():
    print('............. Running task start_ec2_ins ..............')
    TimeTable(CurrentLocalTime()).start_instances()


@task()
def stop_ec2_ins():
    print('.............. Running task stop_ec2_ins ...............')
    TimeTable(CurrentLocalTime()).stop_instances()

