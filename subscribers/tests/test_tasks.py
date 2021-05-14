from django.test import TestCase, tag

from subscribers.models import Subscriber
from subscribers.tasks import refresh_sms_count


class TestSubscriberUtils(TestCase):
    def setUp(self):
        self.subscribers = [
            Subscriber.objects.create(
                email="foo@bar.com", pincode=111111, daily_sms_count=10
            ),
            Subscriber.objects.create(
                phone_number="9999999999", district_id=1, daily_sms_count=12
            ),
        ]

        return super().setUp()

    def test_refresh_sms_count(self):
        refresh_sms_count()
        for subscriber in self.subscribers:
            subscriber.refresh_from_db()
            self.assertEqual(subscriber.daily_sms_count, 0)

    def test_check_available_slots(self):
        pass
