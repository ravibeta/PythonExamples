from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import BackupRequest
from .serializers import BackupRequestSerializer
from .filters import BackupRequestFilter
from django.core import serializers
from django.http import Http404, HttpResponse, QueryDict
from django.shortcuts import render
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
'''
#import pika

import logging
import base64
import json
import urllib
import httplib2
import sys
import os
import commvaultapi.settings
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

mqserver = commvaultapi.settings.MQSERVER
vcocred = commvaultapi.settings.VCOAUTH
vcoserver = commvaultapi.settings.VCOSERVERURL
vcouser = commvaultapi.settings.VCOUSER
vcopwd = commvaultapi.settings.VCOPWD
http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

class BackupRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BackupRequestSerializer
    queryset = BackupRequest.objects.all()
    queryset = queryset.filter(status__in=['LA', 'A'])
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = BackupRequestFilter
    ordering_fields = ('id', 'name', 'location', 'backup_size', 'created')

    def perform_create(self, serializer):
        hostname = serializer.data["server"]
        owner = serializer.data["owner"] #'rajamani' # request.user
        location = ''
        print('data='+serializer.data["server"])
        print('serializer='+repr(serializer))
        if hostname:
           vmdks = find_image(hostname, owner)
           if len(vmdks) > 0:
              location = vmdks[0]
        #print(repr(self.request.user))
        serializer.save(owner=owner, location=location)

    def list(self, request):
        owner='rajamani'
        if request.GET.get('owner'):
           owner = request.GET['owner']
        escapeList = ['ordering', 'sort', 'page']
        queryset = self.get_queryset()
        isAdminPage = request.META.get('HTTP_X_PAGE')
        if not list(set(request.QUERY_PARAMS.keys()) - set(escapeList)) and not isAdminPage:
            queryset = queryset.filter(owner=owner) #created_by=request.user)

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Delete NFS Share
        """
        backup = self.populate(pk)
        backup.status = "D"
        backup.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def populate(self, pk):
        try:
            pk = int(pk)
            backup = BackupRequest.objects.get_object(pk=pk)
            return backup
        except:
            raise Http404("Nfs share doesn't exists.")
