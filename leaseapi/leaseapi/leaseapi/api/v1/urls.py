from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'leases', views.ResourceLeaseViewSet, base_name='lease')

urlpatterns = patterns('',
    url(r'^', include(router.urls), name='lease'),
    url(r'^unlease', views.unlease, name='unlease'),
    url(r'^unsubscribe', views.unlease, name='unsubscribe'),
    url(r'^test$', views.test, name='test'),
)
