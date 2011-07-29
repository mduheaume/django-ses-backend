# Django-SES-Backend

A Django email backend for Amazon Simple Email Service that does
not require an additional python package to talk to AWS.
For a more complete solution checkout django-ses
(https://github.com/hmarr/django-ses) which uses boto
(http://boto.cloudhackers.com/) for its interface to AWS.

## Usage

Add the following to settings.py in your Django project:

    EMAIL_BACKEND = "django_ses_backend.SESBackend"
    AWS_ACCESS_KEY_ID = 'YOUR-AWS-ACCESS-KEY-ID'
    AWS_SECRET_ACCESS_KEY = 'YOUR-AWS-SECRET-ACCESS-KEY'