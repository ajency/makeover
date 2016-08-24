import sendmail
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import json
import urllib2
import requests
import sys
import re
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors import LinkExtractor


list_of_pages = []

class MySpider(CrawlSpider):
    name = "MySpider"
    rules = [Rule(LinkExtractor(allow=()),follow=True, callback='parse2')]

    iLinks = []
    images = []
    name_flag = False;

    def __init__ (self,*a, **kw):
        super(MySpider, self).__init__()
        self.allowed_domains = [a[0][1]]
        self.start_urls = [
            a[0][0],
        ]

    def parse2(self, response):

        url = response.url
        print "====================" + url + "========================"
        try:
            if str(self.allowed_domains[0]) in str(url) or not str(url).startswith('http') or not str(url).startswith('www'):
                if str(url) not in self.iLinks:
                    if '#' not in str(url).split('/')[-1] and '@' not in str(url):

                        self.iLinks.append(str(url))
                        if str(url) is not "":
                            ends_with = ['.jpg','.png','.gif','.jpeg','.bmp','.css','.js']
                            if not any(x in str(url) for x in ends_with):
                                list_of_pages.append(url)
            else:
                url = str(url)
                if not url[0] == "/":
                    url = "/" + url;
                url = str(self.allowed_domains[0]) + url;
                
                if str(url) not in self.iLinks:
                    if '#' not in str(url).split('/')[-1] and '@' not in str(url):

                        self.iLinks.append(str(url))
                        if str(url) is not "":
                            ends_with = ['.jpg','.png','.gif','.jpeg','.bmp','.css','.js']
                            if not any(x in str(url) for x in ends_with):
                                list_of_pages.append(url)
        except:
            pass


								
									
def main(main_url,main_domain):
    
    try:
        os.remove('xyz.txt')
        os.remove('data.json')
    except OSError:
        pass

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(MySpider,[main_url,main_domain])
    process.start() # the script will block here until the crawling is finished
    
    return list_of_pages

#main("http://www.onedaywithoutgoogle.org/","onedaywithoutgoogle.org");
