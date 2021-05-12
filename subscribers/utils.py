import textwrap
from datetime import datetime

import requests
from constance import config
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client

from sniffer.api import get_centers_by_district_id, get_centers_by_pincode
from sniffer.models import Slots
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


def create_message_strings(slots):
    message_texts = []
    message_text = "Vaccination slot found!\n"
    for slot in slots:

        slot_text = ", ".join(slot.slots)
        center_text = f"""
{slot.name}, {slot.address}, {slot.district_name}, {slot.state_name}, {slot.pincode} on {slot.date}. Slots available {slot.available_capacity} ({slot.vaccine})

        """
        if len(center_text) + len(message_text) >= settings.TWILIO_MAX_SMS_SIZE:
            message_texts.append(message_text)
            message_text = center_text
        else:
            message_text += center_text
    message_texts.append(message_text)
    return message_texts


def welcome_new_subscriber(subscriber):
    subject = "Welcome to Vaccination Slot Notifications for CoWin"
    message = render_to_string(
        "subscribers/onboarding_mail.html",
        {
            "domain": settings.SITE_HOST_DOMAIN,
            "subscriber_id": subscriber.id,
            "mail_time_interval_mins": config.MAIL_COOLDOWN_SECONDS // 60,
        },
    )
    send_mail.delay(subscriber.email, subject, message)


def _filter_centers(centers, age_limit):
    filtered_slots = []
    for center in centers:
        for session in center.sessions:
            if session.min_age_limit == age_limit and session.available_capacity > 0:
                filtered_slots.append(Slots.from_center_session(center, session))
    return filtered_slots


def check_and_notify_subscriber(subscriber):
    if subscriber.pincode:
        centers = get_centers_by_pincode(subscriber.pincode)
    elif subscriber.pincode:
        centers = get_centers_by_district_id(subscriber.district_id)
    else:
        return

    if not centers:
        return

    filtered_slots = _filter_centers(centers, subscriber.age_limit)
    if filtered_slots:
        if subscriber.email:
            message = render_to_string(
                "subscribers/notification_mail.html",
                {
                    "domain": settings.SITE_HOST_DOMAIN,
                    "slots": filtered_slots,
                    "subscriber_id": subscriber.id,
                },
            )
            subject = "Vaccination slot found! | Notification"
            send_mail.delay(subscriber.email, subject, message)

        if config.SMS_SERVICE_ACTIVE and subscriber.phone_number:
            for message in create_message_strings(filtered_slots):
                send_whatsapp.delay(subscriber.phone_number.as_e164, message)
