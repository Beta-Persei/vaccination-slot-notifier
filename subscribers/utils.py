import textwrap
from datetime import datetime

import requests
from constance import config
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from twilio.rest import Client

from vaccination_slot_notifier import celery_app


@celery_app.task
def send_mail(email, subject, message):
    msg = EmailMessage(
        subject,
        message,
        None,
        to=[email],
    )
    msg.content_subtype = "html"
    msg.send(
        fail_silently=True,
    )


@celery_app.task
def send_whatsapp(subscriber_number, message):
    twilio_client = Client(settings.TWILIO_ACCOUND_SID, settings.TWILIO_AUTH_TOKEN)
    message = twilio_client.messages.create(
        body=message,
        from_=f"whatsapp:{settings.TWILIO_PHONE_NUMBER}",
        to=f"whatsapp:{subscriber_number}",
    )


@celery_app.task
def send_sms(subscriber_number, message):
    twilio_client = Client(settings.TWILIO_ACCOUND_SID, settings.TWILIO_AUTH_TOKEN)
    message = twilio_client.messages.create(
        body=message,
        from_=f"{settings.TWILIO_PHONE_NUMBER}",
        to=f"{subscriber_number}",
    )


@celery_app.task
def send_telegram_message(subscriber_number, message):
    pass
