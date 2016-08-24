import celery
from celery.decorators import task
from celery.utils.log import get_task_logger
import os

logger = get_task_logger(__name__)

from rest_framework.response import Response
from test_app.models import first

@task(name="scraper")
def scraper(url,domain):
    
    """sends an email when feedback form is filled successfully"""
    print "====================" + scraper.request.id + "======================="
    print "I am inside scraper"
    import scraper_quick
    xyz = scraper_quick.main(url,domain)
    print "I finished running"

    data = ""
    for qwerty in xyz:
        data = data + str(qwerty) + ",";
    if data is not "":
        data = data[:-1]
    print data

    data = str(data)
    reqId = str(scraper.request.id.encode('ascii','ignore'))

    p = first(reqId=reqId , domainName=domain , data=data)
    p.save()
