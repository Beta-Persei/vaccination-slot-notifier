from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase

from subscribers.forms import SubscriberForm


class TestSubscriberForm(TestCase):
    def test_valid_form_data(self):
        valid_form_data = [
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 45,
                "pincode": "",
                "state": 1,
                "district_id": 1,
                "search_type": "district",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": 111111,
                "state": "",
                "district_id": "",
                "search_type": "pincode",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": 111111,
                "state": "",
                "district_id": 10,
                "search_type": "pincode",
            },
        ]
        for data in valid_form_data:
            with self.subTest(data):
                form = SubscriberForm(data=data)
                self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        invalid_form_data = [
            {
                "email": "foo@bar.com",
                "phone_number": "+91999999999",
                "age_limit": 45,
                "pincode": "",
                "state": 1,
                "district_id": 1,
                "search_type": "district",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 1,
                "pincode": "",
                "state": 1,
                "district_id": 1,
                "search_type": "district",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": 1,
                "state": "",
                "district_id": "",
                "search_type": "pincode",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": "",
                "state": 1,
                "district_id": 2,
                "search_type": "pincode",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": 1,
                "state": "",
                "district_id": "",
                "search_type": "district",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": "",
                "state": 1,
                "district_id": "TEST",
                "search_type": "district",
            },
            {
                "email": "",
                "phone_number": "",
                "age_limit": 18,
                "pincode": "",
                "state": 1,
                "district_id": 1,
                "search_type": "district",
            },
            {
                "email": "foo@bar.com",
                "phone_number": "+919999999999",
                "age_limit": 18,
                "pincode": "",
                "state": "",
                "district_id": "",
                "search_type": "pincode",
            },
        ]
        for data in invalid_form_data:
            with self.subTest(data):
                form = SubscriberForm(data=data)
                self.assertFalse(form.is_valid())
