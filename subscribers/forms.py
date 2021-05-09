from django.forms import ModelForm, ValidationError
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from subscribers.models import Subscriber


SEARCH_TYPE_CHOICES = (("pincode", "Pincode"), ("district", "District"))


class SubscriberForm(ModelForm):
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPE_CHOICES,
        initial=SEARCH_TYPE_CHOICES[0][0],
        widget=forms.RadioSelect(attrs={"class": "form-check-input radio-inline"}),
    )
    state = forms.CharField(required=False, widget=forms.Select)

    class Meta:
        model = Subscriber
        fields = [
            "email",
            "phone_number",
            "age_limit",
            "pincode",
            "district_id",
            "search_type",
        ]
        widgets = {
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "pincode": forms.TextInput(attrs={"placeholder": "Pincode"}),
            "district_id": forms.Select,
        }

    def clean(self):
        cleaned_data = super().clean()
        error = {}

        if not cleaned_data.get("email") and not cleaned_data.get("phone_number"):
            error.update(
                {
                    "email": "Please enter at least one out of email or phone number.",
                    "phone_number": "Please enter at least one out of email or phone number.",
                }
            )

        if cleaned_data.get("search_type") == SEARCH_TYPE_CHOICES[0][
            0
        ] and not cleaned_data.get("pincode"):
            error.update(
                {
                    "pincode": "Please enter your pincode",
                }
            )

        if cleaned_data.get("search_type") == SEARCH_TYPE_CHOICES[1][0]:
            if not cleaned_data.get("state"):
                error.update(
                    {
                        "state": "Please select your State",
                    }
                )
            if not cleaned_data.get("district_id"):
                error.update(
                    {
                        "district_id": "Please select your district",
                    }
                )
        if cleaned_data.get("pincode") and cleaned_data.get("district_id"):
            cleaned_data.pop("district_id")

        if error:
            error.update({"search_type": cleaned_data.get("search_type")})
            raise ValidationError(error)

        return cleaned_data
