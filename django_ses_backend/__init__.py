import httplib
import urllib
import hashlib
import hmac
import base64
import smtplib
from datetime import datetime
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

class SESConnection:
    """An interface to Amazon's SImple Email Service.
    """
    
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self._aws_access_key_id=aws_access_key_id
        self._aws_secret_access_key=aws_secret_access_key
    
    def _get_signature(self, date_val):
        h = hmac.new(key=self._aws_secret_access_key, msg=date_val, digestmod=hashlib.sha256)
        return base64.b64encode(h.digest()).decode()
    
    def _get_headers(self):
        headers = { 'Content-type': 'application/x-www-form-urlencoded' }
        date_val = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        headers['Date'] = date_val
        signature = self._get_signature(date_val)
        headers['X-Amzn-Authorization'] = 'AWS3-HTTPS AWSAccessKeyId=%s, Algorithm=HMACSHA256, Signature=%s' % (self._aws_access_key_id, signature)
        return headers    
        
    def send_mail(self, mail_from, recipients, message):
        """Send raw message data though SES
        """
        message_b64=base64.b64encode(message)
        params = {'Source': mail_from}
        n=0
        for addr in recipients:
           n+=1
           params['Destinations.member.%d' % n] = addr
        params['RawMessage.Data']=message_b64
        params['Action'] = 'SendRawEmail'
        conn = httplib.HTTPSConnection('email.us-east-1.amazonaws.com')
        params = urllib.urlencode(params)
        conn.request('POST', '/', params, self._get_headers())
        response = conn.getresponse()
        response_result = response.read()
        conn.close()
        if response.status==200:
            pass
        else:
            raise smtplib.SMTPRecipientsRefused(recipients[0])
        
class SESBackend(BaseEmailBackend):
   
    def __init__(self,fail_silently=False,**kwargs):
        super(SESBackend, self).__init__(fail_silently=fail_silently)
        self.connection = ''
        
    def open(self):
        """Create the connection to AWS
        """
        self.connection = SESConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

    def close(self):
        """Close the connection to AWS
        """
        self.connection = None

    def send_messages(self, email_messages):
        """Sends one or more EmailMessage objects and returns the number of
        messages sent.
        """
        if not email_messages:
            return

        conn = self.open()
        if not self.connection:
            return
        
        num_sent = 0
        for message in email_messages:
            result = self._send(message)
            if result:
                num_sent += 1
        
        if conn:
            self.close()
        
        return num_sent
    
    def _send(self, email_message):
        """Sends an EmailMessage object
        """
        recipients = email_message.recipients()
        if not recipients:
            return False        
        try:
            self.connection.send_mail(email_message.from_email, email_message.recipients(),
                    email_message.message().as_string())
        except:
            if not self.fail_silently:
                raise
            return False
        return True
    
   