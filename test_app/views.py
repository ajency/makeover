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
from test_app.tasks import scraper
from test_app.models import first,second




class GetHeader(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    'Please pass a id',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        if scraper.AsyncResult(data['id']).state == "SUCCESS":
            try:
                user_data = second.objects.get(reqId=data['id'])
                return Response(
                    user_data.header
                )
            except:
                return Response(
                "Please enter valid request id."
            )

        else:
            return Response(
                "Your state is: " + scraper.AsyncResult(data['id']).state
            )




class GetContent(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    'Please pass a id',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        if scraper.AsyncResult(data['id']).state == "SUCCESS":
            try:
                user_data = second.objects.get(reqId=data['id'])
                return Response(
                    user_data.data
                )
            except:
                return Response(
                "Please enter valid request id."
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
            data = request.data

            if "id" not in data:
                return Response(
                    'Please pass a id',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
                crawler.AsyncResult(data['id']).state
            )



    

class RequestScrapView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    'Please pass a id and email',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        if crawler.AsyncResult(data['id']).state == "SUCCESS":
            try:
                url_data = first.objects.get(reqId=data['id'])
                data = url_data.data
                domain = url_data.domainName
            except:
                return Response(
                "Please enter valid request id."
            )

        else:
            return Response(
                "Run Crawler First"
            )

        process_task = scraper.delay(data,domain)
        task_id = process_task.task_id
        print task_id

        
        return Response(
                task_id
            )




        


class GetPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    'Please pass a id',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        if crawler.AsyncResult(data['id']).state == "SUCCESS":
            try:
                url_data = first.objects.get(reqId=data['id'])
                return Response(
                    url_data.data
                )
            except:
                return Response(
                "Please enter valid request id."
            )

        else:
            return Response(
                "Your state is: " + crawler.AsyncResult(data['id']).state
            )





class CheckRequestPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "id" not in data:
                return Response(
                    'Please pass a id',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
                crawler.AsyncResult(data['id']).state
            )
















class RequestGetPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "url" not in data or "domain" not in data:
                return Response(
                    'Please pass a url and domain',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        url = data['url']
        domain = data['domain']

        process_task = crawler.delay(url,domain)
        task_id = process_task.task_id
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
            data = request.data

            if "url" not in data:
                return Response(
                    'Please pass a url',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_401_UNAUTHORIZED
            )

        import urllib2
        try:
            urllib2.urlopen(str(data["url"]))
        except :
            return Response(
                'Website Not Found',
                status=status.HTTP_400_BAD_REQUEST
            )

        
        return Response('Request accepted')

















class TestView(APIView):
    """
    Welcome to scraper
    """

    def post(self, request, format=None):

        try:
            data = request.data
        except:
            return Response(
                'No Data Found',
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if "email" not in data:
            return Response(
                'Please pass email',
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
                        'Database Error.',
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

    
