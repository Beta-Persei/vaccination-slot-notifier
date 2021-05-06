import requests
from datetime import datetime
from django.core.mail import send_mail

from vaccination_slot_notifier import celery_app
from sniffer.api import get_centers_by_district_id, get_centers_by_pincode

@celery_app.task
def send_slot_mail(subscriber_email, body):

    subject = "Vaccination slot found!"
    message = "We have found the following vaccination slots for you!"
    message += "\n" + body

    send_mail(subject, message, None, recipient_list=[subscriber_email], fail_silently=True)


def parse_centers(centers, age_limit):
    message_text = ''
    for center in centers:
        for session in center.sessions:
            if session.min_age_limit == age_limit and session.available_capacity > 0:
                message_text += f"""
Center name : {center.name}
Center address : {center.address}
Date : {session.date}
Vaccine : {session.vaccine}
Slot Timings : {session.slots}
Total Slots available : {session.available_capacity}

                """
    return message_text


def check_and_notify_subscriber(subscriber):
    if subscriber.pincode:
        centers = get_centers_by_pincode(subscriber.pincode)
    else:
        centers = get_centers_by_district_id(subscriber.district_id)
    print(centers)
    if centers:
        centers_string = parse_centers(centers, subscriber.age_limit)
        send_slot_mail.delay(subscriber.email, centers_string)
