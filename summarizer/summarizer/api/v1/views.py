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
#import httplib2
import os
import uuid
from django.core import serializers
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
#from models import Metric
#from serializers import MetricSerializer
import logging
import datetime
logging.basicConfig()
logger = logging.getLogger(__name__)

user=''
password=''
#http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
#http.add_credentials(user, password)
#auth = base64.encodestring(user + ':' + password)

'''
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
'''   
'''
Sample post
{
  "Type" : "Notification",
  "MessageId" : "22b80b92-fdea-4c2c-8f9d-bdfb0c7bf324",
  "TopicArn" : "arn:aws:sns:us-west-2:123456789012:MyTopic",
  "Subject" : "My First Message",
  "Message" : "Hello world!",
  "Timestamp" : "2012-05-02T00:54:06.655Z",
  "SignatureVersion" : "1",
  "Signature" : "EXAMPLEw6JRNwm1LFQL4ICB0bnXrdB8ClRMTQFGBqwLpGbM78tJ4etTwC5zU7O3tS6tGpey3ejedNdOJ+1fkIp9F2/LmNVKb5aFlYq+9rk9ZiPph5YlLmWsDcyC5T+Sy9/umic5S0UQc2PEtgdpVBahwNOdMW4JPwk0kAJJztnc=",
  "SigningCertURL" : "https://sns.us-west-2.amazonaws.com/SimpleNotificationService-f3ecfb7224c7233fe7bb5f59f96de52f.pem",
  "UnsubscribeURL" : "https://sns.us-west-2.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-west-2:123456789012:MyTopic:c9135db0-26c4-47ec-8998-413945fb5a96"
  }
'''
from gensim.summarization import summarize
def add(request):
    logger.info('add metric='+str(request.POST))
    #logger.info('text='+str(request.data.get('text','')))
    text = request.POST.get('text','')
    #msgType = None
    #msgType = request.META.get('HTTP_x_amz_sns_message_type')
    #if msgType == 'Notification':
    #   #add metric
    #   pass
    #from textselector import test_build_counts, test_find_closest
    #text = get_text()
    #counts = test_build_counts(text)
    #closest = test_find_closest(text, counts)
    #closest = text.splitlines()[0:1]
    #summary = '\n'.join(closest) 
    text = text.split('.')
    text = '\n'.join(text)
    try:
       summary = summarize(text)
    except Exception as e:
       summary = str(e)
       if type(e).__name__ == "TypeError":
          summary = ''.join(text.splitlines()[0:1])
    logger.info('summary='+repr(summary))
    return HttpResponse(json.dumps({'status':'success',
              'msg':'added',
              'summary':summary
              }))


def test(request):
    return HttpResponse('', status=200)
    pass
