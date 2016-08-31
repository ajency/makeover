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
from scrapy.spider import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

list_of_dict = []
list_of_pages = []
page_count = []
responsive = []
html_doctype = []

temporary = "panjiminn.com"

class MySpider(scrapy.Spider):
    name = "MySpider"

    iLinks = []
    images = []
    name_flag = False;

    def __init__ (self,*a, **kw):
        super(MySpider, self).__init__()
        self.allowed_domains = [a[0][1]]
        self.start_urls = []
        for asdfgh in a[0][0]:
            self.start_urls.append(asdfgh)

    def parse(self, response):
        url = response.url
        print "========================== Hello: " + url + " ============================="
        self.parse_dir_contents(response)
            

									
    def parse_dir_contents(self, response):
        page_count.append(0);
        
        url = response.url                                                       
        if url is None:
            url = str(self.allowed_domains[0]) + "index.html"
            
        list_of_pages.append(url)
        

        if self.allowed_domains[0].replace("index.html","") in list_of_pages:
            del list_of_pages[-1]

        #------------------------------------------------- Scraper -------------------------------------------------
        if str(self.allowed_domains[0]) in str(url) or not str(url).startswith('http') or not str(url).startswith('www'):
            for sel in response.xpath('//html'):
                body = sel.xpath('//body').extract()[0]

                dictionary = {}

                #print "==========================" + url + "============================="

                if not str(url).endswith('/') or not self.name_flag:
                    dictionary['name'] = str(url.split('/')[-1])
                    if dictionary['name'].count(".") == 0:
                        dictionary['name'] = dictionary['name'] + ".html"

                    if dictionary['name'] is ".html":
                        dictionary['name'] = "index.html"

                    self.name_flag = True
                else:
                    url = str(url)[:-1]
                    dictionary['name'] = str(url.split('/')[-1])
                    if dictionary['name'].count(".") == 0:
                        dictionary['name'] = dictionary['name'] + ".html"

                    if dictionary['name'] is ".html":
                        dictionary['name'] = "index.html"






                dictionary['title'] = "";
                dictionary['old_url'] = str(url);
                dictionary['content'] = ""
                dictionary['images'] = "";

                # ------- name of page in wordpress --------
                dictionary['name'] = dictionary['name'].replace('.html','').replace('.php','').replace('.aspx','').replace('.asp','')


                # ------- Get exact title of page --------
                try:
                    domain_name = [str(str(self.allowed_domains[0]).replace('www.','').replace('http://','').replace('https://','').replace(' ','')).rsplit('.', 1)[0]]
                    title = str(sel.xpath('head/title/text()').extract()[0].encode('utf-8')).replace('::','-').replace('|','-').split('-')
                    
                    flag = True;
                    flag2 = False;

                    if len(title) < 4:
                        for plm in range(0,len(title)):
                            xyz = title[plm];

                            new_string = xyz.replace(" ","").lower();
                            new_string = [new_string[i:i+5] for i in range(0, len(new_string), 5)]

                            if len(str(xyz)) > 30 or domain_name[0].strip().lower() in xyz.replace(" ","").lower():
                                flag = True;
                                continue;
                            else:

                                for qwerty in new_string:
                                    if qwerty in domain_name[0].strip().lower():
                                        flag = True;
                                        flag2 = True;
                                        print "============ Real name reverted ==============="
                                        break;

                                if flag2:
                                    flag2 = False;
                                    continue;
                                
                                flag = False;
                                title = xyz;
                                break;
                except:
                    flag = True;

                for qwerty in list_of_dict:
                    if qwerty["title"] == title:
                        flag = True;
                        break;
                
                if flag:
                    if str(url)[-1] == '/':
                        title = str(url)[:-1]
                        title = str(url).split('/')[-1]
                    else:
                        title = str(url).split('/')[-1]

                    title = title.replace('-',' ');
                    title = title.replace('_',' and ');
                    
                    if "." in str(title):
                        title = title.split('.')[0]

                if title == "" or title == "www":
                    title = "Home"
                

                dictionary['title'] = str(title).replace('\n','').replace('\t','').replace('\r','').strip()


                

                #------------------ Get content by scraping -----------------------
                body = sel.css('body').extract()[0]

                soup = BeautifulSoup(body,"html.parser")
                
                for script in soup(["head","script","style","noscript","footer","link","font"]):            #remove tags
                    script.extract()    # rip it out



                for tag in soup():                                        #for each tag in html

                    for attribute in ["class", "id", "name", "style","background","border","bordercolor","cellpadding","cellspacing"]:
                        del tag[attribute]

                    if tag.name=='a':
                        try:
                            if tag['href'] == "#":
                                del tag['href'];
                                tag.name = 'span';
                            elif "#" in tag['href']:
                                tag['href'] = tag['href'].split("#")[0]
                        except:
                            pass

                    #------------- Table code ----------------
                    if tag.name == 'tbody' or tag.name == 'thead' or tag.name == 'tfoot':
                        tag.name = 'span';

                    flag = False;
                    if tag.name == 'table':

                        for tagsssss in tag.find_all('div'):
                            flag = True;
                            break;

                        for tagsssss in tag.find_all('img'):
                            flag = True;
                            break;

                        for tagsssss in tag.find_all('table'):
                            flag = True;
                            break;

                        if flag:
                            tag.name = 'ul';
                            tag['style'] = "list-style: none";


                    flag = False;        
                    if tag.name == 'tr':

                        for tagsssss in tag.find_all('div'):
                            flag = True;
                            break;

                        for tagsssss in tag.find_all('img'):
                            flag = True;
                            break;

                        if flag:
                            tag.name = 'li';


                    flag = False;
                    if tag.name == 'td':
                        for tagsssss in tag.find_all('div'):
                            flag = True;
                            break;

                        for tagsssss in tag.find_all('img'):
                            flag = True;
                            break;
                        
                        if flag:
                            tag.name = 'span';
                            tag['style'] = "padding-right:5em";






                    if tag.name == 'div':
                        tag.name = 'p';

                        
                    try:                                                                # align
                        align = tag["align"]

                        ends_with = ['.png','.jpg','.jpeg','.bmp','.gif']
                        for yuiop in ends_with:
                            if align.endswith(yuiop):
                                tag["src"] = align
                                


                        del tag["align"]


                    except KeyError:
                        pass

                    
                    

                    try:                                                                # Image Links   (src)
                        if not tag.name == "iframe" and not tag.name == "embed":
                            src = tag["src"]
                            

                            if not str(src).startswith('http') and not str(src).startswith('www'):
                                if str(self.allowed_domains[0]) in str(src):
                                    src = str(src).split(self.allowed_domains[0], 1)[-1]
                                    src = src[1:]

                                if str(src).endswith('/'):
                                    src = str(self.allowed_domains[0]) + str(src);
                                else:
                                    src = str(self.allowed_domains[0]) + "/" + str(src);




                            tag["src"] = src;


                            
                            if src not in self.images:
                                dictionary['images'] = dictionary['images'] + src.replace('http://','').replace('https://','') + ","
                                self.images.append(src)
                            
                            tag["src"] = str(tag["src"]).split("/")[-1]
                            tag["src"] = "http://localhost/wordpress/wp-content/uploads/" + tag["src"].replace("%","")

                                
                        
                    except KeyError:
                        pass;




                    try:                                                                # Links  (href)
                        href = tag["href"]

                        if str(href).startswith('http') or str(href).startswith('www'):
                            if self.allowed_domains[0] in str(href):
                                if str(href).endswith('/'):
                                    href = str(href)[:-1]
                                    href = "http://localhost/wordpress/" + str(href).split('/')[-1]
                                    href = href.replace('.html','').replace('.php','')
                                else:
                                    href = "http://localhost/wordpress/" + str(href).split('/')[-1]
                                    href = href.replace('.html','').replace('.php','')
                        elif str(href).startswith('mail'):
                            pass
                        elif str(href).endswith('/'):
                            href = str(href)[:-1]
                            href = "http://localhost/wordpress/" + str(href).split('/')[-1]
                            href = href.replace('.html','').replace('.php','')
                        else:
                            href = "http://localhost/wordpress/" + str(href).split('/')[-1]
                            href = href.replace('.html','').replace('.php','')

                        tag["href"] = href

                        
                    except KeyError:
                        pass;



                dictionary['images'] = dictionary['images'][:-1]
        
                dictionary['content'] = soup.prettify()
                dictionary['content'] = str(dictionary['content'].replace('\n', '').replace('\"', "'").encode('utf-8').strip())
                
                list_of_dict.append(dictionary)


                break;






def removeComments(string):
    string = re.sub("(<!--.*?-->)", "", string)             # remove all occurance streamed comments (<!-- COMMENT -->) from string
    return string

def SubstringFinder(string1, string2):
    answer = []
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if ((i + j) < len1 and string1[i + j] == string2[j]):
                    match += string2[j]
            else:
                if not match == "" and len(match) > 50:
                    match = match.replace('<body >','').replace('<body>','').replace('</body>','');

                    try:
                        while not match[-1]==">" and not match[match.rfind("<") + 1] == "/":
                            match = match[:-1]

                        while not match[0]=="<" and not match[1]=="/":
                            match = match[1:]

                        if len(match) > 20:
                            answer.append(match);
                    except:
                        pass

                match = "";


        if not match == "" and len(match) > 50:
            match = match.replace('<body>','').replace('</body>','');

            try:
                while not match[-1]==">" and not match[match.rfind("<") + 1] == "/":
                    match = match[:-1]

                while not match[0]=="<" and not match[1]=="/":
                    match = match[1:]

                if len(match) > 20:
                    answer.append(match);
            except:
                pass


    #print "============== Done ================"  
    return answer


								
									
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

    #-------------------------- Post Scraping -------------------------
    
    for i in range(0,len(list_of_dict)):
        list_of_dict[i]['content'] = removeComments(list_of_dict[i]['content']);


    try:
        if list_of_dict[0]['name'] == list_of_dict[1]['name']:
            del list_of_dict[1];
    except:
        pass
    

    soup = []
    for i in range(0,len(list_of_dict)):        
        try:
            soup.append(BeautifulSoup(list_of_dict[i]['content'],"html.parser"))
        except:
            pass


    tags2 = []
    i = 0;
    j = 1;
    k = 2;
    while k<len(list_of_dict):
        flag = False;
        for tag in soup[i]():
            for tagsssss in tag.find_all(True):
                flag = True;
                break;

            if tag.name == 'p':
                flag = True;

            if flag:
                flag= False
                
                xyz = soup[j].find_all(tag.name)

                for tag2 in xyz:
                    if tag == tag2:
                        pqr = soup[k].find_all(tag.name)

                        for tag3 in pqr:
                            if tag == tag3:
                                if tag not in tags2:
                                    tags2.append(tag)
        i = i+1;
        j = j+1;
        k = k+1;


    #for zxcvb in tags2:
    #    print zxcvb
    #    print ""

    logo = "";
    if tags2:
        for tag in tags2:
            try:
                new_soup = BeautifulSoup(str(tag),"html.parser");

                for tagsss in new_soup:
                    print tag.name
                    
                    if tagsss.name == 'img':
                        logo = tagsss['src']
                        print tagsss['src']
                        break;

                if not logo == "":
                    break;
            except:
                pass






    print "\n\n======================== Footer ============================"
    footer = []
    
    #---------- Extract Footer -------------
    if tags2:
        for tag in tags2:
            #print tag
            #print ""
            try:
                new_soup = BeautifulSoup(str(tag),"html.parser");

                
                for tagsss in new_soup:
                    try:

                        #print tagsss.getText()

                        if "copyright" in str(tagsss.getText()).lower():
                            if str(tag) not in footer:
                                footer.append(str(tag))
                            break;

                        if "rights reserve" in str(tagsss.getText()).lower():
                            if str(tag) not in footer:
                                footer.append(str(tag))
                            break;

                        if "&copy" in str(tagsss.getText()).lower():
                            if str(tag) not in footer:
                                footer.append(str(tag))
                            break;

                        if "powered by" in str(tagsss.getText()).lower():
                            if str(tag) not in footer:
                                footer.append(str(tag))
                            break;


                    except:
                        pass
                    
            except:
                pass


    items_to_delete = []

    for i in range(0,len(footer)):
        for j in range(i+1,len(footer)):
            #print i
            #print j
            if footer[j] in footer[i] and j not in items_to_delete and i not in items_to_delete:
                #print "Deleting: "
                #print footer[j]
                items_to_delete.append(j);
                j = j + 1;
            elif footer[i] in footer[j] and i not in items_to_delete and j not in items_to_delete:
                #print "Deleting: "
                #print footer[i]
                items_to_delete.append(i);
                i = i + 1;

    footer2 = []
    for i in range(0,len(footer)):
        if i not in items_to_delete:
            footer2.append(footer[i])
            
    '''       
    print ""
    print ""
    print ""
    print footer;
    '''

    footer = []
    for i in footer2:
        try:
            temp_dict = {};
            temp_dict['content'] = str(i).replace('"',"'");
            footer.append(temp_dict)
        except:
            pass

    #print ""
    #print ""
    #print ""
    #print footer;
    
    print "======================== Footer ============================\n\n"
    














    #---------- Extracr nav bar ------------

    nav = "";
    flag_final = True;

    if tags2:
        for tag in tags2:
            try:
                new_soup = BeautifulSoup(str(tag),"html.parser");
                
                flag_once = True;
                flag_final = True;
                count_items = 0;

                nav = new_soup.find('ul')
                if nav is not None:
                    for tags in nav.find_all('li', recursive=False):    
                        flag_once = True;
                        for tagss in tags.find_all('a', recursive=False):                        
                            if flag_once:
                                count_items = count_items + 1;
                                flag_once = False;
                            else:
                                flag_final = False;
                                break;

                    if count_items<=3:
                        flag_final = False;

                    if flag_final:
                        print "Nav bar is present 1"
                        print "======================================="
                        #print nav.prettify();
                        print "======================================="
                        flag_final = False;
                        break;
            except:
                pass

    if flag_final:
        for tag in tags2:
            try:
                new_soup = BeautifulSoup(str(tag),"html.parser");
                
                flag_once = True;
                flag_final = True;
                count_items = 0;

                nav = new_soup.find('ul')
                if nav is not None:
                    for tags in nav.find_all('li', recursive=False):
                        for tagss in tags():
                            if tagss.name == "span":
                                for tagssss in tagss.find_all('a'):
                                    count_items = count_items + 1;

                    if count_items<=3:
                        flag_final = False;

                    if flag_final:
                        print "Nav bar is present 2"
                        print "======================================="
                        #print nav.prettify();
                        print "======================================="
                        break;
            except:
                pass


    list_of_dict2 = []
    #with open('nav.json', 'w') as f:
    #    json.dump(list_of_dict2, f)

    if not flag_final:
        list_of_dict2 = []
        try:
            nav = BeautifulSoup(str(nav),"html.parser");
            asdfg = nav.find('ul',recursive=False)
            for lists in asdfg.find_all('li',recursive=False):
                try:
                    anchor = lists.find('a',recursive=False)
                    dictionary = {}
                    dictionary['title'] = anchor.getText().strip();
                    dictionary['url'] = anchor['href'];
                    list_of_dict2.append(dictionary)
                except:
                    pass

                
            #with open('nav.json', 'w') as f:
            #    json.dump(list_of_dict2, f)
        except:
            print "Error"
    else:
        list_of_dict2 = []
        try:
            nav = BeautifulSoup(str(nav),"html.parser");

            asdfg = nav.find('ul',recursive=False)
            for lists in asdfg.find_all('li',recursive=False):
                try:
                    for tagss in tags():
                        if tagss.name == "span":
                            for tagsss in tagss():
                                if tagsss.name == "p":
                                    for tagsss in tagss.find_all('a'):
                                        dictionary = {}
                                        dictionary['title'] = tagssss.getText().strip().replace("\r","").replace("\n","").replace("\b","").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ");
                                        dictionary['url'] = tagsss['href'];
                                        list_of_dict2.append(dictionary)
                except:
                    pass

                
            #with open('nav.json', 'w') as f:
            #    json.dump(list_of_dict2, f)
        except:
            print "Error"

    #---------- Extracr nav bar ------------

    print "Reached : " + str(len(tags2) * len(soup)) 
    i = 1;
    for qwerty in soup:
        for tag in tags2:
            #print i
            i = i + 1;
            lmn = qwerty.find_all(tag.name)
            for tags in lmn:
                if tags == tag:
                    #print tags.name
                    tags.extract();

        

    i = 0;
    for xyz in soup:
        list_of_dict[i]['content'] = xyz.prettify()
        list_of_dict[i]['content'] = str(list_of_dict[i]['content'].replace('\n', '').replace('\"', "'").encode('utf-8').strip())
        i = i + 1;



    
    #---------------------------- Title --------------------------------
    already = [];
    for qwerty in list_of_dict:
        if qwerty['title'] in already:
            if qwerty['old_url'][-1] == '/':
                title = str(qwerty['old_url'])[:-1]
                title = str(qwerty['old_url']).split('/')[-1]
            else:
                title = str(qwerty['old_url']).split('/')[-1]

            title = title.replace('-',' ');
            title = title.replace('_',' and ');
                
            if "." in str(title):
                title = title.split('.')[0]

            if title == "" or title == "www":
                title = "Home"

            qwerty['title'] = title;
            already.append(qwerty['title'])
        else:
            already.append(qwerty['title'])
    
    #--------------------------- Json Data -----------------------------
    #with open('data.json', 'w') as f:
    #    json.dump(list_of_dict, f)

    common = []
    for tag in tags2:
        dictionary = {}
        dictionary['content'] = str(tag).replace('"',"'");
        common.append(dictionary);

    return [json.dumps(list_of_dict2) , json.dumps(footer) , str(logo) ,json.dumps(common)]

        
#main();
#main(["http://www.onedaywithoutgoogle.org/","http://www.onedaywithoutgoogle.org/contact.html","http://www.onedaywithoutgoogle.org/idea.html",],"onedaywithoutgoogle.org");
