from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Reminder, ReminderForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import base64
import json
import urllib
import httplib2
http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
from django.contrib.auth.decorators import login_required
import urlparse
import logging
import sys
logger = logging.getLogger(__name__)


@csrf_exempt
def reminder_create(request):
    login = 'dummylogin'
    success = 'Success'
    error = ''
    purpose = ''
    if request.method == 'POST':
        print repr(request.POST)
        form = ReminderForm(request.POST)
        print repr(form)
        if form.is_valid():
            print 'form is valid'
            reminder = form.save(commit=False)
            if '@adobe.com' not in reminder.subscriber:
                 error = 'Invalid input!'
                 form = ReminderForm()
                 return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form, 'imgurl':''})
            import reminders.settings
            server = reminders.settings.SERVER
            port = reminders.settings.PORT
            import requests
            url = 'http://'+server+':'+port+'/lease/v1/leases'
            import urllib
            params = {#urllib.urlencode({ #urllib.parse.urlencode({
              'term':str(reminder.term),
              'email':str(reminder.subscriber),
              'purpose':str(reminder.purpose),
              #'landscape':reminder.landscape,
              }#)
            #if hasattr(request, 'user'):
            #   owner = getusername(request.user.email)
            print('url='+url+',params='+repr(params))
            logger.info('url='+url+',params='+repr(params))
            headers = {'Content-Type': 'application/x-www-form-urlencoded'} #json'} #x-www-form-urlencoded'}
            response = requests.post(url,headers=headers, data=urllib.urlencode(params), verify=False)
            status = response.status_code
            content = response.text
            print('status='+repr(status)+' content=' + repr(content))
            if '200' in str(status):
               messages.add_message(request, messages.SUCCESS, 'Reminder has been set successfully.')
               render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form },
                                 context_instance=RequestContext(request))
            else:
               messages.add_message(request, messages.ERROR, 'Server not reachable.')
        else:
           messages.add_message(request, messages.ERROR, 'Invalid input.')
    form = ReminderForm()
    return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form}, context_instance=RequestContext(request))


@csrf_exempt
def reminder_list(request):
    import reminders.settings
    server = reminders.settings.SERVER
    port = reminders.settings.PORT
    url = 'http://'+server+':'+port+'/lease/v1/leases'
    import requests
    headers = {'content-type':'application/json'}
    response = requests.get(url,headers=headers, verify=False)
    status = response.status_code
    content = response.text
    print('status='+str(status)+'content='+str(content))
    if '200' in str(status):
       models = json.loads(content)
    else:
       models = []
    return render_to_response('reminderlist.html', {'models': models}, context_instance=RequestContext(request))


@csrf_exempt
def reminder_delete(request):
    purpose = ''
    error = ''
    success = ''
    login = ''
    form = ReminderForm()
    import reminders.settings
    server = reminders.settings.SERVER
    port = reminders.settings.PORT
    ID = None
    if request.GET.get('ID') and request.GET['ID']:
        ID = request.GET.get('ID')
    if ID == None:
       messages.add_message(request, messages.ERROR, 'Invalid input.')
       return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form}, context_instance=RequestContext(request))
    url = 'http://'+server+':'+port+'/lease/v1/leases/'+str(ID)
    import requests
    headers = {'content-type':'application/json'}
    response = requests.delete(url,headers=headers, verify=False)
    status = response.status_code
    content = response.text
    print('status='+str(status)+'content='+str(content))
    if '200' in str(status):
       messages.add_message(request, messages.SUCCESS, 'Reminder deleted  successfully.')
    else:
       messages.add_message(request, messages.ERROR, 'Reminder could not be deleted.')
    return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form}, context_instance=RequestContext(request))

@csrf_exempt
def reminder_edit(request):
    purpose = ''
    error = ''
    success = ''
    login = ''
    form = ReminderForm()
    import reminders.settings
    server = reminders.settings.SERVER
    port = reminders.settings.PORT
    ID = None
    term = None
    if request.GET.get('ID') and request.GET['ID']:
        ID = request.GET.get('ID')
    if ID == None:
       messages.add_message(request, messages.ERROR, 'Invalid input.')
       return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form}, context_instance=RequestContext(request))
    if request.GET.get('term') and request.GET['term']:
        term = request.GET.get('term')
    if not term or int(term) <= 0 or int(term) > 365:
       messages.add_message(request, messages.ERROR, 'Invalid input.')
       return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form}, context_instance=RequestContext(request))
    url = 'http://'+server+':'+port+'/lease/v1/leases/'+str(ID)
    import requests
    headers = {'content-type':'application/json'}
    params = {"term": term}
    response = requests.put(url,headers=headers, data=urllib.urlencode(params), verify=False)
    status = response.status_code
    content = response.text
    print('status='+str(status)+'content='+str(content))
    if '200' in str(status):
       messages.add_message(request, messages.SUCCESS, 'Reminder edited  successfully.')
    else:
       messages.add_message(request, messages.ERROR, 'Reminder could not be updated.')
    return render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form}, context_instance=RequestContext(request))
    

@csrf_exempt
def getQRCode(request):
    ID = None
    filename = ''
    error = ''
    purpose = ''
    success = 'Error'
    owner = 'rajamani'
    if hasattr(request, 'user'):
       owner = request.user.email.split('@')[0]
    login = owner
    form = ReminderForm()
    if request.GET.get('ID', None):
       ID = request.GET['ID']
    if ID:
       import reminders.settings
       server = reminders.settings.SERVER
       port = reminders.settings.PORT
       url = 'http://'+server+':'+port+'/lease/v1/leases/'+str(ID)+'/qrcode'
       import requests
       headers = {}
       response = requests.get(url,headers=headers, verify=False)
       status = response.status_code
       content = response.text
       import random
       import string
       filename = ''.join([random.choice(string.digits + string.ascii_uppercase) for x in range(0, 6)])
       filename = reminders.settings.STATICFILES_DIRS[0]+'/'+filename+'.bmp'
       print('filename='+filename)
       import qrcode
       qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
       qr.add_data(repr(content))
       qr.make(fit=True)
       img = qr.make_image()
       img.save(filename)
       #content  = '<!DOCTYPE html><html><body>'
       #content += '<img src="data:image/png;base64,'+img.tostring() +' " alt="QRCode" />'
       #content += '</body></html>'
       print('filename='+filename)
       #with open(filename, "w") as myfile:
       #  myfile.write(content)
       success = 'Success'
    else:
       error = 'Invalid ID to retrieve reminder.'
    storage = messages.get_messages(request)
    for message in storage:
        message = message
    render_to_response('reminderform.html', {'purpose': purpose, 'error': error, 'success' : success, 'owner' : login, 'form':form, 'imgurl':'{% '+filename+' %}'})
       
