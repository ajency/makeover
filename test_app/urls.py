from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from test_app import views

urlpatterns = [
    url(r'^auth/', views.AuthView.as_view(), name='auth-view'),
    url(r'^requestpages/', views.RequestPagesView.as_view(), name='request-pages-view'),
    url(r'^checkrequestgetpages/', views.CheckRequestPagesView.as_view(), name='check-request-pages-view'),
    url(r'^getpages/', views.GetPagesView.as_view(), name='check-request-pages-view'),
    url(r'^', views.TestView.as_view(), name='test-view'),
]
