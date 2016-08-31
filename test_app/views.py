from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User



#celery
from test_app.tasks import crawler
from test_app.tasks import domainStructure
from test_app.tasks import scraper
from test_app.models import domainData,domainDataMeta,pageData



#translation
from django.utils.translation import ugettext as _
from django.utils import translation


class GetContent(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')
        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        if scraper.AsyncResult(data['id']).state == "SUCCESS":
            try:
                user_data = pageData.objects.get(sReqId=data['id'])

                try:
                    import json
                    make_json = []
                    dictionary = {}
                    dictionary['html'] = user_data.data
                    dictionary['title'] = user_data.title
                    dictionary['pageUrl'] = user_data.pageUrl
                    dictionary['images'] = user_data.images
                    dictionary['description'] = user_data.description
                    dictionary['keywords'] = user_data.keywords
                    make_json.append(dictionary)

                    return Response(
                        str(json.dumps(make_json))
                    )
                except:
                    return Response(
                        _("JSON Error"),
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except:
                return Response(
                _("Please enter valid request id."),
                    status=status.HTTP_400_BAD_REQUEST
            )

        else:
            return Response(
                "Your state is: " + scraper.AsyncResult(data['id']).state
            )





class CheckScrapView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')
        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
                scraper.AsyncResult(data['id']).state
            )













#--------------- Force method ---------------
class ForceRequestScrapView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')
        
        try:
            data = request.data

            if "url" not in data or "domain" not in data:
                return Response(
                    _('Please pass url and domain'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        
        try:
            process_task = domainData.objects.get(domainName=data['domain'])
            process_task_id = process_task.domainStructureQueueId
            
            process_task = domainDataMeta.objects.get(domainStructureQueueId=process_task_id , key="common")
            common = process_task.value
        except:
            return Response(
                _("Please crawler first."),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            pageData.objects.filter(pageUrl=data['url']).delete()
        except:
            pass


        import json
        common2 = json.loads(common);

        common = []
        for xyz in common2:
            common.append(xyz['content'])
        
        process_task = scraper.delay(data['url'],data['domain'],common)
        task_id = process_task.task_id
        print task_id

        
        return Response(
                task_id
            )













    

class RequestScrapView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        
        try:
            data = request.data

            if "url" not in data or "domain" not in data:
                return Response(
                    _('Please pass url and domain'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        
        try:
            process_task = domainData.objects.get(domainName=data['domain'])
            process_task_id = process_task.domainStructureQueueId
            
            process_task = domainDataMeta.objects.get(domainStructureQueueId=process_task_id , key="common")
            common = process_task.value
        except:
            return Response(
                _("Please crawler first."),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            process_task = pageData.objects.get(pageUrl=data['url'])
            task_id = process_task.sReqId
        except:
            import json
            common2 = json.loads(common);

            common = []
            for xyz in common2:
                common.append(xyz['content'])
            
            process_task = scraper.delay(data['url'],data['domain'],common)
            task_id = process_task.task_id
            print task_id

        
        return Response(
                task_id
            )






















class GetDomainStructureFooterView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            process_task = domainData.objects.get(cReqId=data['id'])
            process_task_id = process_task.domainStructureQueueId

            process_task = domainDataMeta.objects.get(domainStructureQueueId=process_task_id,key="footer")
            footer = process_task.value

            
            return Response(
                footer
            )

            
        except:
            return Response(
                "Your state is: PENDING"
            )        


class GetDomainStructureHeaderView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            process_task = domainData.objects.get(cReqId=data['id'])
            process_task_id = process_task.domainStructureQueueId
            
            process_task = domainDataMeta.objects.get(domainStructureQueueId=process_task_id , key="header")
            header = process_task.value

            
            return Response(
                header
            )

            
        except:
            return Response(
                "Your state is: PENDING"
            )






class GetPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            process_task = domainData.objects.get(cReqId=data['id'])
            data = process_task.data

            
            return Response(
                data
            )

            
        except:
            return Response(
                _("Your state is: PENDING")
            )




class CheckRequestDomainStructureView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )


        try:
            try:
                process_task = domainData.objects.get(cReqId=data['id'])
                data = process_task.domainStructureQueueId

                process_task2 = domainDataMeta.objects.filter(domainStructureQueueId=data).exists()

                if process_task2:
                    return Response(
                            "SUCCESS"
                        )
            except:
                if domainStructure.AsyncResult(data['id']).state == "SUCCESS":
                    return Response(
                        "SUCCESS"
                    )
                else:
                    return Response(
                    "Your state is: PENDING"
                    )
        except:
            return Response(
                "Your state is: PENDING"
            )



        return Response(
                "Your state is: PENDING"
            )




class CheckRequestPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    _('Please pass a id'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )


        try:
            process_task = domainData.objects.get(cReqId=data['id'])
            return Response(
                    "SUCCESS"
                )
        except:
            return Response(
                    crawler.AsyncResult(data['id']).state
                )

















#--------------- Force method ---------------
class ForceRequestGetPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')
        
        try:
            data = request.data

            if "url" not in data or "domain" not in data:
                return Response(
                    _('Please pass a url and domain'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        url = data['url']
        domain = data['domain']

        try:
            process_task = domainData.objects.get(domainName=data['domain'])
            domainStructureId = process_task.domainStructureQueueId
            domainData.objects.filter(domainName=data['domain']).delete()
            domainDataMeta.objects.filter(domainStructureQueueId=domainStructureId).delete()
        except:
            pass
        
        #------------------------ Crawler ------------------------
        process_task = crawler.delay(url,domain)
        task_id1 = process_task.task_id
        
        #-------------------- Domain Structure --------------------
        process_task = domainStructure.delay(domain,task_id1)
        task_id2 = process_task.task_id

        print task_id1
        print task_id2

        task_id = str(task_id1) + "," + str(task_id2)

        print task_id
        
        return Response(
                task_id
            )















class RequestGetPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')
        
        try:
            data = request.data

            if "url" not in data or "domain" not in data:
                return Response(
                    _('Please pass a url and domain'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        url = data['url']
        domain = data['domain']


        
        #------------------------ Crawler ------------------------
        try:
            process_task = domainData.objects.get(domainName=data['domain'])
            task_id1 = process_task.cReqId
        except:
            process_task = crawler.delay(url,domain)
            task_id1 = process_task.task_id
        
        #-------------------- Domain Structure --------------------
        try:
            process_task = domainData.objects.get(domainName=data['domain'])
            task_id2 = process_task.domainStructureQueueId

            process_task2 = domainDataMeta.objects.filter(domainStructureQueueId=task_id2).exists()

            if not process_task2:
                process_task = domainStructure.delay(domain,task_id1)
                task_id2 = process_task.task_id
            else:
                task_id2 = task_id1
        except:
            process_task = domainStructure.delay(domain,task_id1)
            task_id2 = process_task.task_id

        

        import json
        print task_id1
        print task_id2
        dictionary = {}
        dictionary['PageRequestId'] = task_id1;
        dictionary['StructureRequestId'] = task_id2;
        output_list = []
        output_list.append(dictionary)
        task_id = json.dumps(output_list)

        task_id = str(task_id1) + "," + str(task_id2)

        print task_id
        
        return Response(
                task_id
            )











class AuthView(APIView):
    """
    Authentication is needed for this methods
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
 
    def post(self, request, format=None):

        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        try:
            data = request.data

            if "url" not in data:
                return Response(
                    _('Please pass a url'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_401_UNAUTHORIZED
            )


        import httplib
        from urlparse import urlparse
        p = urlparse(str(data["url"]))
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        if not resp.status < 400:
            return Response(
                _('Website Not Found'),
                status=status.HTTP_400_BAD_REQUEST
            )

        
        return Response(
            'Request accepted'
        )

















class TestView(APIView):
    """
    Welcome to scraper
    """

    def post(self, request, format=None):

        try:
            translation.activate(request.data['lang'])
        except:
            translation.activate('en-us')

        try:
            data = request.data
        except:
            return Response(
                _('No Data Found'),
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if "email" not in data:
            return Response(
                _('Please pass email'),
                status=status.HTTP_401_UNAUTHORIZED
            )

        import random, string
        email = data["email"]
        email2 = data["email"]
        
        try:
            while True:
                print data["email"]
                email2 = ''.join(random.choice(data["email"]) for i in range(50))
                print email2
                user = User.objects.get(username=str(email2))
        except:
            try:
                user = User.objects.create_user(str(email2), "password", str(email))
                user.save()
            except:
                return Response(
                        _('Database Error.'),
                        status=status.HTTP_404_NOT_FOUND
                    )


        token = Token.objects.get_or_create(user=user)
        print "=============================="
        print user.username
        print user.password
        print user.email
        print token
        print "=============================="
        
        return Response(str(token[0]))

    
class demo(APIView):
    """
    Welcome to scraper
    """

    def get(self, request):
        translation.activate("pt-pt")
        output = "Hello"
        return Response(output,
                status=700)
