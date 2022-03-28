"""
WSGI config for ditry_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

path = 'home/ditry/ditry_project'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

os.environ['DJANGO_SETTINGS_MODULE']='ditry_project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
