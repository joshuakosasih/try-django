"""
WSGI config for PeminjamanRuanganSarpras project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

#import django.core.handlers.wsgi

sys.path.append('/home/ppl/SarprasI')
#sys.path.append('/home/ppl/SarprasI/PeminjamanRuanganSarpras')
sys.path.append('/home/ppl/SarprasI/PeminjamanRuanganSarpras')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PeminjamanRuanganSarpras.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#application = django.core.handlers.wsgi.WSGIHandler()
