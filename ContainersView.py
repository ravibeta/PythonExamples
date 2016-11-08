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
from lxdapi import settings
import logging
import datetime
logging.basicConfig()
logger = logging.getLogger(__name__)

class ContainerViewSet(viewsets.GenericViewSet):
  """
    list : lists the containers
    PURPOSE: lists the containers
    RESULT:  returns JSON with all containers
  """
  def list(self, request):
      containers = self.all()
      return containers

  def all(self):
      containers = []
      with open('containerslist', 'r') as f:
           for line in f.readlines():
               keys = []
               if line.startswith('+') == False:
                  parts = line.split('|')
                  container = {}
                  parts = [ x.strip() for x in parts ]
                  container["NAME"] = parts[0]
                  container["STATE"] = parts[1]
                  container["IPV4"] = parts[2]
                  containers.append(container)
      return containers
