from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ModelForm, ValidationError

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
            "email": forms.TextInput(attrs={"placeholder": "you@example.com"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "10-digit number (Optional)"}),
            "pincode": forms.TextInput(attrs={"placeholder": "110006"}),
            "district_id": forms.Select,
        }

    def clean(self):
        cleaned_data = super().clean()
        error = {}

        if not cleaned_data.get("email") and not cleaned_data.get("phone_number"):
            error.update({
                "email": "Please enter either email or phone number.",
                "phone_number": "Please enter either email or phone number.",
            })

        if cleaned_data.get("search_type") == SEARCH_TYPE_CHOICES[0][0] and not cleaned_data.get("pincode"):
            error.update({
                "pincode": "Please enter your pincode",
            })

        if cleaned_data.get("search_type") == SEARCH_TYPE_CHOICES[1][0]:
            if not cleaned_data.get("state"):
                error.update({
                    "state": "Please select your State",
                })
            if not cleaned_data.get("district_id"):
                error.update({
                    "district_id": "Please select your district",
                })

        if cleaned_data.get("email") or cleaned_data.get("phone_number"):
            email = cleaned_data.get("email")
            phone_number = cleaned_data.get("phone_number")

            if cleaned_data.get("pincode"):
                if email:
                    if Subscriber.objects.filter(email=email, pincode=cleaned_data.get("pincode")).exists():
                        error.update({
                            "pincode": "You have already subscribed at this pincode.",
                        })
                elif phone_number:
                    if Subscriber.objects.filter(phone_number=phone_number, pincode=cleaned_data.get("pincode")).exists():
                        error.update({
                            "pincode": "You have already subscribed at this pincode.",
                        })

            if cleaned_data.get("district_id"):
                if email:
                    if Subscriber.objects.filter(email=email, district_id=cleaned_data.get("district_id")).exists():
                        error.update({
                            "district_id": "You have already subscribed at this district.",
                        })
                elif phone_number:
                    if Subscriber.objects.filter(phone_number=phone_number, district_id=cleaned_data.get("district_id")).exists():
                        error.update({
                            "pincode": "You have already subscribed at this district.",
                        })
                
        
        if cleaned_data.get("pincode") and cleaned_data.get("district_id"):
            cleaned_data.pop("district_id")

        if error:
            error.update({"search_type": cleaned_data.get("search_type")})
            raise ValidationError(error)

        return cleaned_data
