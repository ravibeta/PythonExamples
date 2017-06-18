from django.conf.urls import patterns, include, url
#from rest_framework.routers import DefaultRouter
from . import views

#router = DefaultRouter(trailing_slash=False)
#router.register(r'leases', views.MetricViewSet, base_name='metric')

urlpatterns = patterns('',
    #url(r'^', include(router.urls), name='metric'),
    url(r'^add', views.add, name='add'),
    url(r'^test$', views.test, name='test'),
)
