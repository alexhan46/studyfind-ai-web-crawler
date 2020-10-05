from django.db import models

# Create your models here.
class CrawlingLog(models.Model):
    id = models.BigAutoField(
        'ID',
        primary_key=True,
    )

    start_study_id = models.BigIntegerField(
        'Start Study ID',
        null=True,
    )

    end_study_id = models.BigIntegerField(
        'End Study ID',
        null=True,
    )

    status = models.CharField(
        'Status',
        max_length=30,
        null=True,
    )

    detail = models.TextField(
        'Detail',
        default=None,
        blank=True,
        null=True,
    )

    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        'Updated',
        null=True,
    )


class StudyLog(models.Model):
    id = models.BigIntegerField(
        'ID',
        primary_key=True
    )

    status = models.CharField(
        'Status',
        max_length=100,
        null=True,
    )

    crawled = models.DateTimeField(
        'Crawled',
        null=True
    )

    study_created = models.DateTimeField(
        'Study Created',
        null=True,
    )

    study_updated = models.DateTimeField(
        'Study Updated',
        null=True,
    )

    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        'Updated',
        null=True,
    )


class Preference(models.Model):
    id = models.AutoField(
        'ID',
        primary_key=True,
    )

    name = models.CharField(
        'Name',
        max_length=100,
    )

    value = models.CharField(
        'Value',
        max_length=100,
        null=True,
        default=None,
        blank=True,
    )

    datetime_value = models.DateTimeField(
        'Datetime Value',
        null=True,
        default=None,
        blank=True,
    )

    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        'Updated',
        null=True,
    )


class Scheduler(models.Model):
    id = models.AutoField(
        'ID',
        primary_key=True,
    )

    start_study_id = models.BigIntegerField(
        'Start Study ID',
        default=None,
        blank=True,
        null=True,
    )

    end_study_id = models.BigIntegerField(
        'End Study ID',
        default=None,
        blank=True,
        null=True,
    )

    start_after = models.DateTimeField(
        'Start After',
        null=True,
    )

    interval_value = models.CharField(
        'Interval Value',
        max_length=100,
        default=None,
        blank=True,
        null=True,
    )

    interval = models.CharField(
        'Interval',
        max_length=100,
    )

    created = models.DateTimeField(
        'Created',
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        'Updated',
        null=True,
    )