from django.db import models


class Regions(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(null=True)
    default_display = models.BooleanField(default=False)
    description = models.TextField(null=True)
    location = models.CharField(max_length=200, null=True)
    update_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Regions'

    def __str__(self):
        return f'{self.location} -  {self.name}'


class Ec2Instances(models.Model):
    regions = models.ForeignKey(
              'Regions',
              on_delete=models.SET_NULL,
              blank=True,
              null=True
              )
    instance_id = models.CharField(max_length=200, null=False)
    name = models.CharField(max_length=200, null=True)
    instance_type = models.CharField(max_length=200, null=True)
    tags = models.TextField(null=True)
    active = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.instance_id}'


class SchedulesInfo(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Schedules Info'


class SchedulesDetails(models.Model):
    schedule = models.ForeignKey(
        'SchedulesInfo',
        on_delete=models.CASCADE,
    )
    day_name = models.CharField(max_length=20)
    start_hour = models.IntegerField(null=True)
    start_minute = models.IntegerField(null=True)
    stop_hour = models.IntegerField(null=True)
    stop_minute = models.IntegerField(null=True)
    active = models.BooleanField(default=True)
    order = models.IntegerField(null=True)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Schedules Details'

    def __str__(self):
        return f'({self.active}) - {self.day_name} - {self.start_hour} - {self.stop_hour}'


class ScheduleTags(models.Model):
    schedule = models.ForeignKey(
        'SchedulesInfo',
        on_delete=models.CASCADE,
    )
    key_name = models.CharField(max_length=300)
    value = models.CharField(max_length=300)
    instances = models.TextField(null=True)
    active = models.BooleanField(default=True)
    update_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Schedule Tags'

    def __self__(self):
        return f'{self.Key_name} - {self.Value} -{self.instances}'

