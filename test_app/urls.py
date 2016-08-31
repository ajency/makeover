from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from test_app import views

urlpatterns = [
    url(r'^demo/', views.demo.as_view(), name='demo-view'),


    
    url(r'^auth/', views.AuthView.as_view(), name='auth-view'),

    url(r'^requestgetpages/', views.RequestGetPagesView.as_view(), name='request-pages-view'),
    url(r'^forcerequestgetpages/', views.ForceRequestGetPagesView.as_view(), name='force-request-pages-view'),
    url(r'^checkrequestgetpages/', views.CheckRequestPagesView.as_view(), name='check-request-pages-view'),
    url(r'^checkrequestdomainstructure/', views.CheckRequestDomainStructureView.as_view(), name='check-request-domain-structure-pages-view'),
    url(r'^getpages/', views.GetPagesView.as_view(), name='check-request-pages-view'),
    url(r'^getdomainstructureheader/', views.GetDomainStructureHeaderView.as_view(), name='get-domain-structure-header-view'),
    url(r'^getdomainstructurefooter/', views.GetDomainStructureFooterView.as_view(), name='get-domain-structure-footer-view'),

    url(r'^requestscrap/', views.RequestScrapView.as_view(), name='request-scrap-view'),
    url(r'^forcerequestscrap/', views.ForceRequestScrapView.as_view(), name='force-request-scrap-view'),
    url(r'^checkscrap/', views.CheckScrapView.as_view(), name='check-scrap-view'),
    url(r'^getcontent/', views.GetContent.as_view(), name='get-content-view'),

    url(r'^', views.TestView.as_view(), name='test-view'),
]
