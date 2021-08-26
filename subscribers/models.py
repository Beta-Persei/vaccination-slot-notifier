import uuid

from constance import config
from django import forms
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from sniffer.api import get_centers_by_district_id, get_centers_by_pincode
from sniffer.models import Slots
from subscribers.utils import send_mail, send_whatsapp

AGE_CATEGORY = [
    (18, "18 and older"),
    (45, "45 and older"),
]


class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("email", max_length=200, blank=True, null=True)
    phone_number = PhoneNumberField("phone number", blank=True, null=True)
    pincode = models.IntegerField(
        "pincode",
        validators=[MinValueValidator(100000), MaxValueValidator(999999)],
        blank=True,
        null=True,
        help_text="Don't know your pincode? Use 'By District'",
    )
    district_id = models.IntegerField(
        "district",
        blank=True,
        null=True,
        help_text="Districts are based on voting districts",
    )
    age_limit = models.IntegerField(
        "age limit",
        help_text="Select your age category",
        choices=AGE_CATEGORY,
        default=AGE_CATEGORY[0][0],
        null=False,
        blank=False,
    )

    active = models.BooleanField("active", default=True)
    last_mail_sent = models.DateTimeField(
        "last_mail", null=False, blank=True, default=timezone.now
    )
    daily_sms_count = models.IntegerField("daily sms count", default=0)

    created_date = models.DateTimeField(
        "created_date", null=False, blank=True, auto_now_add=True
    )
    updated_date = models.DateTimeField(
        "updated_date", null=False, blank=True, auto_now=True
    )

    def __str__(self):
        s = []
        if self.email:
            s.append(str(self.email))
        if self.phone_number:
            s.append(str(self.phone_number))

        return " ".join(s)

    @staticmethod
    def _filter_centers(centers, age_limit):
        filtered_slots = []
        for center in centers:
            for session in center.sessions:
                if (
                    session.min_age_limit == age_limit
                    and session.available_capacity > 0
                ):
                    filtered_slots.append(Slots.from_center_session(center, session))
        return filtered_slots

    @staticmethod
    def _create_message_strings(slots):
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

    def check_and_notify_slots(self):
        if self.pincode:
            centers = get_centers_by_pincode(self.pincode)
        elif self.district_id:
            centers = get_centers_by_district_id(self.district_id)
        else:
            return

        if not centers:
            return

        filtered_slots = self._filter_centers(centers, self.age_limit)
        if filtered_slots:
            if self.email:
                message = render_to_string(
                    "subscribers/notification_mail.html",
                    {
                        "domain": settings.SITE_HOST_DOMAIN,
                        "slots": filtered_slots,
                        "subscriber_id": self.id,
                    },
                )
                subject = (
                    f"{len(filtered_slots)} slots found | Vaccination Notification"
                )
                send_mail.delay(self.email, subject, message)
                self.last_mail_sent = timezone.now()

            if (
                config.SMS_SERVICE_ACTIVE
                and self.phone_number
                and self.daily_sms_count < config.MAX_DAILY_SMS_COUNT
            ):
                self.daily_sms_count = models.F("daily_sms_count") + 1

                for message in self._create_message_strings(filtered_slots):
                    send_whatsapp.delay(self.phone_number.as_e164, message)

        self.save()

    def send_welcome_mail(self):
        subject = "Welcome to Vaccination Slot Notifications for CoWin"
        message = render_to_string(
            "subscribers/onboarding_mail.html",
            {
                "domain": settings.SITE_HOST_DOMAIN,
                "subscriber_id": self.id,
                "mail_time_interval_mins": config.MAIL_COOLDOWN_SECONDS // 60,
            },
        )
        send_mail.delay(self.email, subject, message)
