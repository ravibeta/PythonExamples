from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import JiraRequest
from .serializers import JiraRequestSerializer
from django.core import serializers
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
'''
import smtplib
from ejira.mime.text import MIMEText
from ejira.mime.multipart import MIMEMultipart
from ejira.MIMEImage import MIMEImage
'''
import pika

import logging
import base64
import json
import urllib
import httplib2
import sys
import os
import jiraapi.settings
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

mqserver = jiraapi.settings.MQSERVER
http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)


def home(request):
    viewset = JiraRequestViewSet()
    return viewset.create(request)
    #return render(request, 'home.html', {})

class JiraRequestViewSet(viewsets.GenericViewSet): #(generics.ListAPIView): #(viewsets.ModelViewSet):
    serializer_class = JiraRequestSerializer
    queryset = JiraRequest.objects.all()
    
    def list(self, request):
        queryset = self.get_queryset()
        #queryset = queryset.filter(sender=request.user)
        #queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Delete JiraRequest
        """
        jira = self.populate(pk)
        jira.status = "D"
        jira.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def populate(self, pk):
        try:
            pk = int(pk)
            jira = JiraRequest.objects.get(pk=pk)
            return jira
        except:
            raise Http404("JiraRequest doesn't exist.")
    
    def create(self, request):
       print( '*** CREATE ***')
       sender = ''
       receiver = ''
       subject = ''
       message = ''
       sent = False
       try:
          print(repr(request.POST))
          if request.POST.get('sender'):
             sender = request.POST['sender']
          if request.POST.get('receiver'):
             receiver = request.POST['receiver']
          if request.POST.get('subject'):
             subject = request.POST['subject']
          if request.POST.get('message'):
             message = request.POST['message']
          if sender and receiver:
              #digest = 'compute hash'
              #jira = JiraRequest.objects.get_object_by_hash(digest)
              #if jira:
              #   return HttpResponse('Duplicate message by sender: ' + sender + ' already exists')
              jira = JiraRequest()
              jira.sender = sender
              jira.receiver = receiver
              jira.subject = subject
              jira.message = message
              jira.status = 'A'
              jira.user_name = 'rajamani' # TODO: request.user
              obj = {'sender':sender, 'receiver':receiver, 'subject':subject, 'message':message}
              connection = pika.BlockingConnection(pika.ConnectionParameters(
               jiraapi.settings.MQSERVER)) 
              from jira import JIRA
              jira_actual = JIRA('https://jira.corp.adobe.com', basic_auth=(settings.VCO_EMAIL, settings.VCO_PASSWORD))    # a username/password tuple
              projects = jira_actual.projects()
              issue_dict = {
                  'project': 'CLAPI',
                  'summary': jira.subject,
                  'description': 'SMB Background Task : create',
                  'issuetype': {'name': 'Task'},
              }
              ### put this in JIRA services to be invoked by signals
              #issue = jira.create_issue(fields=issue_dict)
              ###issue = jira_actual.issue('CLAPI-240', fields='summary,comment')
              #parameters = pika.URLParameters('amqp://guest:guest@' + '10.5.177.231' + ':5672/%2F')
              #connection = pika.BlockingConnection(parameters)
              #channel = connection.channel()
              #channel.basic_publish(SETTINGS.MQ_EXCHANGE,
              #                      SETTINGS.MQ_QUEUE,
              #                      json.dumps(result),
              #                      pika.BasicProperties(content_type='text/plain',
              #                             delivery_mode=1))
              #print(' [x] Sent ' + json.dumps(result))
              #connection.close()
              jira.save()
              sent = True
              if sent:
                 return HttpResponse(json.dumps({
                 'status': 'success',
                 'msg': 'Jira sent.'
                  }), status=200)
              else:
                 return HttpResponse(json.dumps({
                 'status': 'error',
                 'msg': 'Jira could not be sent.'
                  }), status=500)
          else:
              return HttpResponse(json.dumps({
                 'status': 'error',
                 'msg': 'Sender and Receiver missing.'
                  }), status=500)
       except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          import traceback
          msg = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
          print (msg) # for Loggregator
          sys.stdout.flush()
          logger.warn(msg)
          return HttpResponse(json.dumps({
               'status': 'error',
               'msg': msg
               }), status=500)
       finally:
          pass
       pass

