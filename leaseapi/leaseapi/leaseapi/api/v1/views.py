from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import logging
import base64
import json
import urllib
import httplib2
import os
import uuid
import mailer
from django.core import serializers
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from models import Resource, ResourceLease, ResourceSubscribers, Subscriber
from serializers import ResourceLeaseSerializer, ResourceSerializer, SubscriberSerializer
import logging
import datetime
logging.basicConfig()
logger = logging.getLogger(__name__)

user=''
password=''
http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
http.add_credentials(user, password)
auth = base64.encodestring(user + ':' + password)


class ResourceLeaseViewSet(viewsets.GenericViewSet):
  queryset = ResourceLease.objects.all()
  serializer_class = ResourceLeaseSerializer
    
  """
    list : lists the leases by resource
    PURPOSE: lists the leases
    RESULT:  returns JSON with all leases
  """
  def list(self, request):
    lease = ''
    try:
        queryset = self.get_queryset()
        #queryset = queryset.filter(user_name=request.user)
        queryset = queryset.filter(status='A')
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        logger.info(repr(serializer.data))
        #return HttpResponse(json.dumps(
        #       {'error': '', 'object_list': serializer.data}))
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
               'lease' : lease
               }), status=500)
    finally:
        pass


  def destroy(self, request, pk=None):
        """
        Delete Lease
        """
        print('delete_called_on_pk='+str(pk))
        lease = self.populate(pk)
        lease.status = "D"
        lease.save()
        #return self.list(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

  def populate(self, pk):
        try:
            pk = int(pk)
            lease = ResourceLease.objects.filter(pk=pk)
            return index
        except:
            raise Http404("ResourceLease doesn't exist.")
  
  @csrf_exempt
  def create(self, request):
    term = ''
    guid = None
    email = ''
    leaseid = ''
    try:
        if request.POST.get('term') and request.POST['term']:
           term = request.POST['term'] 
        if request.POST.get('email') and request.POST['email']:
           email = request.POST['email']
        if request.POST.get('guid') and request.POST['guid']:
           guid = request.POST['guid']
        if request.POST.get('leaseid') and request.POST['leaseid']:
           leaseid = request.POST['leaseid']
        if term==None or email==None or int(term) < 0 or int(term) > 365:
            return HttpResponse(json.dumps({'status':'error', 
                   'msg':'Term and email required.Term has to be less than 365 days'}), status=400)
        if guid == None:
              resource = Resource()
              #guid = uuid.uuid4
              #resource.guid = guid
              resource.callbackurl = ''
              resource.callbackauth = ''
              resource.save()
              print('resource saved')
              guid = resource.guid
        try:
              print('all_resources='+repr(Resource.objects.all()))
              resource = Resource.objects.get(guid=guid)
        except Resource.DoesNotExist:
              resource = None
              return HttpResponse(json.dumps({
               'status': 'error',
               'msg': 'Resource could not be created',
               'lease':'',
               }), status=500)
        try:
            subscriber = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            subscriber = None
            pass
        if subscriber == None:
           subscriber = Subscriber()
           subscriber.email = email
           subscriber.save()
        subscriber = Subscriber.objects.get(email=email)

        if not leaseid:
            lease = ResourceLease()
            print('lease.resource='+repr(resource))
            lease.resource = resource
            lease.subscriber = subscriber
            lease.term = int(term)
            from datetime import timedelta
            lease.expires = datetime.datetime.now() + timedelta(days=int(term))
            lease.status = 'A'
            lease.save()
            print('lease.id'+str(lease.id))
            leaseid = str(lease.id)
        try:
            lease = ResourceLease.objects.get(id=leaseid)
        except ResourceLease.DoesNotExist:
            lease = None
            return HttpResponse(json.dumps({
               'status': 'error',
               'msg': 'Resource could not be created',
               'lease':'',
               }), status=500)
        queryset = ResourceSubscribers.objects.filter(resource=resource)
        recipients = []
        for item in queryset:
            recipients.append(item.subscriber.email)
        if email not in recipients:
            recipients.append(email)
            ressub = ResourceSubscribers()
            ressub.resource = resource
            ressub.subscriber = subscriber
            ressub.save()
        return HttpResponse(json.dumps({'status':'success', 'guid':str(guid), 'leaseid':str(leaseid), 'subscribers':recipients}))
    except:
        import sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        import traceback
        msg = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.warn(msg)
        return HttpResponse(json.dumps({
               'status': 'error',
               'msg': msg,
               'lease':'',
               }), status=500)
    finally:
        pass
   
def unlease(request):
    rid = ''
    leaseid = ''
    if request.POST.get('guid') and request.POST['guid']:
       rid = request.POST['guid']
    if request.POST.get('leaseid') and request.POST['leaseid']:
       leaseid = request.POST['leaseid']
    if rid:
       lease = ResourceLease.objects.filter(resource_id=rid)
       if not lease:
           return HttpResponse(json.dumps({'status':'error',
              'msg': 'valid resource guid needed.'
              }), status=400)
    if leaseid:
       lease = ResourceLease.objects.filter(id=leaseid)
       if not lease:
           return HttpResponse(json.dumps({'status':'error',
              'msg': 'valid lease id needed.'
              }), status=400)
    lease.status = 'D'
    lease.save()
    resource = lease.resource
    #optionally delete resource
    return HttpResponse(json.dumps({'status':'success',
              'msg':'resource ' + str(rid) + ' removed and unsubscribed from lease',
              }))



def unsubscribe(request):
    # when the resource is active but subscribers change
    rid = ''
    leaseid = ''
    if request.POST.get('guid') and request.POST['guid']:
       rid = request.POST['guid']
    if request.POST.get('leaseid') and request.POST['leaseid']:
       leaseid = request.POST['leaseid']
    if rid:
       lease = ResourceLease.objects.filter(resource_id=rid)
       if not lease:
           return HttpResponse(json.dumps({'status':'error',
              'msg': 'valid resource guid needed.'
              }), status=400)
    if leaseid:
       lease = ResourceLease.objects.filter(id=leaseid)
       if not lease:
           return HttpResponse(json.dumps({'status':'error',
              'msg': 'valid lease id needed.'
              }), status=400)
    emails=[]
    emailstr = ''
    if request.POST.get('emails') and request.POST['emails']:
       emailstr = request.POST['emails']
    emailstr = emailstr.strip(',').strip()
    emails = emailstr.split(',')
    removed = []
    queryset = ResourceSubscribers.objects.filter(resource=lease.resource)
    for item in queryset:
        if item.subscriber.email in emails:
           removed.append(item.subscriber.email)
           item.delete()
    return HttpResponse(json.dumps({'status':'success',
              'msg': 'unsubscribed',
              'emails': removed
              }))

def test(request):
    return HttpResponse('', status=200)
    pass


class Reaper():
 def remind(self):
     for lease in ResourceLease.objects.filter(expires <= datetime.date.today()):
         #TODO : set reminder count and adjust expires
         lease.reminder += 1;
         lease.expires = self.updateExpires(lease)
         lease.save()
         users = []
         for key in ResourceSubscribers.filter(resource_id == lease.resource.id):
             if key.subscriber.email not in users:
                users.append(key.subscriber.email)
         for user in users:
             mailer.mail(owner=user, resource=lease.resource)
         if lease.resource.callbackurl:
             import httplib2
             import urllib
             import base64
             import json
             try:
                url = lease.resource.callbackurl
                auth = lease.resource.callbackauth
                logger.info('url='+url)
                params = urllib.urlencode({'id':lease.resource.id, 'msg': 'lease expiration reminder',
                      'subscribers': users, 'count':lease.reminder, 'next':repr(lease.expires)})
                response, content = http.request(url, 'POST',
                    headers={"Content-Type": "application/json", 'Authorization' : 'Basic ' + auth})
                if response.status != 200:
                    logger.error('status='+str(response.status))
                logger.info(repr(content))
                msg = 'callback invoked'
                logger.info(msg)
             except:
                pass 
     pass

 def updateExpires(self, lease):
     return lease.expires + datetime.timedelta(days=lease.term)

 def reset(self, lease):
     lease.expires = self.updateExpires()
     lease.reminder = 0
     lease.status = 'A'
     lease.save()

