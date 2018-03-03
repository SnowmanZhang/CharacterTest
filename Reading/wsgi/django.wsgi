import os
import sys
import django.core.handlers.wsgi
from django.conf import settings
import django

sys.path.insert(0,os.path.join(os.path.dirname(os.path.realpath(__file__)),'..'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'Reading.settings'
django.setup()
sys.stdout = sys.stderr

DEBUG = True

application = django.core.handlers.wsgi.WSGIHandler()
