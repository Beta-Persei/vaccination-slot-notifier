from __future__ import absolute_import
import os
from datetime import datetime, timedelta

from celery import Celery
from django.conf import settings


from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vaccination_slot_notifier.settings")

app = Celery("vaccination_slot_notifier")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
