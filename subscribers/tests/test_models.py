from http import HTTPStatus
from typing import AnyStr, List
from unittest import mock

from constance.test import override_config
from django.contrib.messages import get_messages
from django.test import TestCase

from sniffer.models import Center
from sniffer.utils import parse_centers
from subscribers.models import Subscriber
from vaccination_slot_notifier import celery_app


class TestSubscriberModel(TestCase):
    def setUp(self):
        self.subscriber1 = Subscriber.objects.create(
            email="foo@bar.com", pincode=111111
        )
        self.subscriber2 = Subscriber.objects.create(
            phone_number="9999999999", district_id=1
        )
        self.subscriber3 = Subscriber.objects.create(
            email="foo@bar.com", phone_number="9999999999", pincode=222222, district_id=2
        )

        self.test_centers = [
            {
                "center_id": 7986,
                "name": "DGD Chhawla PHC",
                "address": "Village And Post Office Chhawla Near Radha Krishan Mandir Chhawla New Delhi - 110071",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 77,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "e18b9a85-0c6d-4684-ac5b-21dea3899867",
                        "date": "08-05-2021",
                        "available_capacity": 3,
                        "min_age_limit": 45,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    }
                ],
            },
            {
                "center_id": 693703,
                "name": "SKV DEENDARPUR 1",
                "address": "DEENPUR NEAR JHOR DEENPUR GOLA GAANV ROAD NAJAFGARH SCHOOL ID-1822176",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 77,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "0ac8ddcd-da25-477d-88a7-563b1a9877b2",
                        "date": "13-05-2021",
                        "available_capacity": 0,
                        "min_age_limit": 18,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    }
                ],
            },
            {
                "center_id": 605135,
                "name": "DGD Kanganheri",
                "address": "KANGHERI Phc",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 76,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "5e283285-b2e1-4d21-9d32-0c1bbb2195f9",
                        "date": "13-05-2021",
                        "available_capacity": 0,
                        "min_age_limit": 45,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    },
                ],
            },
            {
                "center_id": 605135,
                "name": "DGD Kanganheri",
                "address": "KANGHERI Phc",
                "state_name": "Delhi",
                "district_name": "South West Delhi",
                "block_name": "Not Applicable",
                "pincode": 110071,
                "lat": 28,
                "long": 76,
                "from": "09:00:00",
                "to": "17:00:00",
                "fee_type": "Free",
                "sessions": [
                    {
                        "session_id": "5e283285-b2e1-4d21-9d32-0c1bbb2195f9",
                        "date": "13-05-2021",
                        "available_capacity": 5,
                        "min_age_limit": 18,
                        "vaccine": "COVISHIELD",
                        "slots": [
                            "09:00AM-11:00AM",
                            "11:00AM-01:00PM",
                            "01:00PM-03:00PM",
                            "03:00PM-05:00PM",
                        ],
                    },
                ],
            },
        ]
        self.parsed_test_centers = []
        for test_center in self.test_centers:
            self.parsed_test_centers.append(Center.from_json(test_center))

        celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
        return super().setUp()

    def test_str_method(self):
        self.assertEqual(str(self.subscriber1), "foo@bar.com")
        self.assertEqual(str(self.subscriber2), "+919999999999")
        self.assertEqual(str(self.subscriber3), "foo@bar.com +919999999999")

    def test_filter_centers(self):
        filter_18 = Subscriber._filter_centers(self.parsed_test_centers, 18)
        filter_45 = Subscriber._filter_centers(self.parsed_test_centers, 45)

        self.assertEqual(len(filter_18), 1)
        self.assertEqual(len(filter_45), 1)

    def test_create_message_strings(self):
        filterd_slots = Subscriber._filter_centers(self.parsed_test_centers, 45)
        message_strings = Subscriber._create_message_strings(filterd_slots)
        self.assertIsInstance(message_strings, list)
        self.assertIn("Vaccination slot found", message_strings[0])

    @mock.patch("subscribers.utils.send_mail.delay")
    def test_send_welcome_mail(self, send_mail_func):
        self.subscriber1.send_welcome_mail()

        self.assertTrue(send_mail_func.called)
        self.assertEqual(send_mail_func.call_count, 1)
        self.assertEqual(send_mail_func.call_args[0][0], "foo@bar.com")
        self.assertEqual(
            send_mail_func.call_args[0][1],
            "Welcome to Vaccination Slot Notifications for CoWin",
        )

    @override_config(SMS_SERVICE_ACTIVE=False)
    @mock.patch("subscribers.utils.send_whatsapp.delay")
    @mock.patch("subscribers.utils.send_mail.delay")
    @mock.patch("subscribers.models.get_centers_by_pincode")
    def test_check_and_notify_slots_pincode(
        self, get_centers_func, send_mail_func, send_whatsapp_func
    ):
        get_centers_func.return_value = parse_centers(self.test_centers)

        initial_sms_count = self.subscriber1.daily_sms_count
        initial_last_mail_sent = self.subscriber1.last_mail_sent

        self.subscriber1.check_and_notify_slots()

        self.subscriber1.refresh_from_db()

        self.assertEqual(initial_sms_count, self.subscriber1.daily_sms_count)

        self.assertNotEqual(initial_last_mail_sent, self.subscriber1.last_mail_sent)

        self.assertTrue(get_centers_func.called)
        self.assertTrue(send_mail_func.called)
        self.assertFalse(send_whatsapp_func.called)

    @override_config(SMS_SERVICE_ACTIVE=True)
    @mock.patch("subscribers.utils.send_whatsapp.delay")
    @mock.patch("subscribers.utils.send_mail.delay")
    @mock.patch("subscribers.models.get_centers_by_district_id")
    def test_check_and_notify_slots_district(
        self, get_centers_func, send_mail_func, send_whatsapp_func
    ):
        get_centers_func.return_value = parse_centers(self.test_centers)

        initial_sms_count = self.subscriber2.daily_sms_count
        initial_last_mail_sent = self.subscriber2.last_mail_sent
        self.subscriber2.check_and_notify_slots()

        self.assertEqual(
            initial_sms_count + 1,
            Subscriber.objects.get(id=self.subscriber2.id).daily_sms_count,
        )
        self.assertEqual(
            initial_last_mail_sent,
            Subscriber.objects.get(id=self.subscriber2.id).last_mail_sent,
        )

        self.assertTrue(get_centers_func.called)
        self.assertFalse(send_mail_func.called)
        self.assertTrue(send_whatsapp_func.called)
