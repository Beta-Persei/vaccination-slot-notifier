import uuid

from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField


AGE_CATEGORY = [
    (18, "18+"),
    (45, "45+"),
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
    )
    district_id = models.IntegerField("district", blank=True, null=True)
    age_limit = models.IntegerField(
        "age limit",
        choices=AGE_CATEGORY,
        default=AGE_CATEGORY[0],
        null=False,
        blank=False,
    )

    active = models.BooleanField("active", default=True)
    last_mail_sent = models.DateTimeField(
        "last_mail", null=False, blank=True, auto_now_add=True
    )

    created_date = models.DateTimeField(
        "created_date", null=False, blank=True, auto_now_add=True
    )
    updated_date = models.DateTimeField(
        "updated_date", null=False, blank=True, auto_now=True
    )

    def __str__(self):
        return self.email
