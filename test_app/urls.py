from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from test_app import views

urlpatterns = [
    url(r'^auth/', views.AuthView.as_view(), name='auth-view'),

    url(r'^requestgetpages/', views.RequestGetPagesView.as_view(), name='request-pages-view'),
    url(r'^checkrequestgetpages/', views.CheckRequestPagesView.as_view(), name='check-request-pages-view'),
    url(r'^getpages/', views.GetPagesView.as_view(), name='check-request-pages-view'),

    url(r'^requestscrap/', views.RequestScrapView.as_view(), name='request-scrap-view'),
    url(r'^checkscrap/', views.CheckScrapView.as_view(), name='check-scrap-view'),
    url(r'^getcontent/', views.GetContent.as_view(), name='get-content-view'),
    url(r'^getheader/', views.GetHeader.as_view(), name='get-header-view'),

    url(r'^', views.TestView.as_view(), name='test-view'),
]
