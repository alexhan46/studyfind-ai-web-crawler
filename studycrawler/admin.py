from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CrawlingLog)
class CrawlingLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'start_study_id',
        'end_study_id',
        'status',
        'created',
        'updated',
    ]


@admin.register(StudyLog)
class StudyLogAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'status',
        'crawled',
        'study_created',
        'study_updated',
        'created',
        'updated',
    ]


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'value',
        'datetime_value',
        'created',
        'updated',
    ]


@admin.register(Scheduler)
class SchedulerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'start_study_id',
        'end_study_id',
        'start_after',
        'interval_value',
        'interval',
        'created',
        'updated',
    ]