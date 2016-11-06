from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter() 
router.register(r'messages', views.JiraRequestViewSet, base_name='jira')

urlpatterns = patterns('',
    url(r'^', include(router.urls), name='mail_url'),
)
