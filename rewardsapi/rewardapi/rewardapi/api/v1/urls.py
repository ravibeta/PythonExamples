from django.conf.urls import patterns, include, url
#from rest_framework.routers import DefaultRouter
from . import views

#router = DefaultRouter(trailing_slash=False)
#router.register(r'leases', views.RewardViewSet, base_name='reward')

urlpatterns = patterns('',
    #url(r'^', include(router.urls), name='reward'),
    url(r'^add', views.add, name='add'),
    url(r'^test$', views.test, name='test'),
)
