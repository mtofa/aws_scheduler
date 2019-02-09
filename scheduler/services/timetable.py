import json

import IPython
from scheduler.models import *
# from scheduler.tasks import start_ec2_instance, stop_ec2_instance
import boto3

class TimeTable(object):
    def __init__(self, current_local_time):
        self.day = current_local_time.day()
        self.hour = current_local_time.hour()
        self.minute = current_local_time.minute()
        self.result = []
        self.state = None

    def stop_ec2_instance(self, instance, day, hour, minute):
        zone = instance[0]
        instance_id = instance[1]
        ec2 = boto3.resource('ec2', zone)
        # IPython.embed()
        try:
            ec2.instances.filter(InstanceIds=instance_id).stop()
        except Exception as e:
            print(e)
        else:
            print('Execution Time day:{} | Hour:{} | Minute:{}'.format(day, hour, minute))
            print('Stopping...  {}'.format(instance))

    def start_ec2_instance(self, instance, day, hour, minute):
        zone = instance[0]
        instance_id = instance[1]
        ec2 = boto3.resource('ec2', zone)
        # IPython.embed()
        try:
            ec2.instances.filter(InstanceIds=instance_id).start()
        except Exception as e:
            print(e)
        else:
            print('Execution Time day:{} | Hour:{} | Minute:{}'.format(day, hour, minute))
            print('Starting ...  {}'.format(instance))

    def start_instances(self):
        self.state = 'start'
        self.get_instances_by_schedule()
        for instance in self.result:
            self.start_ec2_instance(instance, self.day, self.hour, self.minute)  # call celery

    def stop_instances(self):
        self.state = 'stop'
        self.get_instances_by_schedule()
        for instance in self.result:
            self.stop_ec2_instance(instance, self.day, self.hour, self.minute)  # call celery

    def find_instances_by_day_hour_min(self):
        schedule_ids = []
        if self.state == 'start':
            schedule_ids = SchedulesInfo.objects \
                .filter(schedulesdetails__day_name=self.day, schedulesdetails__start_hour=self.hour,
                        schedulesdetails__start_minute=self.minute) \
                .values_list('id', flat=True)

        if self.state == 'stop':
            schedule_ids = SchedulesInfo.objects \
                .filter(schedulesdetails__day_name=self.day, schedulesdetails__stop_hour=self.hour,
                        schedulesdetails__stop_minute=self.minute) \
                .values_list('id', flat=True)
        # IPython.embed()
        return self.get_instances_by_schedule_ids(schedule_ids)

    def get_instances_by_schedule_ids(self, ids):
        # IPython.embed()
        return SchedulesInfo.objects.filter(id__in=ids) \
            .values_list('scheduletags__instances', flat=True)

    def get_instances_by_schedule(self):
        for all_instances in self.find_instances_by_day_hour_min():
            if all_instances is not None:  # There may be no instance/s in a schedule
                for region_and_instances in json.loads(all_instances).items():
                    self.result.append(region_and_instances)