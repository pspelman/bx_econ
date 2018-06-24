"""
WSGI config for bx_econ project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bx_econ.settings")

application = get_wsgi_application()


# wsgi.py
# import os, sys
#
# # parent directory of project
# sys.path.append('/var/www/bx_econ')
# sys.path.append('/var/www/bx_econ/bx_econ')
#
# #You might not need this next line. But if you do, this directory needs to be world-writable.
# # os.environ['PYTHON_EGG_CACHE'] = '/path/to/.python-eggs'
# os.environ['DJANGO_SETTINGS_MODULE'] = 'bx_econ.settings'
#
# import django.core.handlers.wsgi
# _application = django.core.handlers.wsgi.WSGIHandler()
# def application(environ, start_response):
#     environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
#     environ['SCRIPT_NAME'] = '' # my little addition to make it work
#     return _application(environ, start_response)