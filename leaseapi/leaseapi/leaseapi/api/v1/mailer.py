import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
import logging
import models
from datetime import time
import leaseapi.settings

logger = logging.getLogger('mailer')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def mail(t=None, owner = None, resource = None, token=''):
    me = settings.ITC_DEV_EMAIL # the sender's email address
    if owner == None or resource == None:
       return
    you = owner # the recipient's email address
    text = 'This is a reminder for resource: ' + str(resource.id) #TODO: get resource info from callback
    message = MIMEMultipart('alternative')
    msg = MIMEText(text, 'html')
    message['Subject'] = settings.EMAIL_SUBJECT
    message['From'] = me
    message['To'] = you
    message.preamble = 'This is a multi-part message in MIME format.'
    message.attach(msg)
    s = smtplib.SMTP('europemail.eur.adobe.com')
    try:
       s.sendmail(me, [you], message.as_string())
    except Exception, e:
       logger.info('Failed to send mail to : '+ str(owner) +  str(e))
    logger.info("Mailed!")
