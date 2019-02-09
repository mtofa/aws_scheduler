from django.contrib import admin

from .models import *

admin.site.register(Regions)
admin.site.register(SchedulesInfo)
admin.site.register(SchedulesDetails)
admin.site.register(ScheduleTags)