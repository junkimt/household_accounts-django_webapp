"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

#application = get_wsgi_application()


# 参考:https://qiita.com/ymhr1121/items/344c4eb300ab9972d0c2
from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)
