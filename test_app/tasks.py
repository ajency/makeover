import celery
from celery.decorators import task
from celery.utils.log import get_task_logger
import os

logger = get_task_logger(__name__)

from rest_framework.response import Response
from test_app.models import first
from test_app.models import second



@task(name="crawler")
def crawler(url,domain):
    
    """sends an email when feedback form is filled successfully"""
    print "====================" + crawler.request.id + "======================="
    print "I am inside Crawler"
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
    reqId = str(crawler.request.id.encode('ascii','ignore'))

    p = first(reqId=reqId , domainName=domain , data=data)
    p.save()





@task(name="scraper")
def scraper(data,domain):
    
    """sends an email when feedback form is filled successfully"""
    print "====================" + scraper.request.id + "======================="
    print "I am inside scraper"

    urls = data.split(',')

    import scraper_quick2
    xyz = scraper_quick2.main(urls,domain)
    print "I finished running"

    reqId = str(scraper.request.id.encode('ascii','ignore'))
    data = str(xyz[0]).replace('\"', "'").encode('utf-8')
    header = str(xyz[1]).replace('\"', "'").encode('utf-8')
    p = second(reqId=reqId , domainName=domain , data=data, header=header)
    p.save()
