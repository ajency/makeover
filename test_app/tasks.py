import celery
from celery.decorators import task
from celery.utils.log import get_task_logger
import os

logger = get_task_logger(__name__)

from rest_framework.response import Response
from test_app.models import domainData,domainDataMeta,pageData



@task(name="crawler")
def crawler(url,domain):
    """sends an email when feedback form is filled successfully"""
 
    print "====================" + str(crawler.request.id) + "======================="
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

    try:
        obj= domainData.objects.order_by('-domainStructureQueueId')[0].domainStructureQueueId + 1
    except:
        obj = 1;

    p = domainData(cReqId=reqId , domainName=domain , data=data , domainStructureQueueId=obj)
    p.save()



    



@task(name="domainStructure")
def domainStructure(domain,cid):
    
    """sends an email when feedback form is filled successfully"""
    print "====================" + domainStructure.request.id + "======================="
    print "I am inside domainStructure"

    
    process_tasks = domainData.objects.get(cReqId=cid)
    data = process_tasks.data
    data = data.split(',')
    
    import scraper_quick2
    xyz = scraper_quick2.main([data[0],data[1],data[2],data[3],data[4]],domain)
    print "I finished running"


    
    process_tasks = domainData.objects.get(domainName=domain)
    domainStructureId = process_tasks.domainStructureQueueId


    header = str(xyz[0]).encode('utf-8')
    footer = str(xyz[1]).encode('utf-8')
    logo = str(xyz[2])
    common = str(xyz[3]).encode('utf-8')
    
    p = domainDataMeta(domainStructureQueueId=domainStructureId , key="header" , value=header)
    p.save()

    p = domainDataMeta(domainStructureQueueId=domainStructureId , key="footer" , value=footer)
    p.save()

    p = domainDataMeta(domainStructureQueueId=domainStructureId , key="logo" , value=logo)
    p.save()

    p = domainDataMeta(domainStructureQueueId=domainStructureId , key="common" , value=common)
    p.save()
    


@task(name="scraper")
def scraper(url,domain,common):
    
    """sends an email when feedback form is filled successfully"""
    print "====================" + scraper.request.id + "======================="
    print "I am inside scraper"

    string_to_list = []
    string_to_list.append(url)
    import scraper_quick3
    xyz = scraper_quick3.main(string_to_list,domain,common)
    print "I finished running"

    process_tasks = domainData.objects.get(domainName=domain)
    domainId = process_tasks.domainStructureQueueId
    
    sReqId = str(scraper.request.id.encode('ascii','ignore'))
    data = xyz[0]
    title = xyz[1]
    pageUrl = xyz[2]
    images = xyz[3]
    description = xyz[4]
    keywords = xyz[5]


    print title;

    p = pageData(domainId=domainId , pageUrl=pageUrl , data=data, title=title, images=images ,description=description ,keywords=keywords ,sReqId=sReqId)
    p.save()
    
