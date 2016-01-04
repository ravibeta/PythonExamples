from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import logging
import base64
import json
try:
    import urllib.parse as urllib
except ImportError:
    import urllib
import httplib2
import os
import uuid
from django.core import serializers
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from models import Metric
from serializers import MetricSerializer
import logging
import datetime
logging.basicConfig()
logger = logging.getLogger(__name__)

user=''
password=''
http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
http.add_credentials(user, password)
auth = base64.encodestring(user + ':' + password)


class MetricViewSet(viewsets.GenericViewSet):
  queryset = Metric.objects.all()
  serializer_class = MetricSerializer
    
  """
    list : lists the metrics
  """
  def list(self, request):
    metric = ''
    try:
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        logger.info(repr(serializer.data))
        return Response(serializer.data)
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        msg = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.warn(msg)
        return HttpResponse(json.dumps({
               'status': 'error',
               'msg': msg,
               'metric' : metric
               }), status=500)
    finally:
        pass


  def destroy(self, request, pk=None):
        """
        Delete Metric
        """
        print('delete_called_on_pk='+str(pk))
        metric = self.populate(pk)
        metric.status = "D"
        metric.save()
        #return self.list(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

  def populate(self, pk):
        try:
            pk = int(pk)
            metric = Metric.objects.filter(pk=pk)
            return index
        except:
            raise Http404("Metric doesn't exist.")
  
  @csrf_exempt
  def create(self, request):
        logger.info('add metric='+str(request.POST);
        return HttpResponse(json.dumps({'status':'success',
              'msg':'added',
              }))
   
def add(request):
    logger.info('add metric='+str(request.POST);
    return HttpResponse(json.dumps({'status':'success',
              'msg':'added',
              }))


def test(request):
    return HttpResponse('', status=200)
    pass


