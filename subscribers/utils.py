import requests
from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.conf import settings

from vaccination_slot_notifier import celery_app
from sniffer.api import get_centers_by_district_id, get_centers_by_pincode

@celery_app.task
def send_slot_mail(subscriber_email, message):
    subject = "Vaccination slot found!"
    send_mail(subject, message, None, recipient_list=[subscriber_email], fail_silently=True)


def parse_centers(centers, age_limit):
    message_text = ''
    for center in centers:
        for session in center.sessions:
            if session.min_age_limit == age_limit and session.available_capacity > 0:
                slot_text = ", ".join(session.slots)
                date_text = session.date.strftime("%d-%m-%Y")
                message_text += f"""
Center name : {center.name}
Center address : {center.address}, {center.district_name}, {center.state_name}, {center.pincode}
Date : {date_text}
Vaccine : {session.vaccine}
Slot Timings : {slot_text}
Total Slots available : {session.available_capacity}

                """
    return message_text


def check_and_notify_subscriber(subscriber):
    if subscriber.pincode:
        centers = get_centers_by_pincode(subscriber.pincode)
    else:
        centers = get_centers_by_district_id(subscriber.district_id)

    if centers:
        centers_string = parse_centers(centers, subscriber.age_limit)
        if centers_string:
            message = render_to_string(
                "subscribers/notification_mail.html",
                {
                    "domain": settings.SITE_HOST_DOMAIN,
                    "centers": centers_string,
                    "subscriber_id": subscriber.id,
                },
            )

            send_slot_mail.delay(subscriber.email, message)
