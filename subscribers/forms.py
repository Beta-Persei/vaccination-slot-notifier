from django.forms import ModelForm, ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from subscribers.models import Subscriber


class SubscriberForm(ModelForm):

    class Meta:
         model = Subscriber
         fields = ['email', 'age_limit', 'pincode', 'district_id']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit'

        self.helper.add_input(Submit('submit', 'Submit'))
    
    def clean(self):
        cleaned_data = super().clean()
        if (not cleaned_data.get('pincode') and not cleaned_data.get('district_id')):
            raise ValidationError({'pincode': 'Please enter your pincode', 'district_id': 'Please select your district'})
        if (cleaned_data.get('pincode') and cleaned_data.get('district_id')):
            raise ValidationError('Enter either pincode or district')
        return cleaned_data
