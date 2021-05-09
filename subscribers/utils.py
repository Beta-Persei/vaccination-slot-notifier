import requests
from datetime import datetime
import textwrap

from django.core.mail import send_mail
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.conf import settings
from twilio.rest import Client

from sniffer.api import get_centers_by_district_id, get_centers_by_pincode
from sniffer.models import Slots
from vaccination_slot_notifier import celery_app


twilio_client = Client(settings.TWILIO_ACCOUND_SID, settings.TWILIO_AUTH_TOKEN)


def send_onboarding_mail(subscriber_email):
    subject = "Welcome to "
    message = render_to_string(
        "subscribers/onboarding_mail.html",
        {
            "domain": settings.SITE_HOST_DOMAIN
        },
    )
    send_mail(
        subject, message, None, recipient_list=[subscriber_email], fail_silently=True
    )


@celery_app.task
def send_slot_mail(subscriber_email, message):
    subject = "Vaccination slot found!"
    send_mail(
        subject, message, None, recipient_list=[subscriber_email], fail_silently=True
    )


@celery_app.task
def send_slot_whatsapp(subscriber_number, message):
    message = twilio_client.messages.create(
        body=message,
        from_=f"whatsapp:{settings.TWILIO_PHONE_NUMBER}",
        to=f"whatsapp:{subscriber_number}",
    )


@celery_app.task
def send_slot_sms(subscriber_number, message):
    pass


def create_mail_string(slots):
    message_text = ""
    for slot in slots:
        slot_text = ", ".join(slot.slots)
        date_text = slot.date.strftime("%d-%m-%Y")
        message_text += f"""
Center : {slot.name}, {slot.address}, {slot.district_name}, {slot.state_name}, {slot.pincode}
Date : {date_text}
Vaccine : {slot.vaccine}
Slot Timings : {slot_text}
Total Slots available : {slot.available_capacity}

    """
    return message_text


def create_message_strings(slots):
    message_texts = []
    message_text = "Vaccination slot found!\n"
    for slot in slots:

        slot_text = ", ".join(slot.slots)
        date_text = slot.date.strftime("%d-%m-%Y")
        center_text = f"""
{slot.name}, {slot.address}, {slot.district_name}, {slot.state_name}, {slot.pincode} on {date_text}. Slots available {slot.available_capacity} ({slot.vaccine})

        """
        if len(center_text) + len(message_text) >= settings.TWILIO_MAX_SMS_SIZE:
            message_texts.append(message_text)
            message_text = center_text
        else:
            message_text += center_text
    message_texts.append(message_text)
    return message_texts


def filter_centers(centers, age_limit):
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

    filtered_slots = filter_centers(centers, subscriber.age_limit)
    if filtered_slots:
        if subscriber.email:
            message = render_to_string(
                "subscribers/notification_mail.html",
                {
                    "domain": settings.SITE_HOST_DOMAIN,
                    "centers": create_mail_string(filtered_slots),
                    "subscriber_id": subscriber.id,
                },
            )
            send_slot_mail.delay(subscriber.email, message)
        if subscriber.phone_number:
            for message in create_message_strings(filtered_slots):
                send_slot_whatsapp.delay(subscriber.phone_number.as_e164, message)
