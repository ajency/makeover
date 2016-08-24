from __future__ import unicode_literals

from django.db import models

# Create your models here.
class first(models.Model):
    reqId = models.CharField(primary_key=True,max_length=255)
    domainName = models.CharField(default='', max_length=512)
    data = models.TextField(default='')
