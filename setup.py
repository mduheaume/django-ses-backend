from setuptools import setup, find_packages
import os
import platform

DESCRIPTION = "A Django email backend for Amazon Simple Email Service with minimal dependencies."

LONG_DESCRIPTION = None

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

setup(
    name='django-ses-backend',
    version='0.1',
    packages=['django_ses_backend'],
    author='Mike du Heaume',
    author_email='mduheaume@gmail.com',
    url='http://github.com/mduheaume/django-mailgun/',
    license='BSD',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    classifiers=CLASSIFIERS,
)
