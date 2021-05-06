from django.forms import ModelForm, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from subscribers.models import Subscriber


class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "age_limit", "pincode", "district_id"]

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if not cleaned_data.get("pincode") and not cleaned_data.get("district_id"):
            raise ValidationError(
                {
                    "pincode": "Please enter your pincode",
                    "district_id": "Please select your district",
                }
            )
        if cleaned_data.get("pincode") and cleaned_data.get("district_id"):
            cleaned_data.pop("district_id")

        return cleaned_data
