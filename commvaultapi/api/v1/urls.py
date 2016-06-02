from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from api.v1 import routers
from api.v1 import signals
from . import views

#router = DefaultRouter() 
router = routers.BackupRouter(trailing_slash=False)
#router.register(r'exports', views.BackupRequestViewSet)
#router.register(r'exports', views.BackupRequestViewSet, base_name='backup')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    #url(r'stream', views.download_file, name='download_file'),
)
