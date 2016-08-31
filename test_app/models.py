from __future__ import unicode_literals

from django.db import models

# Create your models here.
class domainData(models.Model):
    tableId = models.AutoField(primary_key=True)
    cReqId = models.CharField(max_length=255)
    domainName = models.CharField(unique=True , max_length=512)
    data = models.TextField(default='')
    domainStructureQueueId = models.IntegerField(unique=True)


class domainDataMeta(models.Model):
    tableId = models.AutoField(primary_key=True)
    domainStructureQueueId = models.IntegerField()
    key = models.TextField(default='')
    value = models.TextField(default='')


class pageData(models.Model):
    tableId = models.AutoField(primary_key=True)
    domainId = models.CharField(default='', max_length=512)
    pageUrl = models.CharField(max_length=255)
    data = models.TextField(default='')
    title = models.TextField(default='')
    images = models.TextField(default='')
    description = models.TextField(default='')
    keywords = models.TextField(default='')
    sReqId = models.CharField(max_length=255)

