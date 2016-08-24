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
from test_app.tasks import scraper
from test_app.models import first





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
                'No Data Found 1',
                status=status.HTTP_401_UNAUTHORIZED
            )

        if scraper.AsyncResult(data['id']).state == "SUCCESS":
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
                "Your state is: " + scraper.AsyncResult(data['id']).state
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
                'No Data Found 1',
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
                scraper.AsyncResult(data['id']).state
            )
















class RequestPagesView(APIView):
    """
    After Authentication
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = request.data

            if "url" not in data or "domain" not in data or "email" not in data:
                return Response(
                    'Please pass a url,domain and email',
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                'No Data Found 1',
                status=status.HTTP_401_UNAUTHORIZED
            )

        url = data['url']
        domain = data['domain']

        process_task = scraper.delay(url,domain)
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

        
        return Response({'detail': "Request accepted"})

















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
            
        if "user" not in data or "password" not in data or "email" not in data:
            return Response(
                'Please pass username, email and password',
                status=status.HTTP_401_UNAUTHORIZED
            )

        import random, string
        
        try:
            while True:
                print data["user"]
                data["user"] = ''.join(random.choice(data["user"]) for i in range(50))
                print data["user"]
                user = User.objects.get(username=str(data["user"]))
        except:
            try:
                user = User.objects.create_user(str(data["user"]), str(data["email"]), str(data["password"]))
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

    
