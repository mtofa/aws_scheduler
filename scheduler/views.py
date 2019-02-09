from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import connection
from .models import *
import json
import pytz



@login_required(login_url='/accounts/login/')
def index(request):
    schedule_info = SchedulesInfo.objects.all()
    load_template = 'scheduler/_content.html'
    return render(request, 'scheduler/index.html', {'schedule_info': schedule_info, 'load_template': load_template})


@login_required(login_url='/accounts/login/')
def new(request):
    load_template = 'scheduler/_new.html'
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    timezones = pytz.common_timezones
    action = '/create'
    return render(request, 'scheduler/index.html',
                  {'days': days, 'load_template': load_template, 'timezones': timezones, 'action': action})


@login_required(login_url='/accounts/login/')
def edit(request, pk):
    load_template = 'scheduler/_edit.html'
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    timezones = pytz.common_timezones
    action = '/update/{}'.format(pk)
    schedule_info = SchedulesInfo.objects.get(id=pk)
    schedule_dtls = SchedulesDetails.objects.filter(schedule_id=pk).order_by('order')
    schedule_tags = ScheduleTags.objects.filter(schedule_id=pk, active=True)
    return render(request, 'scheduler/index.html',
                  {'days': days, 'load_template': load_template, 'timezones': timezones, 'action': action,
                   'schedule_info': schedule_info, 'schedule_dtls': schedule_dtls, 'schedule_tags': schedule_tags})


@login_required(login_url='/accounts/login/')
def update(request, pk):
    json_string = next(iter(request.POST.dict()))
    jdata = json.loads(json_string)
    info = jdata['info']
    details = jdata['details']
    tags = jdata['tags']
    SchedulesInfo.objects.filter(id=pk).update(**info[0])
    for schedule in details:
        SchedulesDetails.objects \
            .filter(schedule_id=pk, day_name=schedule.get('day_name'), order=schedule.get('order')) \
            .update(**schedule)

    # TO DO: Before update cleanup
    if not tags:
        ScheduleTags.objects.filter(schedule_id=pk).delete()
    else:
        ScheduleTags.objects.filter(schedule_id=pk).update(active=False)
    for tag in tags:
        ScheduleTags.objects.update_or_create(schedule_id=pk, **tag, defaults={'active': True})
    ScheduleTags.objects.filter(schedule_id=pk, active=False).delete()  # cleanup

    return HttpResponse(200)


@login_required(login_url='/accounts/login/')
def create(request):
    json_string = next(iter(request.POST.dict()))
    jdata = json.loads(json_string)
    info = jdata['info']
    details = jdata['details']
    tags = jdata['tags']
    SchedulesInfo.objects.create(**info[0])

    schedule_i = SchedulesInfo.objects.latest('id')
    for schedule in details:
        SchedulesDetails.objects.create(schedule_id=schedule_i.id, **schedule)
    for tag in tags:
        ScheduleTags.objects.create(schedule_id=schedule_i.id, **tag)
    return HttpResponse(200)


@login_required(login_url='/accounts/login/')
def delete(request, pk):
    if request.method == 'DELETE':
        schedule_info = get_object_or_404(SchedulesInfo, pk=pk)
        schedule_info.delete()
    return HttpResponseRedirect('')
